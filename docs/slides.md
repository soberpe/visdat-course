---
title: Slides
---

# Slides

The slide decks of the lectures, straight from the browser. Use the arrow keys
or click to move through a deck, and press <kbd>F</kbd> for full screen.

| Session | Deck | Covers |
|---|---|---|
| 1 | [Programming Fundamentals & Tools](pathname:///decks/01-fundamentals-and-tools.html) | Organisation, paradigms, C++ and Python, Git |
| 2 | [Environment & Kickoff](pathname:///decks/02-environment-and-kickoff.html) | Both repositories, Python 3.13, virtual environment, VS Code, kickoff assignment |
| 3 | [Programming Basics](pathname:///decks/03-programming-basics.html) | Declaration and assignment, references and pointers, scope, classes |
| 4 | [Data Processing](pathname:///decks/04-data-processing.html) | pandas, data quality, calibration, integration, HDF5 |
| 6, 7 | [Visualization](pathname:///decks/06-visualization.html) | Matplotlib, colour maps, VTK, meshio, PyVista |
| 10 | [User Interfaces](pathname:///decks/10-user-interfaces.html) | Qt, PyQt6, signals and slots, PyVista in Qt |
| 12 | [Build Systems & Parallelization](pathname:///decks/12-advanced-topics.html) | CMake, the GIL, multiprocessing, Numba, final assignment |

The number of a deck is the session it belongs to. The sessions in between
are workshops and work sessions, which are described in the script.

:::note The slides are not the script
A deck carries a lecture. It shows the pictures, the code that gets typed live
and the questions that get asked. The complete explanation is in the chapters of
this site, and that is where you look things up afterwards.
:::

## The sources

Every deck is a Markdown file in `slides/` in the course repository, written for
[Marp](https://marp.app/). That is the same tool you use for your own
presentation in the kickoff assignment.

To work with them locally:

1. Open the course repository as a folder in VS Code
2. Install the **Marp for VS Code** extension
3. Open a deck and start the preview with <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd>

The theme is registered in the repository, so the preview looks exactly like the
published version without any further setup.

:::tip Why Markdown for slides
A deck in Markdown can be diffed, reviewed and versioned like code. You can see
what changed between two lectures, and a correction is a two line commit instead
of a new file called `lecture3_final_v2.pptx`.
:::
