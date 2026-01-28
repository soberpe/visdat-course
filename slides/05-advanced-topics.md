---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-size: 26px;
    padding: 40px 50px;
  }
  h1 {
    font-size: 46px;
    color: #2c3e50;
    margin-bottom: 20px;
  }
  h2 {
    font-size: 36px;
    color: #34495e;
    margin-bottom: 15px;
  }
  code {
    font-size: 20px;
  }
  pre {
    margin: 10px 0;
  }
  footer {
    font-size: 16px;
  }
---

# Advanced Topics
## Build Systems & Parallelization

**Visualization and Data Analysis Course**
Cross-Platform Development & Parallel Computing

---

## Today's Agenda

**Input (45 min)**: Advanced Topics
- CMake & Build Systems (awareness level)
- Parallelization & Concurrency
- Python GIL and threading
- Multiprocessing & Numba

**Practice (90 min)**: Qt Workshop
- Work on FEM Viewer exercises
- Individual progress on interactive applications

**Assignment (15 min)**: Final Project
- Requirements and deliverables
- Timeline and grading criteria

---

# Part 1: CMake & Build Systems

## Why Build Systems?

---

## The Compilation Problem

Manual compilation becomes unmaintainable:

```bash
g++ -c src/main.cpp -o build/main.o -I include
g++ -c src/processor.cpp -o build/processor.o -I include  
g++ -c src/utils.cpp -o build/utils.o -I include
g++ -c src/solver.cpp -o build/solver.o -I include
g++ -c src/io.cpp -o build/io.o -I include
...
g++ build/*.o -o app -lopencv -leigen3
```

**Problems:**
- Tedious for large projects
- Platform-specific compiler flags
- Dependency management
- Incremental builds

---

## What is CMake?

**CMake** = Cross-platform Make

Not a build system itself, but a **build system generator**:

```
CMakeLists.txt → CMake → Makefile/VS Project → Build Tool → Executable
```

**Abstracts platform differences:**
- Linux: generates Makefiles
- Windows: generates Visual Studio solutions
- macOS: generates Xcode projects
- Any: generates Ninja build files

---

## Basic CMake Example

**Project structure:**
```
my_project/
├── CMakeLists.txt
├── include/
│   └── calculator.h
└── src/
    ├── main.cpp
    └── calculator.cpp
```

**CMakeLists.txt:**
```cmake
cmake_minimum_required(VERSION 3.10)
project(Calculator VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)

add_executable(calculator src/main.cpp src/calculator.cpp)
target_include_directories(calculator PRIVATE include)
```

---

## Building with CMake

```bash
# Create build directory (out-of-source build)
mkdir build
cd build

# Generate build files
cmake ..

# Build the project
cmake --build .

# Run the executable
./calculator
```

**Key concept:** Always build in separate `build/` directory!

---

## CMake with External Libraries

```cmake
cmake_minimum_required(VERSION 3.10)
project(FEMSolver)

set(CMAKE_CXX_STANDARD 17)

# Find required packages
find_package(OpenCV REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(VTK REQUIRED)

add_executable(fem_solver src/main.cpp src/solver.cpp)

# Link libraries
target_link_libraries(fem_solver 
    ${OpenCV_LIBS}
    Eigen3::Eigen
    ${VTK_LIBRARIES}
)
```

---

## When You Encounter CMake

### As a Python User:

1. **Installing packages from source:**
   ```bash
   pip install opencv-python  # May use CMake internally
   pip install scipy          # Compiled extensions
   ```

2. **Creating Python C++ extensions:**
   ```cmake
   find_package(pybind11 REQUIRED)
   pybind11_add_module(fast_solver src/bindings.cpp)
   ```
   Then use in Python:
   ```python
   import fast_solver
   result = fast_solver.optimize(data)
   ```

---

## CMake: Key Takeaways

1. **Automates compilation** for large C++ projects
2. **Cross-platform** - same CMakeLists.txt works everywhere
3. **Industry standard** - used by OpenCV, VTK, Blender, etc.
4. **You'll encounter it** when:
   - Building C++ projects
   - Installing Python packages from source
   - Creating Python extensions for performance

**For Python-focused work:** Understanding basic concepts is sufficient. Deep expertise needed only when building complex C++ projects.

---

# Part 2: Parallelization

## Making Your Code Faster

---

## Why Parallelization?

Modern computers have multiple CPU cores:
- Desktop: 4-16 cores typical
- Workstation: 16-64 cores
- Server: 64-256+ cores

**Problem:** Single-threaded Python uses only ONE core!

**Solution:** Parallelization to utilize all cores

**Example:** Processing 1000 images
- Sequential: 10 minutes
- Parallel (8 cores): ~1.3 minutes

---

## Concurrency vs. Parallelism

**Concurrency:**
Multiple tasks making progress (not necessarily simultaneously)

**Parallelism:**
Multiple tasks executing simultaneously on different cores

**Analogy:**
- **Concurrency:** One chef cooking multiple dishes, switching between them
- **Parallelism:** Multiple chefs each cooking different dishes simultaneously

---

## The Python GIL Problem

**GIL** = Global Interpreter Lock

**What it does:**
Only ONE thread can execute Python bytecode at a time

**Why it exists:**
- Simplifies memory management
- Makes Python easier to implement
- Protects internal data structures

**Impact:**
❌ Python threads DO NOT provide parallel speedup for CPU-bound tasks!

---

## GIL Demonstration

```python
import threading, time

def cpu_work():
    total = 0
    for i in range(10_000_000):
        total += i * i
    return total

# Sequential
start = time.time()
cpu_work()
cpu_work()
print(f"Sequential: {time.time() - start:.2f}s")

# Multi-threaded (still limited by GIL!)
start = time.time()
t1 = threading.Thread(target=cpu_work)
t2 = threading.Thread(target=cpu_work)
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Threaded: {time.time() - start:.2f}s")  # Same time!
```

---

## Threading: When It Works

**Good for I/O-bound tasks:**
- Network requests
- File operations
- Database queries
- User input

During I/O, GIL is released → other threads can run

```python
import threading, requests

urls = ["https://api.example.com/data1", "https://api.example.com/data2", ...]

def download(url):
    response = requests.get(url)
    save_data(response.content)

threads = [threading.Thread(target=download, args=(url,)) for url in urls]
for t in threads: t.start()
for t in threads: t.join()  # Much faster!
```

---

## Thread Synchronization

**Problem:** Multiple threads accessing shared data → race conditions

**Solution:** Locks (mutexes)

```python
import threading

class BankAccount:
    def __init__(self):
        self.balance = 1000
        self.lock = threading.Lock()  # Protection
    
    def deposit(self, amount):
        with self.lock:  # Acquire lock
            current = self.balance
            current += amount
            self.balance = current
        # Lock automatically released

account = BankAccount()
# Multiple threads can safely deposit
```

---

## Processes vs. Threads

| Aspect | Threads | Processes |
|--------|---------|-----------|
| **GIL Impact** | ❌ Limited by GIL | ✓ No GIL |
| **Memory** | Shared | Separate |
| **Overhead** | Low | Higher |
| **Data Sharing** | Easy | Complex |
| **Best For** | I/O-bound | CPU-bound |

**Key point:** For CPU-intensive work, use **multiprocessing**!

---

## Multiprocessing in Python

Each process has its own Python interpreter → no GIL limitation!

```python
import multiprocessing as mp
import numpy as np

def expensive_computation(data_chunk):
    """Heavy computation - benefits from multiprocessing"""
    return np.sum(np.sin(data_chunk * np.arange(1000)))

# Split data into chunks
data = np.random.rand(8000, 100)
chunks = np.array_split(data, 8)

# Parallel processing
with mp.Pool(processes=8) as pool:
    results = pool.map(expensive_computation, chunks)
# 8x speedup possible!
```

---

## Real-World Example: Eigenvalues

**Problem:** Compute eigenvalues for many matrices

Each matrix computation is independent → **perfect for parallelization**!

**Application:** Parameter studies in structural dynamics

```python
def compute_eigenvalues(matrix):
    eigenvalues = np.linalg.eigvals(matrix)
    return np.sort(np.abs(eigenvalues))[::-1]

if __name__ == '__main__':
    matrices = [np.random.rand(200, 200) for _ in range(80)]
    
    # Parallel computation
    with mp.Pool(processes=8) as pool:
        results = pool.map(compute_eigenvalues, matrices)
```

**Measured speedup:** 2.88x on 8 cores (80 matrices)

---

## Advanced: Threading with C Extensions

**Special case:** Threading CAN work for CPU-bound tasks when C/Fortran extensions release the GIL!

```python
from scipy.sparse.linalg import factorized
from joblib import Parallel, delayed

def compute_column(solve_func, B, col_idx):
    return solve_func(B[:, col_idx].toarray().ravel())

# Factorize once, solve columns with threading
solve = factorized(A)  # C code
X_cols = Parallel(prefer="threads")(  # Threading works!
    delayed(compute_column)(solve, B, i) for i in range(num_cols)
)
```

**Why it works:** scipy sparse solvers release GIL in C code  
**Speedup:** 2.44x (no pickling overhead!)

---

## Numba: The Game Changer

**Numba** = Just-In-Time (JIT) compiler for Python

**Why it's important:**
1. ✓ Compiles Python to machine code
2. ✓ **Releases the GIL**
3. ✓ Near-C performance
4. ✓ Easy to use (just add decorator!)

```python
import numba

@numba.jit(nopython=True)
def fast_computation(data):
    result = 0.0
    for i in range(len(data)):
        result += np.sin(data[i]) * np.cos(data[i])
    return result
```

**Typical speedup:** 10-100x over pure Python!

---

## Numba Parallel Execution

```python
import numba

@numba.jit(nopython=True, parallel=True)
def parallel_computation(data):
    n = len(data)
    result = np.zeros(n)
    
    for i in numba.prange(n):  # Parallel range - no GIL!
        result[i] = expensive_calc(data[i])
    
    return result
```

**Benefits:**
- No GIL limitation
- Automatic parallelization
- Minimal code changes
- Works great with NumPy

---

## Monte Carlo Example

```python
import numba, numpy as np

@numba.jit(nopython=True, parallel=True)
def monte_carlo_pi(n_samples):
    inside = 0
    for _ in numba.prange(n_samples):  # Parallel!
        x, y = np.random.random(), np.random.random()
        if x*x + y*y <= 1.0:
            inside += 1
    return 4.0 * inside / n_samples

pi_estimate = monte_carlo_pi(100_000_000)
```

**Performance:**
- Pure Python: 45s
- Numba: 0.8s (56x faster!)
- Numba parallel: 0.15s (300x faster!)

---

## asyncio: Another Approach

For **many concurrent I/O operations** (hundreds/thousands):

```python
import asyncio, aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Efficiently handle 1000+ concurrent requests
results = asyncio.run(fetch_all(urls))
```

**When to use:** Web scraping, API clients, many network connections

---

## Choosing the Right Approach

**I/O-bound tasks** (network, files, database):
- Few operations → `threading`
- Many operations → `asyncio`

**CPU-bound tasks** (computation, data processing):
- Pure Python loops → `multiprocessing`
- NumPy/SciPy numerical code → `numba` (parallel=True)
- NumPy/SciPy with C extensions → `threading` may work if GIL released

**Mixed workload:**
- Combine approaches (e.g., multiprocessing + Numba)

---

## Common Pitfalls

❌ **Using threads for CPU work:**
```python
# Won't speed up due to GIL!
threads = [threading.Thread(target=heavy_calc) for _ in range(8)]
```

✓ **Use multiprocessing instead:**
```python
with mp.Pool(8) as pool:
    results = pool.map(heavy_calc, data_chunks)
```

❌ **Sharing data without locks:**
```python
counter = 0  # Race condition!
def increment():
    global counter
    counter += 1
```

---

## Parallelization: Key Takeaways

1. **GIL limits threading** for CPU-bound tasks
2. **Threading works** for I/O-bound tasks
3. **Multiprocessing** bypasses GIL (separate processes)
4. **Numba** provides parallel execution without GIL
5. **Always profile** before optimizing
6. **Use locks** when threads share mutable state

**For scientific computing:**
- Heavy computation → Numba or multiprocessing
- Data loading/saving → threading or asyncio
- Large-scale → consider Dask or distributed computing

---

# Practice Time

## Qt Workshop (90 min)

Work through the **Qt Workshop** exercises:
- Build complete FEM Viewer application
- File loading, field selection, visualization controls
- Deformation visualization
- Try the extension challenges!

**Online documentation:**
https://soberpe.github.io/visdat-course/user-interfaces/qt-workshop

**Approach:**
- Work at your own pace
- Complete Block 1 first (foundation), try to reach Block 3 (advanced features)

---

# Final Assignment

## Individual Project

---

## Assignment Overview

**Type:** Individual project  
**Topic:** Flexible - scientific data handling/visualization  
**Deadline:** January 28, 2026, 23:59 (PR submission)  
**Presentation:** Last January session

**Freedom:**
- Extend semester projects (FEM viewer, data processing, visualization)
- Create new project related to your interests
- Solve real problem from thesis/research/work

**Key requirement:** Demonstrate significant effort and mastery of course concepts

---

## What to Submit

**Folder structure:**
```
final-assignment/
└── your-name/
    ├── README.md           # Documentation
    ├── code/               # Implementation
    │   ├── main.py
    │   ├── src/
    │   └── requirements.txt  # If additional packages
    ├── slides.md           # Marp presentation
    └── assets/             # Screenshots, images
```

**Deliverables:**
1. **Working code** (must run!)
2. **Documentation** (README with setup/usage)
3. **Presentation slides** (Marp format)

---

## Requirements

### 1. Individual Ideas (30%)
Original contribution, creative problem-solving, goes beyond basics

### 2. Code Quality (40%)
**Must run on instructor's machine!**  
Organization, error handling, demonstrates course concepts

### 3. Documentation (30%)
Clear README, setup/usage instructions, presentation

---

## Code Must Run!

**Critical requirement:**

✓ Use existing course dependencies  
✓ OR include updated `requirements.txt`  
✓ Test in fresh virtual environment before submission  
✓ Document any setup steps clearly  

❌ Don't assume instructor has specific tools installed  
❌ Don't use obscure packages without documentation  

**Test procedure:**
```bash
python -m venv test_env
test_env\Scripts\activate
pip install -r requirements.txt
python main.py  # Must work!
```

---

## Appropriate Complexity

**Good examples:**
- Interactive FEM viewer with deformation, clipping, export
- Parallel data processing with progress tracking
- Time-series dashboard with filtering
- 3D mesh comparison with difference visualization

**Too simple:** Single plot script, basic calculator

**Too ambitious:** Complete FEM solver, large ML framework

---

## Timeline

**Now - January:** Use sessions for development, ask questions, test regularly

**January 28, 23:59:** PR deadline - all code, docs, slides complete

**Last January Session:** Present (5-8 min), live demo/video, Q&A

---

## Grading Criteria Summary

**Must Have:**
✓ Runs without errors  
✓ Clear documentation  
✓ Significant effort evident  
✓ Uses course concepts appropriately  

**Nice to Have:**
✓ Solves real problem elegantly  
✓ Clean, maintainable code  
✓ Good performance  
✓ Impressive presentation  

**Remember:** Better to do one thing really well than many things poorly!

---

## Tips for Success

1. **Start early** - don't underestimate time needed
2. **Keep it focused** - polish over scope
3. **Test in clean environment** before submission
4. **Commit regularly** - not just once at end
5. **Ask questions** during January sessions
6. **Document as you go** - easier than at end
7. **Practice presentation** - stay within time limit

**Most common mistake:** Assuming code works without testing in fresh environment!

---

## Project Ideas

**Extend FEM Viewer:** Animation, multiple viewports, clipping, export

**Data Processing:** Parallel batch processor, data cleaning tool, format converter

**Visualization:** Custom plotting, 3D trajectories, real-time monitor, comparison tool

---

## Questions?

**Documentation:** https://soberpe.github.io/visdat-course/advanced-topics/final-assignment

**During January sessions:**
- Get feedback on your approach
- Ask technical questions
- Test your code
- Prepare presentation

**Remember:**
- Deadline: January 28, 23:59
- Presentations: Last January session
- This is your chance to showcase what you've learned!

---

# Summary

## Today's Session

**Learned:**
- Build systems (CMake) and when you'll encounter them
- Parallelization strategies (threads vs. processes)
- GIL implications and solutions (multiprocessing, Numba)

**Practice:**
- Qt Workshop - build complete FEM viewer
- Apply GUI concepts from previous session

**Assignment:**
- Individual project with flexible topic
- Due January 28 with presentation

**Next:** January sessions for project work and support

---

# Good Luck!

**Remember:**
- Use Qt Workshop to deepen your GUI skills
- Start thinking about your final project
- January sessions are for YOUR work
- Don't hesitate to ask questions

**Documentation:**
https://soberpe.github.io/visdat-course/

**See you in January!** 🎄🎆🚀

