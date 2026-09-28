---
title: Python Overview
---

# Python Overview

## Introduction

Python is a high-level, interpreted programming language that excels in data processing, analysis, and visualization. Its clear syntax, extensive standard library, and rich ecosystem make it an ideal choice for rapid prototyping and data science applications.

## Why Python for Data Processing?

### Advantages

- **Productivity:** Clean, readable syntax accelerates development
- **Rich Ecosystem:** Extensive libraries for data science (NumPy, Pandas, Matplotlib)
- **Interactive Development:** Jupyter notebooks for exploratory analysis
- **Cross-Platform:** Runs on Windows, Linux, macOS
- **Community:** Large, active community with extensive documentation

### Use Cases in This Course

- **Data Analysis:** Processing and cleaning datasets
- **Visualization:** Creating charts, plots, and interactive dashboards
- **Prototyping:** Rapid development of data processing algorithms
- **Automation:** Scripting repetitive data tasks
- **Integration:** Connecting different data sources and formats

## Language Characteristics

Python is an interpreted language with several key features:

- **Dynamic Typing:** Variable types are determined at runtime
- **Indentation-Based:** Code blocks are defined by indentation, not braces
- **Interactive:** Can be run interactively or as scripts
- **Object-Oriented:** Everything is an object

## Basic Syntax

```python
# Comments start with #

# Variables and basic types
integer_var = 42
float_var = 3.14159
string_var = "Hello, Python!"
boolean_var = True

# Print output
print(f"Integer: {integer_var}")
print(f"Float: {float_var}")
print(f"String: {string_var}")
print(f"Boolean: {boolean_var}")

# Multiple assignment
x, y, z = 1, 2, 3
print(f"x={x}, y={y}, z={z}")
```

## Getting Started

### Installation

Download Python 3.8+ from [python.org](https://python.org/)

```bash
# Verify Python installation
python --version
# or
python3 --version
```

### Interactive Mode

```python
# Start Python interpreter
python

# Try some basic operations
>>> 2 + 3
5
>>> "Hello" + " " + "World"
'Hello World'
>>> exit()
```

### Running Scripts

```python
# Create a file: hello.py
print("Hello, Python!")

# Run from command line
python hello.py
```

## Python Philosophy

Python follows the "Zen of Python" principles:

- **Beautiful is better than ugly**
- **Explicit is better than implicit**
- **Simple is better than complex**
- **Readability counts**
- **There should be one obvious way to do it**

You can see the full Zen of Python by typing `import this` in the Python interpreter.

## Development Environment

### Recommended Setup

1. **Python Installation:** Python 3.8 or higher
2. **Code Editor:** VS Code with Python extension
3. **Package Manager:** pip (included with Python)
4. **Virtual Environments:** venv for project isolation

### Virtual Environments

A virtual environment is an isolated Python environment that allows you to install packages independently for each project. This prevents conflicts between different projects that might require different versions of the same package.

#### Understanding Virtual Environments

**Key concepts:**
- A virtual environment is **bound to the specific Python version** used to create it
- Created using `python -m venv`, which uses the Python interpreter that runs the command
- Contains its own Python binary and package installation directory
- **Cannot change Python version** after creation - you must recreate the environment
- Named `.venv` by convention (the leading dot hides it on Unix-like systems)

#### Creating a Virtual Environment (Command Line)

```bash
# Method 1: If Python is in PATH
python -m venv .venv

# Method 2: Using specific Python installation (recommended)
C:\Python313\python.exe -m venv .venv  # Windows
/usr/bin/python3.13 -m venv .venv      # Linux/macOS

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install packages
pip install numpy pandas matplotlib

# Deactivate when done
deactivate
```

#### Creating a Virtual Environment in VS Code (Recommended)

VS Code provides a convenient workflow for creating virtual environments:

1. **Open Command Palette:** `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. **Select:** "Python: Create Environment"
3. **Choose:** "Venv" (not Conda)
4. **Select Python interpreter:** VS Code shows all available Python installations
5. **Select dependencies (optional):** If a `requirements.txt` exists, VS Code offers to install packages

**Interpreter Selection:**
- Click the Python version in the **bottom-right status bar**
- Or use Command Palette: "Python: Select Interpreter"
- VS Code automatically detects `.venv` folders in your workspace

#### Managing Dependencies with requirements.txt

The course repository includes a `requirements.txt` file with all necessary dependencies for the course. This file lists all required packages with their tested versions.

**Install all course dependencies:**
```bash
pip install -r requirements.txt
```

This will install:
- Core scientific libraries (NumPy, Pandas, SciPy)
- Visualization tools (Matplotlib, Seaborn, Plotly)
- 3D visualization (PyVista, meshio)
- Data storage (HDF5, Excel support)
- Additional utilities

**Update requirements.txt (for instructors/contributors):**
```bash
pip freeze > requirements.txt
```

:::tip Best Practices
- **Always use virtual environments** - one per project
- **Use `.venv` as the folder name** - recognized by VS Code and git (add to `.gitignore`)
- **Track dependencies** in `requirements.txt` for reproducibility
- **Recreate, don't reconfigure** - if you need a different Python version, delete `.venv` and create new
- **Activate before installing packages** - ensures packages go into the virtual environment
:::

:::warning Common Mistakes
- Installing packages globally instead of in the virtual environment
- Forgetting to activate the environment before running scripts
- Trying to change Python version by editing configuration files (doesn't work!)
- Not tracking dependencies in `requirements.txt`
:::

### Essential Tools

```bash
# Check pip version
pip --version

# Install packages
pip install numpy pandas matplotlib

# Upgrade pip (recommended)
python -m pip install --upgrade pip
```

## Next Steps

Now that you understand Python's fundamentals, you're ready to explore:

- **[Data Types & Collections](python-data-types)** - Learn about Python's built-in data structures
- **[Control Flow](python-control-flow)** - Master loops, conditions, and functions
- **[Object-Oriented Programming](python-oop)** - Build classes and objects
- **[File Handling](python-file-handling)** - Work with files and data persistence
- **[External Libraries](python-libraries)** - Leverage NumPy, Pandas, and more

Python's simplicity and power make it an excellent choice for data processing tasks throughout this course!