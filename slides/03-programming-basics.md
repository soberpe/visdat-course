---
marp: true
theme: visdat
paginate: true
footer: "FH OÖ Wels · Visualisierung & Datenaufbereitung"
---

<!-- _class: title -->

# Programming Basics

## The words we use for the rest of the semester

Lecture 3 · Stefan Oberpeilsteiner

<!--
A deliberate step back before the data. Declaration, assignment,
reference, object: these words come up in every later block, in pandas, in
Qt, in the error messages. This part makes sure they mean the same thing to
everyone in the room.

The slides show C++ and Python side by side. C++ makes visible what Python
does quietly, and that is the reason to look at both.
-->

---

# Today

1. **Names and values**: declaration, definition, initialisation, assignment
2. **References and pointers**: when two names share one object
3. **Functions and scope**: where a name lives, and for how long
4. **Classes and objects**: state and operations, kept together

<p class="note">The details are in the script: the C++ and Python chapters. Exercises with solutions: Programming Basics Exercises.</p>

---

<!-- _class: ask -->

# What happens when Python runs `x = 5`?

<!--
Worth answering before reading on, in your own words. The common answer is
"x gets the value 5", and in C++ that would be right. In Python, something
else happens, and the next slides are about the difference.
-->

---

<!-- _class: section -->

# Names and values

## Four words for what looks like one line

---

# C++: four different things

```cpp
extern int count;        // declaration: this name exists, somewhere
int count;               // definition: here is the memory for it
int total = 0;           // definition with initialisation
total = 5;               // assignment: a new value in the same memory

double area(double r);                            // declaration
double area(double r) { return 3.14159 * r * r; } // definition
```

Every definition is also a declaration. The compiler needs a declaration
before a name is used. The linker needs exactly one definition.

<!--
The distinction matters in practice as soon as a program has more than one
file. Header files (.h) contain declarations, source files (.cpp) contain the
definitions. "undefined reference" from the linker means: declared, but never
defined. "multiple definition" means: defined twice.

One more trap: a local variable defined without initialisation, int x; inside
a function, holds whatever was in that memory before. Initialise always.
-->

---

# Python: no declarations at all

```python
x = 5            # an int object 5 exists, and the name x refers to it
x = "five"       # the same name now refers to a str object
type(x)          # str: the type belongs to the object, not to the name

def area(r):     # def runs like any statement: it creates a function object
    return 3.14159 * r * r
```

<div class="boxes">
<div><b>C++</b>A variable is a box of a fixed type. Assignment puts a new value into the box.</div>
<div><b>Python</b>A name is a label. Assignment attaches the label to an object.</div>
</div>

<!--
Type hints like x: int = 5 exist in Python, but they are notes for tools and
readers. Python does not enforce them at runtime.

The label picture explains almost everything on the following slides. Keep it
in mind: a name points to an object, and several names can point to the same
one.
-->

---

# Predict the output

<div class="timer">
<input type="checkbox" id="timer-pb-1">
<label for="timer-pb-1"><span class="tape tens"><b>6</b><b>5</b><b>4</b><b>3</b><b>2</b><b>1</b><b>0</b></span><span class="tape ones"><b>0</b><b>9</b><b>8</b><b>7</b><b>6</b><b>5</b><b>4</b><b>3</b><b>2</b><b>1</b><b>0</b></span></label>
<div class="bar"></div><span class="hint">start / reset</span>
</div>

```python
x = 5
y = x
x = 7
print(y)
```

Write your answer down before you run it.

<!--
The answer is 5. y = x attaches the label y to the object 5. x = 7 moves the
label x to a new object, and y still points to 5.

Here Python and C++ give the same result, so the label picture and the box
picture seem to agree. The next question is where they part.
-->

---

<!-- _class: section -->

# References and pointers

## When two names share one object

---

# Predict the output

<div class="timer">
<input type="checkbox" id="timer-pb-2">
<label for="timer-pb-2"><span class="tape tens"><b>6</b><b>5</b><b>4</b><b>3</b><b>2</b><b>1</b><b>0</b></span><span class="tape ones"><b>0</b><b>9</b><b>8</b><b>7</b><b>6</b><b>5</b><b>4</b><b>3</b><b>2</b><b>1</b><b>0</b></span></label>
<div class="bar"></div><span class="hint">start / reset</span>
</div>

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

<!--
The answer is [1, 2, 3, 4]. b = a does not copy the list. It attaches a second
label to the same list, and append changes that one list.

The difference to the previous question: x = 7 attached a label to a new
object. append changes the object itself. Rebinding and mutating are two
different operations, and they look similar in code.
-->

---

# One object, two names

```python
a = [1, 2, 3]
b = a              # a second name for the same list
b.append(4)        # changes the list, visible through a as well
b = [9]            # rebinds b only, a is untouched
c = a.copy()       # a new list with the same content

print(a, b, c)     # [1, 2, 3, 4] [9] [1, 2, 3, 4]
print(a is c)      # False: equal content, different objects
```

**Mutating** changes the object, every name sees it. **Rebinding** moves one
name, the others stay where they were.

<!--
Why did the integers on the earlier slide behave like values? Because an int
cannot be changed at all, it is immutable. y += 1 cannot modify the object 5,
so it creates a new object 6 and rebinds y. Strings and tuples are immutable
too. Lists, dictionaries, NumPy arrays and DataFrames are mutable.

== asks whether two objects have equal content. is asks whether two names
point to the same object.
-->

---

# Functions receive references

```python
def add_reading(readings, value):
    readings.append(value)     # mutates the caller's list

def reset(readings):
    readings = []              # rebinds the local name only

log = [0.1]
add_reading(log, 0.2)
reset(log)
print(log)                     # [0.1, 0.2]
```

A parameter is a new name for the object the caller passed in. Mutating it
reaches the caller. Rebinding it does not.

<!--
This is the most common source of "my function changed my data and I did not
ask it to". A function that should not change its input either works on a
copy, or returns a new object and leaves the input alone. pandas follows the
second pattern almost everywhere.
-->

---

# C++ makes the choice explicit

```cpp
void by_value(int x)      { x = 99; }   // works on a copy
void by_reference(int& x) { x = 99; }   // x is another name for a
void by_pointer(int* p)   { *p = 99; }  // p holds the address of a

int a = 1;
by_value(a);       // a is still 1
by_reference(a);   // a is now 99
a = 1;
by_pointer(&a);    // a is 99 again
```

In C++ the signature says what a function may do to its argument. In Python
the type of the object decides it.

<!--
Large objects in C++ are usually passed as const reference, for example
const std::vector<double>& data. No copy is made, and the compiler forbids the
function to change the data. That is the explicit version of what pandas does
by convention.
-->

---

# What a pointer is

<div class="cols">
<div>

```cpp
int a = 99;
int* p = &a;   // & takes the address
*p = 5;        // * follows it: a is 5
int& r = a;    // r is a second name for a
r = 7;         // a is 7
```

</div>
<div>

| Name | Address | Content |
|---|---|---|
| `a` | `0x7ffc10` | `7` |
| `p` | `0x7ffc18` | `0x7ffc10` |

</div>
</div>

A **pointer** is a variable that holds an address. It can be changed to point
elsewhere, or to nothing (`nullptr`). A **reference** is bound once, at its
creation, and stays an alias for that one object.

<!--
The addresses are made up, the principle is not. A pointer is just a number
that happens to be a memory address, and *p means: go to that address.

In Python, every name behaves like a pointer that is followed automatically.
There is no address arithmetic and no way to reach freed memory, which removes
a whole class of bugs, at the price of control over memory layout. That
control is one reason the fast libraries under Python are written in C and
C++.
-->

---

# Why this matters in pandas

```python
df = pd.read_csv("data/motorcycle_ride.csv")

clean = df                  # no copy: two names, one DataFrame
clean["speed_kmh"] = 0      # df has changed as well

clean = df.copy()           # an independent copy

df.dropna()                 # returns a new DataFrame, df is unchanged
df = df.dropna()            # rebinding the name keeps the result
```

<p class="note">Most pandas methods return a new object. If you do not assign the result, nothing happened.</p>

<!--
Both mistakes on this slide are among the most frequent ones in data
processing code, and both are silent: no error, just a wrong result. The data
processing lecture uses exactly these operations.
-->

---

<!-- _class: section -->

# Functions and scope

## Where a name lives, and for how long

---

# Scope

<div class="cols">
<div>

```python
offset = 0.25                  # global

def calibrate(value):
    corrected = value - offset # local
    return corrected

calibrate(1.0)
print(corrected)               # NameError
```

</div>
<div>

```cpp
for (int i = 0; i < 3; ++i) {
    double sq = i * i;
}
// i and sq do not exist here
```

</div>
</div>

A name defined inside a function, or in C++ inside any block `{ }`, exists only
there. When the function returns, its local names are gone.

<!--
Python looks up a name in a fixed order: local, then the enclosing function,
then the module (global), then the built-ins. Reading a global from inside a
function works, as offset shows.

C++ is stricter: every pair of braces opens a new scope, including the body of
a loop or an if. Python does not have block scope, a variable defined inside a
loop is still visible after it.
-->

---

# Predict the output

<div class="timer">
<input type="checkbox" id="timer-pb-3">
<label for="timer-pb-3"><span class="tape tens"><b>6</b><b>5</b><b>4</b><b>3</b><b>2</b><b>1</b><b>0</b></span><span class="tape ones"><b>0</b><b>9</b><b>8</b><b>7</b><b>6</b><b>5</b><b>4</b><b>3</b><b>2</b><b>1</b><b>0</b></span></label>
<div class="bar"></div><span class="hint">start / reset</span>
</div>

```python
count = 0

def increment():
    count += 1

increment()
print(count)
```

<!--
Neither 0 nor 1: the call raises UnboundLocalError. An assignment anywhere in
a function makes the name local in the whole function. count += 1 reads count
before it was assigned locally, and fails.

There is a keyword, global, that makes this work. Better is to avoid the
situation: pass the value in and return the new one. A function whose result
depends only on its arguments can be tested, reused and understood on its own.
-->

---

<!-- _class: section -->

# Classes and objects

## State and the operations on it, kept together

---

# A class bundles state and operations

```python
class Sensor:
    def __init__(self, name, unit, offset=0.0):
        self.name = name            # attributes: the state
        self.unit = unit
        self.offset = offset

    def calibrate(self, raw):       # method: an operation on that state
        return raw - self.offset

imu = Sensor("accel_x", "m/s²", offset=0.25)
wheel = Sensor("speed", "km/h")
print(imu.calibrate(1.0), wheel.calibrate(50.0))   # 0.75 50.0
```

The **class** is the blueprint. Each **object** has its own attributes.

<!--
__init__ runs once, when an object is created, and sets up its attributes.

self is the object a method was called on. imu.calibrate(1.0) is a short
form of Sensor.calibrate(imu, 1.0). That is why every method lists self as its
first parameter, and why attributes are always written as self.something.

The two objects share the methods, but not the attributes: imu has an offset
of 0.25, wheel has 0.0.
-->

---

# Predict the output

<div class="timer">
<input type="checkbox" id="timer-pb-4">
<label for="timer-pb-4"><span class="tape tens"><b>6</b><b>5</b><b>4</b><b>3</b><b>2</b><b>1</b><b>0</b></span><span class="tape ones"><b>0</b><b>9</b><b>8</b><b>7</b><b>6</b><b>5</b><b>4</b><b>3</b><b>2</b><b>1</b><b>0</b></span></label>
<div class="bar"></div><span class="hint">start / reset</span>
</div>

```python
imu = Sensor("accel_x", "m/s²", offset=0.25)
backup = imu
backup.offset = 0.0
print(imu.calibrate(1.0))
```

<!--
The answer is 1.0. backup = imu is the same situation as b = a with the list:
one object, two names. Setting the offset through backup changes the one and
only sensor object.

Objects of your own classes follow exactly the same rules as lists. There is
nothing special about them.
-->

---

# The same class in C++

```cpp
class Sensor {
public:
    Sensor(std::string name, double offset)
        : name_(name), offset_(offset) {}

    double calibrate(double raw) const { return raw - offset_; }

private:
    std::string name_;
    double offset_;
};

Sensor imu("accel_x", 0.25);
double a = imu.calibrate(1.0);   // 0.75
```

<!--
Three things Python does not write down. The constructor has the name of the
class, and the list after the colon initialises the attributes. private means
that only the class itself can touch name_ and offset_. const after calibrate
promises that the method does not change the object, and the compiler checks
the promise.

Python has no private. A leading underscore, self._offset, is the convention
for "internal, do not touch from outside".

And one difference to Python: Sensor backup = imu; in C++ makes a copy. Two
objects, unless you write Sensor& backup = imu.
-->

---

# Inheritance, in one slide

```python
class Thermocouple(Sensor):
    def __init__(self, name, offset=0.0):
        super().__init__(name, "degC", offset)

    def to_kelvin(self, raw):
        return self.calibrate(raw) + 273.15

coolant = Thermocouple("coolant", offset=1.5)
print(coolant.unit, coolant.to_kelvin(90.0))   # degC 361.65
```

A subclass gets everything its base class has, and adds or changes what it
needs.

<p class="note">You will meet this again in Qt: every window you build is a subclass of <code>QMainWindow</code> or <code>QWidget</code>.</p>

<!--
super().__init__(...) calls the constructor of the base class, so the
attributes name, unit and offset are set up the same way as for every other
sensor. calibrate is inherited unchanged and used inside to_kelvin.

Inheritance is a strong tool and easy to overuse. A good test: the sentence
"a Thermocouple is a Sensor" has to be true.
-->

---

# You already use objects

```python
import pandas as pd

df = pd.read_csv("data/motorcycle_ride.csv")

type(df)            # pandas.core.frame.DataFrame: an object of a class
df.shape            # an attribute: part of its state
df.describe()       # a method: returns a new DataFrame
df["speed_kmh"]     # a Series, an object of another class
```

`DataFrame` is a class, written by other people. Everything on this page
works the same way for it as for the `Sensor` class.

<!--
This is the bridge to the data processing lecture. The pandas documentation is
organised exactly like this: a page per class, and on it the attributes and
the methods. Once that structure is clear, the documentation becomes
navigable.
-->

---

# The words, once more

| Word | C++ | Python |
|---|---|---|
| Declaration | Name and type, no memory yet | Does not exist |
| Definition | Memory, or a function body | `def`, `class`, first assignment |
| Assignment | New value into existing memory | Name attached to an object |
| Reference | Alias, bound once, explicit `&` | Every name |
| Pointer | Holds an address, explicit `*` | No equivalent you see |
| Object | Instance of a class | Everything, even `5` |

---

# Hands on, the rest of today

1. **Kickoff assignment** first: your branch, your folder, your commits
2. **Programming Basics Exercises** on the course site: predict first, then
   run, then explain the difference
3. **The `Sensor` class** on the motorcycle ride, the last exercise

Before you leave, your kickoff pull request is open, even if the work in it is
not finished yet.

<!--
An open pull request is the checkpoint, not a finished one. It proves that
the whole chain works: clone, branch, commit, push, automatic check. Whatever
fails in that chain is far easier to fix today than on the evening before the
deadline.

In the exercises, a wrong prediction you can explain afterwards is worth more
than a right one you guessed.
-->

---

# Next time

Data formats and processing: CSV, Excel, HDF5, and pandas on the log of a
motorcycle ride.

```python
import pandas as pd

df = pd.read_csv("data/motorcycle_ride.csv")
df.describe()
```

<p class="note">The data processing session starts with data, not with installation.</p>
