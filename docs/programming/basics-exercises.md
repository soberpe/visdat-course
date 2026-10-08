---
title: Programming Basics Exercises
---

# Programming Basics Exercises

These exercises go with the slide deck *Programming Basics*. Most of them are
short pieces of code with one question: what does it print?

Work through each one in three steps.

1. **Predict.** Read the code and write down what you expect, before running
   anything.
2. **Run.** Paste it into a Python file or a terminal and compare.
3. **Explain.** If your prediction was wrong, find the line where your mental
   model and Python disagree. That line is the actual lesson.

Open the solution only after the third step. A wrong prediction that you can
explain afterwards teaches more than a right one you guessed.

## Names and Objects

### Exercise 1: Rebinding

```python
speed = 50
limit = speed
speed = 80
print(limit)
```

<details>
<summary>Solution</summary>

It prints `50`. `limit = speed` attaches the name `limit` to the object `50`.
`speed = 80` moves the name `speed` to a new object. `limit` still refers to
`50`.

</details>

### Exercise 2: One List, Two Names

```python
readings = [0.1, 0.2]
backup = readings
readings.append(0.3)
readings = [9.9]
print(backup)
```

<details>
<summary>Solution</summary>

It prints `[0.1, 0.2, 0.3]`. `backup = readings` does not copy the list, both
names refer to the same one. `append` changes that list, so `backup` sees the
`0.3`. The last assignment moves only the name `readings` to a new list, and
`backup` keeps referring to the old one.

A real copy is `readings.copy()`.

</details>

### Exercise 3: Strings Cannot Change

```python
name = "accel"
alias = name
alias += "_x"
print(name, alias)
```

<details>
<summary>Solution</summary>

It prints `accel accel_x`. Strings are immutable. `alias += "_x"` cannot change
the string object, so it creates a new string and attaches `alias` to it.
`name` still refers to the original. Lists behave differently, because `+=` on
a list changes the list itself.

</details>

## Functions

### Exercise 4: Changing the Input or Returning a New Object

```python
def scale(values, factor):
    for i in range(len(values)):
        values[i] = values[i] * factor
    return values

def scale_copy(values, factor):
    return [v * factor for v in values]

data = [1.0, 2.0]
result = scale_copy(data, 10)
scale(data, 2)
print(data, result)
```

<details>
<summary>Solution</summary>

It prints `[2.0, 4.0] [10.0, 20.0]`. `scale_copy` builds a new list and leaves
its input alone. `scale` writes into the list it received, which is the
caller's list `data`. Returning `values` at the end does not change that: the
damage is already done.

Functions that return a new object and leave their input unchanged are easier
to reason about. pandas follows this pattern almost everywhere.

</details>

### Exercise 5: The Default Value That Remembers

```python
def log(value, history=[]):
    history.append(value)
    return history

print(log(1))
print(log(2))
```

<details>
<summary>Solution</summary>

It prints `[1]` and then `[1, 2]`. A default value is created once, when the
`def` statement runs, not at every call. All calls without a second argument
share the same list, and it keeps growing.

The standard fix uses `None` as the default:

```python
def log(value, history=None):
    if history is None:
        history = []
    history.append(value)
    return history
```

</details>

### Exercise 6: A Grid That Is Not One

```python
grid = [[0] * 3] * 2
grid[0][0] = 1
print(grid)
```

<details>
<summary>Solution</summary>

It prints `[[1, 0, 0], [1, 0, 0]]`. `[row] * 2` repeats the reference to the
inner list, it does not copy the list. Both rows are the same object.

A list comprehension creates a new inner list for every row:

```python
grid = [[0] * 3 for _ in range(2)]
```

For numerical grids, use a NumPy array instead: `np.zeros((2, 3))`.

</details>

### Exercise 7: Two Variables With One Name

```python
offset = 0.25

def calibrate(raw):
    offset = 0.0
    return raw - offset

print(calibrate(1.0), offset)
```

<details>
<summary>Solution</summary>

It prints `1.0 0.25`. The assignment inside the function creates a local name
`offset`, which hides the global one while the function runs. The global
`offset` is never touched.

This is called shadowing. It is legal, and it is a common source of confusion.
Give local variables names that do not collide with global ones.

</details>

## Classes

### Exercise 8: Shared Without Asking

```python
class Logger:
    entries = []

    def __init__(self, name):
        self.name = name

    def log(self, text):
        self.entries.append(f"{self.name}: {text}")

a = Logger("imu")
b = Logger("wheel")
a.log("started")
print(b.entries)
```

<details>
<summary>Solution</summary>

It prints `['imu: started']`. `entries` is defined in the class body, not in
`__init__`. That makes it a class attribute: one list, shared by every object
of the class. `self.name` is an instance attribute, each object has its own.

The fix is to create the list per object, in `__init__`:

```python
class Logger:
    def __init__(self, name):
        self.name = name
        self.entries = []

    def log(self, text):
        self.entries.append(f"{self.name}: {text}")
```

</details>

### Exercise 9: Calibrating a Sensor

Write a class `Sensor` with the attributes `name`, `unit` and `offset`, and two
methods.

- `zero(self, values)` sets `offset` to the mean of a list of values.
- `calibrate(self, value)` returns `value` minus `offset`.

Then use it on these readings of a longitudinal acceleration sensor on a
motorcycle. The first list was recorded while the bike stood still, so the
true value there is zero. Zero the sensor on that list, print the offset, and
print every reading of the second list next to its calibrated value.

```python
at_rest = [0.27, 0.22, 0.29, 0.24, 0.26]
riding = [1.85, 2.40, 0.31, -3.75, -5.10]
```

<details>
<summary>Solution</summary>

```python
class Sensor:
    def __init__(self, name, unit, offset=0.0):
        self.name = name
        self.unit = unit
        self.offset = offset

    def zero(self, values):
        self.offset = sum(values) / len(values)

    def calibrate(self, value):
        return value - self.offset

at_rest = [0.27, 0.22, 0.29, 0.24, 0.26]
riding = [1.85, 2.40, 0.31, -3.75, -5.10]

accel = Sensor("accel_x", "m/s²")
accel.zero(at_rest)
print(f"offset: {accel.offset:.3f} {accel.unit}")

for raw in riding:
    print(f"{raw:6.2f} -> {accel.calibrate(raw):6.2f}")
```

The offset comes out at 0.256 m/s², and every calibrated value is that much
smaller than the raw one. The sensor reported an acceleration while the bike
stood still, and the calibration removes exactly that.

In the data processing session, the same idea is applied to a whole column of
a real recording at once, with pandas.

</details>

## pandas

This exercise uses pandas, which is introduced in the data processing session.
Come back to it afterwards.

### Exercise 10: Which DataFrame Changed?

```python
import pandas as pd

df = pd.read_csv("data/motorcycle_ride.csv")
work = df
work = work.dropna()
df["speed_ms"] = df["speed_kmh"] / 3.6
print("speed_ms" in work.columns, len(df) == len(work))
```

<details>
<summary>Solution</summary>

It prints `False False`. `work = df` makes a second name for the same
DataFrame, but `dropna()` returns a new DataFrame, and `work = work.dropna()`
moves the name `work` to it. From that line on, the two names refer to
different objects. The new column ends up only in `df`, and `work` has fewer
rows because the rows with missing values are gone.

Remove the `dropna` line and run it again. Now both names refer to one object,
and it prints `True True`.

</details>

## C++

These exercises need a C++ compiler. In Visual Studio, open the *Developer
Command Prompt*, save the code as `exercise.cpp` and compile it with
`cl /EHsc exercise.cpp`.

### Exercise 11: Copy or Reference

```cpp
#include <iostream>
#include <vector>

void add(std::vector<double> values, double v) { values.push_back(v); }
void add_ref(std::vector<double>& values, double v) { values.push_back(v); }

int main() {
    std::vector<double> data{1.0};
    add(data, 2.0);
    add_ref(data, 3.0);
    std::cout << data.size() << "\n";
}
```

<details>
<summary>Solution</summary>

It prints `2`. `add` takes its parameter by value, so it appends to a copy that
disappears when the function returns. `add_ref` takes a reference and appends
to `data` itself. The vector ends up as `{1.0, 3.0}`.

In Python, both functions would change the caller's list. In C++, the signature
decides, and the `&` is the whole difference.

</details>

### Exercise 12: Following a Pointer

```cpp
#include <iostream>

int main() {
    int a = 1;
    int b = 2;
    int* p = &a;
    *p = 10;
    p = &b;
    *p = 20;
    std::cout << a << " " << b << "\n";
}
```

<details>
<summary>Solution</summary>

It prints `10 20`. `*p = 10` writes through the pointer into `a`. `p = &b`
changes the pointer itself, it now holds the address of `b`, and `*p = 20`
writes into `b`.

A reference could not do the second step. Once bound to `a`, it stays bound to
`a`.

</details>
