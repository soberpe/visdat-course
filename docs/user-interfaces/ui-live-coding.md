---
title: "Live Coding: From Script to Window"
---

# Live Coding: From Script to Window

This page is the code of the lecture on user interfaces. The lecture builds one
small application in six steps, from an empty window to a 3D view with a slider
beside it. Every step is the complete file, so you can copy it, run it and
compare it with the previous one. The lines that are new in a step are
highlighted.

Along the way the code touches the Python from the programming basics session
again: names and references, scope, classes and inheritance, and functions as
objects. Each step says which of them is at work.

:::tip How to follow along
Create one file, for example `ui_demo.py`, in your submissions repository and
activate your virtual environment. At every step, replace the whole content of
the file with the code of that step and run it. Everything you need is in
`requirements.txt`, so there is nothing to install.
:::

## Step 1: The smallest application that works

```python title="ui_demo.py"
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication([])

window = QWidget()
window.setWindowTitle("First Qt App")
window.resize(400, 300)
window.show()

app.exec()
```

Four things happen here: an application object is created, a window is created
and configured, the window is shown, and `app.exec()` hands control to Qt.

**Try this:** delete the last line and run the file again. The window flashes up
and disappears at once. The script simply reaches its end, Python exits, and the
window goes with it. `app.exec()` is what keeps the program alive: it starts the
event loop, which waits for clicks and key presses until the last window is
closed.

## Step 2: A layout and a signal

```python title="ui_demo.py" {1-3,6-7,15-24}
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
)


def greet():
    label.setText(f"Hello, {name_input.text()}!")


app = QApplication([])

window = QWidget()
window.setWindowTitle("Greeter")

label = QLabel("Enter your name:")
name_input = QLineEdit()
button = QPushButton("Greet")
button.clicked.connect(greet)

layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(name_input)
layout.addWidget(button)
window.setLayout(layout)

window.show()
app.exec()
```

The layout arranges the widgets from top to bottom and keeps them arranged when
the window is resized. The line `button.clicked.connect(greet)` connects the
signal `clicked` to the function `greet`, which is called on every click.

**The Python behind it:**

- `greet` is passed **without** parentheses. A function is an object like any
  other, and `connect` receives the function itself so that Qt can call it
  later. With parentheses, `greet()` would be called once, right on that line,
  and `connect` would receive its return value `None`. PyQt rejects that with a
  `TypeError`.
- `greet` uses the names `label` and `name_input`, although they appear further
  down in the file. This works because Python looks a name up when the function
  **runs**, not when it is defined. By the time somebody clicks, both names exist
  at module level.

## Step 3: The same application as a class

```python title="ui_demo.py"
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
)


class Greeter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Greeter")

        self.label = QLabel("Enter your name:")
        self.name_input = QLineEdit()
        button = QPushButton("Greet")
        button.clicked.connect(self.greet)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.name_input)
        layout.addWidget(button)

    def greet(self):
        self.label.setText(f"Hello, {self.name_input.text()}!")


if __name__ == "__main__":
    app = QApplication([])
    window = Greeter()
    window.show()
    app.exec()
```

The widgets are the same as in step 2. What changes is where they live: the
window is now a class `Greeter` that inherits from `QWidget`, and everything the
window needs is kept together inside it.

**The Python behind it:**

- `class Greeter(QWidget)` is inheritance. A `Greeter` **is** a `QWidget`, with
  everything a widget can do, plus what we add.
- `super().__init__()` runs the constructor of `QWidget`, which creates the
  actual window on the Qt side. Delete the line and PyQt stops with
  `RuntimeError: super-class __init__() of type Greeter was never called`.
- `self.label` and `self.name_input` are attributes, because `greet` needs them
  later. `button` is only used inside `__init__`, so a local name is enough.
- `connect(self.greet)` passes a **bound method**: the function together with
  the object it belongs to. That is why `greet` can use `self`.
- `if __name__ == "__main__":` runs the block only when the file is started
  directly, not when it is imported from another file.

**Try this:** move the creation of the window into a function.

```python
def open_window():
    window = Greeter()
    window.show()


app = QApplication([])
open_window()
app.exec()
```

No window appears, but the program keeps running. When `open_window` returns,
the local name `window` disappears, nothing else refers to the object any more,
and Python deletes it, together with the window on the screen. The event loop
then waits for a window that no longer exists. Stop the program with the bin
icon in the VS Code terminal.

The button in `__init__` is also held only by a local name, and it survives.
The difference is the layout: `addWidget` gives the button a **parent**, and from
then on the parent keeps it alive. A window without a parent has only its Python
references.

## Step 4: Slow work, and where it belongs

Sooner or later a button starts something that takes time: loading a large
mesh, running a solver, exporting a video. This step first shows what happens
when such work runs directly in a slot, and then moves it to where it belongs.

The work here is a plain Python loop that approximates π from the series
$1/1^2 + 1/2^2 + 1/3^2 + \dots = \pi^2/6$. Fifty million terms take a few
seconds and give π to seven decimal places, so it is real work with a result
you can check.

### 4a: The work in the slot

```python title="ui_demo.py" {1,8-13,25-26,32,37-40}
import math

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
)


def slow_pi(n):
    """Approximate pi from 1/1² + 1/2² + 1/3² + ... = pi²/6."""
    total = 0.0
    for i in range(1, n):
        total += 1.0 / (i * i)
    return math.sqrt(6 * total)


class Greeter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Greeter")

        self.label = QLabel("Enter your name:")
        self.name_input = QLineEdit()
        button = QPushButton("Greet")
        button.clicked.connect(self.greet)
        compute_button = QPushButton("Compute")
        compute_button.clicked.connect(self.compute)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.name_input)
        layout.addWidget(button)
        layout.addWidget(compute_button)

    def greet(self):
        self.label.setText(f"Hello, {self.name_input.text()}!")

    def compute(self):
        self.label.setText("Computing...")
        result = slow_pi(50_000_000)
        self.label.setText(f"pi ≈ {result:.8f}")


if __name__ == "__main__":
    app = QApplication([])
    window = Greeter()
    window.show()
    app.exec()
```

**Try this:** click Compute and try to move the window. It does not move, and
the label never shows "Computing...". It keeps its old text and then jumps
straight to the result. `compute` runs **inside** the event loop from step 1.
`setText` only notes that the label has to be repainted, and the repainting
happens when the event loop gets control back, which is after the computation.

### 4b: The work in its own thread

```python title="ui_demo.py" {3,17-18,20-22,34-35,41,48,50-52,54-57,59,61-62,64-65}
import math

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
)


def slow_pi(n):
    """Approximate pi from 1/1² + 1/2² + 1/3² + ... = pi²/6."""
    total = 0.0
    for i in range(1, n):
        total += 1.0 / (i * i)
    return math.sqrt(6 * total)


class Worker(QObject):
    finished = pyqtSignal(float)    # a signal of our own, carrying the result

    def run(self):
        result = slow_pi(50_000_000)
        self.finished.emit(result)


class Greeter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Greeter")

        self.label = QLabel("Enter your name:")
        self.name_input = QLineEdit()
        button = QPushButton("Greet")
        button.clicked.connect(self.greet)
        self.compute_button = QPushButton("Compute")
        self.compute_button.clicked.connect(self.compute)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.name_input)
        layout.addWidget(button)
        layout.addWidget(self.compute_button)

    def greet(self):
        self.label.setText(f"Hello, {self.name_input.text()}!")

    def compute(self):
        self.label.setText("Computing...")
        self.compute_button.setEnabled(False)

        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.show_result)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self.compute_done)

        self.worker_thread.start()

    def show_result(self, value):
        self.label.setText(f"pi ≈ {value:.8f}")

    def compute_done(self):
        self.compute_button.setEnabled(True)



if __name__ == "__main__":
    app = QApplication([])
    window = Greeter()
    window.show()
    app.exec()
```

The computation now lives in a class of its own, `Worker`, and runs in a second
thread. `compute` only starts it and returns at once, so the event loop keeps
running: the label shows "Computing...", the window can be moved, and the button
stays disabled until the result is there.

**The Python behind it:**

- `finished = pyqtSignal(float)` declares a signal of our own, which carries a
  float. It is defined in the class body, just like the `clicked` signal of a
  button is defined in `QPushButton`.
- The worker never touches the label. It emits `finished` with the result, and
  `show_result` sets the text. Widgets belong to the main thread and may only be
  changed there. A signal sent from one thread to an object in another is
  delivered through the receiver's event loop, so `show_result` runs in the main
  thread, at a moment when the event loop is free.
- `self.worker_thread` and `self.worker` are attributes, not local names. With
  local names, both objects would be deleted as soon as `compute` returns, while
  the thread is still running, and the program ends abruptly without an error
  message. It is the lifetime rule from step 3 again, with a harder consequence.
- The four `connect` lines describe the whole sequence: the thread starts, the
  worker runs, the result goes to the label and stops the thread, and the
  stopped thread enables the button again.

If you close the window while the computation runs, the program ends and the
result is lost. A real application would let the worker stop early, which goes
beyond this step.

:::tip The rule
Anything slow does not belong in a slot. The slot starts the work in a
`QThread`, and the result comes back as a signal. Your final project needs
exactly this pattern as soon as it loads a large mesh.
:::

:::info Threads do not make Python faster
The loop in the worker is not faster than before. Python lets only one thread
execute Python code at a time (the GIL), and switches between the threads every
few milliseconds. That is enough to keep the window responsive, but it is not
parallel computation. How to actually use several cores is the topic of
[Parallelization](../advanced-topics/parallelization.md).
:::

## Step 5: A main window with a 3D view

```python title="ui_demo.py"
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout


class SphereViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sphere Viewer")
        self.resize(1000, 600)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        self.plotter = QtInteractor(central)
        main_layout.addWidget(self.plotter.interactor)

        sphere = pv.Sphere()
        self.plotter.add_mesh(sphere, color="lightblue", show_edges=True)


if __name__ == "__main__":
    app = QApplication([])
    window = SphereViewer()
    window.show()
    app.exec()
```

`QMainWindow` is the frame of a real application, with room for a menu bar, a
tool bar and a status bar. It needs a central widget, and the layout goes onto
that widget. `QtInteractor` is the PyVista plotter you know from the
visualization block, this time as a widget that sits inside your own window.

## Step 6: A slider that changes the mesh

```python title="ui_demo.py" {3,5-6,20-29,32-33,35,37-46}
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QGroupBox, QLabel, QSlider
)


class SphereViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sphere Viewer")
        self.resize(1000, 600)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        controls = QGroupBox("Controls")
        controls_layout = QVBoxLayout(controls)
        self.resolution_label = QLabel()
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(5, 100)
        slider.setValue(20)
        slider.valueChanged.connect(self.update_mesh)
        controls_layout.addWidget(self.resolution_label)
        controls_layout.addWidget(slider)
        controls_layout.addStretch()

        self.plotter = QtInteractor(central)
        main_layout.addWidget(controls)
        main_layout.addWidget(self.plotter.interactor, stretch=3)

        self.update_mesh(slider.value())

    def update_mesh(self, value):
        self.resolution_label.setText(f"Resolution: {value}")
        sphere = pv.Sphere(theta_resolution=value, phi_resolution=value)
        self.plotter.clear()
        self.plotter.add_mesh(sphere, color="lightblue", show_edges=True)
        self.plotter.reset_camera()

    def closeEvent(self, event):
        self.plotter.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = SphereViewer()
    window.show()
    app.exec()
```

The controls on the left and the 3D view on the right share one horizontal
layout, and `stretch=3` gives the view most of the space. Every movement of the
slider emits `valueChanged` with the new value, and `update_mesh` rebuilds the
sphere with that resolution.

**The Python behind it:**

- `update_mesh` is an ordinary method. Qt calls it on every slider movement, and
  the last line of `__init__` calls it once directly, so that the sphere is
  there before anybody touches the slider. A slot is not a special kind of
  function.
- `closeEvent` is never called in our code. `QMainWindow` already has a method
  of that name, and Qt calls it when the window is closed. By defining our own,
  we **override** it, and Qt now calls our version. This is where the plotter
  releases its resources before the window goes away.
- `Qt.Orientation.Horizontal` is an enumeration: a fixed set of named values
  instead of a number whose meaning you would have to remember.
- The f-string in `setText` puts the current value into the label.

**Try this:** drag the slider quickly. The view flickers, because every event
clears the plotter and builds a new mesh. For a change of geometry that keeps
the same mesh, such as an animation, it is better to move the points of the
existing mesh. The lecture slides show both variants, and the
[Qt workshop](qt-workshop) uses them on real FEM data.
