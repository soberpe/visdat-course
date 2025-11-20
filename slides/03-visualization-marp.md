---
marp: true
paginate: true
theme: default
class: lead
---

# Visualization with Matplotlib

- Introduction to matplotlib and its role in Python
- Design principles for effective plots
- Typical workflows and practical examples
- Integration with pandas
- Best practices and common pitfalls
<!--
Welcome to the lecture on visualization with matplotlib. This session explores the motivation for data visualization, key design principles, and practical usage of matplotlib in scientific data analysis.
-->
---

# Overview

- Why visualize data?
- What is matplotlib?
- Where does it fit in the Python ecosystem?
- How does it support data analysis?
---

# Why Visualize Data?

- Makes patterns and trends visible
- Supports exploration and hypothesis testing
- Communicates results clearly
- Helps avoid misinterpretation of raw numbers
---

# What is Matplotlib?

- The standard Python library for 2D plotting
- Flexible and widely used in science and engineering
- Foundation for other libraries (pandas, seaborn)
- Supports many chart types and customizations
<!--
Define matplotlib and its importance in the Python data ecosystem.
-->
---

# Where Does Matplotlib Fit?

- Integrates with pandas for tabular data
- Works with numpy for numerical analysis
- Used in Jupyter notebooks and scripts
- Basis for more advanced or interactive tools
<!--
Show how matplotlib connects with other Python tools and workflows.
-->
---

# How Does Matplotlib Support Data Analysis?

- Enables quick exploration with simple plots
- Provides control for publication-quality figures
- Allows customization for clarity and accessibility
- Facilitates reproducible workflows
---

# Why Use Matplotlib?

- Turns raw data into clear graphics
- Reveals patterns, trends, and relationships
- Supports hypothesis testing and sharing results
- Widely adopted and flexible
<!--
Emphasize the motivation for using matplotlib: making data visible and actionable.
-->
---

# Matplotlib Architecture

## Figure, Axes, Artist
- Figure: overall window or page
- Axes: coordinate system and plotting area
- Artist: any visible element (lines, text, legend)
- Hierarchical structure enables complex layouts
<!--
Explain the core objects in matplotlib and how they relate to each other. Use a diagram if possible.
-->
---

# API Styles: Pyplot vs. OO

- Pyplot: quick, stateful, interactive
- Object-Oriented (OO): recommended for scripts and complex layouts
- Choose one style per workflow
- Avoid mixing styles to prevent confusion
<!--
Clarify the difference between the two APIs and why the OO style is preferred for maintainable code.
-->
---

# Pyplot Example

## Quick Line Plot
```python
import matplotlib.pyplot as plt
plt.plot([0, 1, 2, 3], [0, 1, 4, 9])
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Quick Line Plot')
plt.show()
```
---

# Object-Oriented Example

## Controlled Layout
```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [0, 1, 4, 9], marker='o')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Line Plot (OO)')
fig.tight_layout()
plt.show()
```
---

# Typical Plot Types

- Line plot: trends over time or variable
- Scatter plot: relationships between variables
- Bar chart: compare categories
- Histogram: show distributions
- Multiple subplots: compare views side by side

---

# Example: Scatter Plot

```python
import matplotlib.pyplot as plt
x = [1, 2, 3, 4]
y = [4, 5, 6, 7]
plt.scatter(x, y, color='red')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter Plot')
plt.show()
```

---

# Example: Multiple Subplots

```python
import matplotlib.pyplot as plt
import numpy as np
fig, axs = plt.subplots(2, 2, figsize=(8, 6))
x = np.linspace(0, 10, 100)
axs[0, 0].plot(x, np.sin(x))
axs[0, 0].set_title('Sine')
axs[0, 1].plot(x, np.cos(x))
axs[0, 1].set_title('Cosine')
axs[1, 0].plot(x, np.tan(x))
axs[1, 0].set_title('Tangent')
axs[1, 1].plot(x, -np.sin(x))
axs[1, 1].set_title('Negative Sine')
fig.tight_layout()
plt.show()
```
<!--
Demonstrate how to compare multiple views in one figure using subplots.
-->
---

# Design Principles

- Clarity: make the message obvious
- Accuracy: avoid misleading scales
- Aesthetics: support understanding
- Accessibility: use colorblind-friendly palettes
- Label axes, units, and add legends
<!--
Discuss what makes a visualization effective and trustworthy. Use examples of good and bad design.
-->
---

# Matplotlib in Data Analysis

- Used in Jupyter notebooks for exploration
- Used in scripts for automation and publication
- Plots display automatically in notebooks
- Always call plt.show() in scripts
- Save figures with plt.savefig()

---

# Integration with Pandas

- DataFrames have built-in plotting methods
- Use matplotlib as backend
- Quick exploration with df.plot()
- Advanced customization with returned Axes
```python
import pandas as pd
import matplotlib.pyplot as plt
df = pd.DataFrame({'x': [0, 1, 2, 3], 'y': [0, 1, 4, 9]})
ax = df.plot(x='x', y='y', kind='line', marker='o')
ax.set_title('Line Plot from DataFrame')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.tight_layout()
plt.show()
```

---

# Common Pitfalls

- Mixing pyplot and OO styles
- Forgetting plt.show() in scripts
- Overlapping labels and titles
- Poor color choices
- Not labeling axes

---

# Recap

- Matplotlib is essential for scientific visualization in Python
- Understand the architecture: Figure, Axes, Artist
- Choose the right API style for your workflow
- Apply design principles for effective plots
- Integrate with pandas for data analysis
- Avoid common pitfalls
