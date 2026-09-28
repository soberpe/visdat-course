---
title: Slides
---

# Slides

The slide decks of the lectures, straight from the browser. Use the arrow keys
or click to move through a deck, and press <kbd>F</kbd> for full screen.

| | Deck | Covers |
|---|---|---|
| 1 | [Programming Fundamentals & Tools](pathname:///decks/01-fundamentals-and-tools.html) | Organisation, paradigms, C++ and Python, Git, environment |
| 2 | [Data Processing](pathname:///decks/02-data-processing.html) | pandas, data quality, calibration, integration, HDF5 |
| 3 | [Visualization](pathname:///decks/03-visualization.html) | Matplotlib, colour maps, VTK, meshio, PyVista |
| 4 | [User Interfaces](pathname:///decks/04-user-interfaces.html) | Qt, PyQt6, signals and slots, PyVista in Qt |
| 5 | [Build Systems & Parallelization](pathname:///decks/05-advanced-topics.html) | CMake, the GIL, multiprocessing, Numba, final assignment |

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
