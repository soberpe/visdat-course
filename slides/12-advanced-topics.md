---
marp: true
theme: visdat
paginate: true
footer: "FH OÖ Wels · Visualisierung & Datenaufbereitung"
---

<!-- _class: title -->

# Build Systems & Parallelization

## Why installing a package compiles C++, and why your script uses one core

Lecture 12 · CMake, threading, multiprocessing, Numba

<!--
Last lecture before the project phase. Two topics that look unrelated and are
not: both are about what happens underneath the Python you write. After this,
the final assignment.
-->

---

# Today

1. **Build systems**: what CMake does, and why you meet it as a Python user
2. **Parallelization**: the GIL, and the four ways around it
3. **Final assignment**: scope, deliverables, dates

---

<!-- _class: section -->

# Part 1

## Build systems and CMake

---

<!-- _class: ask -->

# Why does `pip install` sometimes take ten minutes and print C++ errors?

<!--
Because there is no prebuilt wheel for your platform, so pip builds from source, and
that build is driven by CMake. This is the honest reason a Python course spends
half an hour on build systems: sooner or later everyone hits it, and the error
messages are unreadable without knowing what is happening.
-->

---

# The problem a build system solves

One file is easy:

```bash
g++ main.cpp -O2 -std=c++17 -o app
```

Two hundred files, across three platforms, against five libraries, half of them
only rebuilt when their inputs changed, is not.

<p class="note">The build system decides what to compile, in which order, with which flags, and skips what has not changed.</p>

---

# CMake, minimal

<div class="cols">
<div>

```
my_project/
├── CMakeLists.txt
├── include/
│   └── calculator.h
└── src/
    ├── main.cpp
    └── calculator.cpp
```

</div>
<div>

```cmake
cmake_minimum_required(VERSION 3.10)
project(Calculator VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)

add_executable(calculator
    src/main.cpp
    src/calculator.cpp)

target_include_directories(
    calculator PRIVATE include)
```

</div>
</div>

CMake does not build. It **generates** the build: a Makefile on Linux, a Visual
Studio solution on Windows, Ninja anywhere.

---

# Out of source, always

```bash
mkdir build && cd build

cmake ..              # configure and generate
cmake --build .       # compile
./calculator          # run
```

Everything generated lands in `build/`, which stays out of version control.
Delete the folder and you are back to a clean state.

<p class="note">The same reason your <code>.venv</code> is not in git.</p>

---

# External libraries

```cmake
find_package(Eigen3 REQUIRED)
find_package(VTK REQUIRED)

add_executable(fem_solver src/main.cpp src/solver.cpp)

target_link_libraries(fem_solver
    Eigen3::Eigen
    ${VTK_LIBRARIES})
```

`find_package` is where most build failures happen: the library is not
installed, or it is installed somewhere CMake does not look.

---

# Where you meet CMake

<div class="cols">
<div>

**Installing**

```bash
pip install scipy
```

No wheel for your platform means pip compiles, and CMake runs.

</div>
<div>

**Extending**

```cmake
find_package(pybind11 REQUIRED)
pybind11_add_module(
    fast_solver src/bindings.cpp)
```

```python
import fast_solver
fast_solver.optimize(data)
```

</div>
</div>

<p class="note">The second is how you move a hot loop out of Python when Numba is not enough.</p>

---

<!-- _class: section -->

# Part 2

## Parallelization

---

<!-- _class: ask -->

# Your script runs for twenty minutes at 12 percent CPU. You have eight cores. Where are the other seven?

<!--
Worth a guess before reading on. The answer is the GIL for CPU work, or
waiting on I/O. 12 percent of eight cores is roughly one core, which is the
signature of both.
Distinguishing the two cases is the whole content of this block.
-->

---

# Two words that get mixed up

<div class="boxes">
<div><b>Concurrency</b>Several tasks make progress. One chef, several pots, switching between them.</div>
<div><b>Parallelism</b>Several tasks run at the same instant. Several chefs, one pot each.</div>
</div>

Concurrency helps when you are **waiting**. Parallelism helps when you are
**computing**. Choosing the wrong one is why speedups do not appear.

---

# The GIL

**Global Interpreter Lock**: only one thread executes Python bytecode at a time.

<div class="cols">
<div>

**Why it exists**

It makes memory management simple and the interpreter fast for single threaded
code, which is most code.

</div>
<div>

**What it costs**

Python threads give you **no speedup at all** for pure Python computation. Eight
threads, one core's worth of work.

</div>
</div>

---

<!-- _class: live -->

# See it yourself

```python
import threading, time

def cpu_work():
    return sum(i * i for i in range(10_000_000))

t0 = time.perf_counter(); cpu_work(); cpu_work()
print(f"sequential: {time.perf_counter() - t0:.2f}s")

t0 = time.perf_counter()
ts = [threading.Thread(target=cpu_work) for _ in range(2)]
[t.start() for t in ts]; [t.join() for t in ts]
print(f"threaded:   {time.perf_counter() - t0:.2f}s")
```

<!--
The two numbers come out nearly identical, sometimes the threaded one is
slower. Nothing convinces like watching it: with the task manager open, one
core sits at 100 percent while the others idle.
-->

---

# When threading does work

<div class="cols">
<div>

**Waiting**

Network requests, reading files, database queries. The GIL is released while
you wait, so threads overlap.

</div>
<div>

**C code that releases the GIL**

```python
solve = factorized(A)          # scipy, C
X = Parallel(prefer="threads")(
    delayed(compute_column)(solve, B, i)
    for i in range(n))
```

Measured: **2.44x**, with no pickling cost.

</div>
</div>

<p class="note">NumPy, SciPy and VTK spend most of their time in C, where the GIL is not held. That is why they parallelize better than you expect.</p>

---

# Multiprocessing: a new interpreter per core

```python
import multiprocessing as mp

def compute_eigenvalues(matrix):
    return np.sort(np.abs(np.linalg.eigvals(matrix)))[::-1]

if __name__ == "__main__":                 # required on Windows
    matrices = [np.random.rand(200, 200) for _ in range(80)]
    with mp.Pool(processes=8) as pool:
        results = pool.map(compute_eigenvalues, matrices)
```

No shared GIL, because there is no shared interpreter. The price: every input
and every result is pickled and copied between processes.

---

# Why the speedup is 2.88x and not 8x

<div class="cols">
<div>

**Where it goes**

Process startup, pickling the matrices, copying the results back, and the part
of the program that stays serial.

</div>
<div>

**Amdahl**

If 20 percent of the runtime cannot be parallelized, eight cores buy you at
most 3.3x. Ever.

</div>
</div>

> Report the speedup you measured, not the number of cores you used. The second
> one is not a result.

---

# Numba: compile the loop instead

```python
@numba.jit(nopython=True, parallel=True)
def monte_carlo_pi(n):
    inside = 0
    for _ in numba.prange(n):           # parallel, and no GIL
        x, y = np.random.random(), np.random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / n
```

| | Pure Python | Numba | Numba parallel |
|---|---|---|---|
| 100M samples | 45 s | 0.8 s | 0.15 s |

<p class="note">Most of the gain is compilation, not parallelism. The first call is slow because it compiles.</p>

---

# asyncio, for many connections at once

```python
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(fetch(session, u) for u in urls))
```

One thread, thousands of open connections, each one idle most of the time. The
right tool for web APIs and data collection, the wrong tool for computation.

---

# Which one, when

| Your work is | Use |
|---|---|
| Waiting on a few files or requests | `threading` |
| Waiting on hundreds of connections | `asyncio` |
| Pure Python loops, CPU bound | `multiprocessing` |
| Numerical loops over arrays | `numba` with `parallel=True` |
| NumPy or SciPy calls | often already parallel, measure first |

---

# Measure before you optimize

```python
import cProfile
cProfile.run("main()", sort="cumtime")
```

```bash
python -m cProfile -s cumtime my_script.py | head -20
```

> Almost every optimization that starts with a guess is wasted. Find the line
> that actually costs the time, and it is usually not the one you suspected.

<!--
This is the most useful slide of the block. Run the profiler on something from
the data processing lecture, and the time usually goes into read_csv, not into
the loop everyone was worried about.
-->

---

# Pitfalls

<div class="cols">
<div>

**Threads for CPU work**

No speedup. The GIL is still there.

**Shared state without a lock**

```python
counter += 1     # race condition
```

</div>
<div>

**Forgetting the guard**

```python
if __name__ == "__main__":
```

Without it, multiprocessing on Windows spawns processes forever.

</div>
</div>

---

# Recap

- CMake **generates** builds, and you meet it whenever pip compiles
- The **GIL** means Python threads do not speed up Python computation
- **Threading** for waiting, **multiprocessing** for Python loops, **Numba** for
  numerical loops
- The speedup is always less than the core count, and **Amdahl** says by how much
- **Profile first**

---

<!-- _class: section -->

# Final assignment

## Your own project

---

# What it is

An individual project along the chain of this course: load data, process it,
visualize it, and wrap it in something that can be operated.

<div class="boxes">
<div><b>Extend</b>Take something from the semester further: more features, more depth.</div>
<div><b>Build new</b>Your own idea in scientific data handling or visualization.</div>
<div><b>Use it</b>A problem from your thesis, your job, or your research.</div>
</div>

<p class="note">Full description with folder layout and grading: Final Assignment on the course site.</p>

---

# What you hand in

```
submissions/<your-github-username>/final/
├── README.md          what it does, how to run it, what you solved
├── code/              entry point, modules, sample data, requirements.txt
├── slides.md          your presentation, in Marp
└── assets/            screenshots
```

| | |
|---|---|
| **Individual ideas** | 30 % |
| **Code quality and function** | 40 % |
| **Documentation and presentation** | 30 % |

---

# Two things that decide the grade

<div class="cols">
<div>

**It has to run**

On my machine, in a fresh virtual environment, from your `requirements.txt`.
Test that before you submit, not after.

</div>
<div>

**The history has to show the work**

Commits over weeks, not one drop on the deadline. That is part of what is
assessed, and it is also what saves you when something breaks.

</div>
</div>

<p class="note">Deadline and presentation date: announced in class, end of January.</p>

---

<!-- _class: section -->

# Questions

<p>Then: Qt workshop, and pick a project topic.</p>
