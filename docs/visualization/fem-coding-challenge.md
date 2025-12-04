---
title: FEM Coding Challenge
sidebar_position: 7
---

# FEM Coding Challenge

**Duration:** 3 blocks (3 × 45 minutes)  
**Goal:** Build a simple FEM solver from scratch and understand the fundamentals

---

## Block 4: Pair Programming - 1D Beam FEM (45 min)

### Setup: Find Your Coding Partner (5 min)

Form pairs. You'll switch roles:
- **Driver:** Types the code
- **Navigator:** Reads instructions, catches errors

**Switch every 10 minutes!**

---

### The Problem (Read Together - 5 min)

We're building a **1D bar finite element solver**:

```
Fixed Wall |----Element 1----|----Element 2----| → Force F
           0                 1                 2
         Node 0            Node 1            Node 2
```

**Given:**
- 3 nodes at positions: $x = [0, 1, 2]$ meters
- Material: Steel ($E = 200$ GPa)
- Cross-section: $A = 0.01$ m²
- Boundary: Node 0 is fixed ($u_0 = 0$)
- Load: Force $F = 1000$ N applied at Node 2

**Find:** Displacements $u_1$ and $u_2$

---

### Theory: Element Stiffness Matrix (5 min - Navigator reads aloud)

For a 1D bar element connecting two nodes:

$$
\mathbf{k}_{\text{element}} = \frac{EA}{L} \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}
$$

Where:
- $E$ = Young's modulus [Pa]
- $A$ = Cross-sectional area [m²]
- $L$ = Element length [m]

This 2×2 matrix relates forces to displacements for one element.

---

### Step 1: Setup (Driver types - 5 min)

**Navigator, read these instructions aloud:**

"Import numpy. Create a numpy array for node positions: 0, 1, and 2 meters. Store the number of nodes in a variable."

"Define the material properties: E equals 200 times 10 to the power 9. A equals 0.01."

```python
# Driver: Write this code (Navigator: don't show this, just dictate!)
import numpy as np

# Node positions
nodes = np.array([___])  # Fill in: 0, 1, 2

# Material properties
E = ___  # Young's modulus in Pa
A = ___  # Cross-section in m²
```

---

### Step 2: Element Stiffness Function (Driver types - 5 min)

**Navigator:** "Write a function called stiffness_1d_bar. It takes three parameters: E, A, and L. Inside, calculate k as E times A divided by L. Then create a 2 by 2 numpy array with the pattern: 1, minus 1 in the first row, minus 1, 1 in the second row. Multiply that array by k. Return the result."

**Driver:** Write the function (no peeking at solutions!)

**Switch roles now!**

---

### Step 3: Global Stiffness Matrix (New Driver types - 10 min)

**New Navigator:** "Create a 3 by 3 matrix of zeros called K_global."

"Calculate the length of element 1: node position 1 minus node position 0."

"Call the stiffness function with E, A, and L1 to get k1."

"Add k1 into K_global at positions [0:2, 0:2]."

"Do the same for element 2: nodes 1 to 2."

```python
# Driver: Implement this
K_global = np.zeros((___, ___))  # What size?

# Element 1
L1 = nodes[___] - nodes[___]  # Which nodes?
k1 = stiffness_1d_bar(___, ___, ___)
K_global[___:___, ___:___] += k1  # Where to add?

# Element 2 - your turn!
```

**Checkpoint:** Print K_global. It should be 3×3 and symmetric!

---

### Step 4: Apply Boundary Conditions (Same Driver - 5 min)

**Navigator:** "Node 0 is fixed, so remove the first row and first column from K_global. Store it as K_reduced."

"Create a force vector: 0 on node 1, 1000 on node 2. Then remove the first entry. Store as F_reduced."

**Switch roles again!**

---

### Step 5: Solve & Visualize (New Driver - 10 min)

**New Navigator:** "Use numpy.linalg.solve to find u_reduced. Add u0 equals 0 at the beginning to get the full displacement vector u."

"Print the results: for each node, print its number and displacement."

**Then together:** "Now import PyVista. Create two sets of points: original nodes and deformed nodes. Use pv.Line for both. Plot them with different colors and labels."

```python
# Driver: Complete this
u_reduced = np.linalg.solve(___, ___)
u = np.array([0, ___, ___])  # Full displacement

# Visualize
import pyvista as pv

# Original
original_points = np.column_stack([nodes, np.zeros(3), np.zeros(3)])
original_line = pv.Line(original_points[0], original_points[-1], resolution=2)

# Deformed (scale by 100 to see it!)
scale = 100
deformed = nodes + scale * u
# Continue - create deformed_line and plot both!
```

---

### Expected Results

You should get:
- $u_1 \approx 5 \times 10^{-6}$ m (5 microns)
- $u_2 \approx 1 \times 10^{-5}$ m (10 microns)

**If not, debug together!**

---

## Block 5: Code Review & Improvement (45 min)

### Phase 1: Musical Chairs (15 min)

**Everyone stand up!**

1. Leave your laptop at your desk with your code visible
2. Move to the next desk (clockwise around the room)
3. You now see someone else's FEM code

**Your task (10 minutes):**
- Read their code carefully
- Write down on paper:
  - ✅ 2 things they did well
  - 🔧 3 things that could be improved
  - 💡 1 extension idea

**Don't change their code yet!**

---

### Phase 2: Discussion (5 min)

Return to your own desk. Your reviewer left notes for you!

**Read the feedback. Do you:**
- Agree with the improvements?
- Understand the suggestions?
- Have questions?

Discuss with your original partner!

---

### Phase 3: Implementation (25 min)

**Choose ONE improvement from the feedback and implement it.**

Ideas might include:
- Add comments explaining each step
- Create functions for repeated code
- Add error checking (what if L=0?)
- Make it work for any number of elements
- Add units to print statements
- Improve the plot (labels, legend, grid)

**Deliverable:**
- Improved code
- Screenshot of visualization
- One sentence: "We improved ___ because ___"

---

## Block 6: Extension Challenges (45 min)

### Instructions

Pick **ONE** challenge and implement it from scratch:

---

### Challenge A: More Elements (Beginner)

**Goal:** Extend your FEM to 5 elements (6 nodes)

**Requirements:**
- Nodes at $x = [0, 0.5, 1.0, 1.5, 2.0, 2.5]$ m
- Same material properties
- Node 0 still fixed
- Force at last node

**Questions to answer:**
- How does displacement change with more elements?
- Is the solution more accurate?

---

### Challenge B: Distributed Load (Intermediate)

**Goal:** Apply force to multiple nodes, not just one

**Scenario:** Instead of 1000 N at node 2, apply:
- 500 N at node 1
- 500 N at node 2

**Requirements:**
- Modify force vector F
- Solve and visualize
- Compare to Challenge A

**Question:** How does the deflection shape change?

---

### Challenge C: Animation (Intermediate)

**Goal:** Animate the force increasing from 0 to 1000 N

**Requirements:**
- Loop from $F = 0$ to $1000$ N in steps of 50
- Solve for each force value
- Create frames showing deformed shape
- Save as GIF or show in interactive window

**Hint:** Look up `pv.Plotter` with `pl.update()` in a loop

---

### Challenge D: 2D Truss (Advanced)

**Goal:** Planar truss structure - bar elements in 2D space with 2 DOF per node

**Concept:** Each node can move in $x$ and $y$ directions ($u_x$, $u_y$). Bar elements resist only axial forces, but are oriented at angles requiring coordinate transformation.

```
        Node 1 (0, 1)
           |
           | Element 1 (vertical)
           |
  Node 0 (0,0) -------- Node 2 (1, 0)
         fixed      Element 2 (horizontal)
                      → Force F
```

**Requirements:**
- 3 nodes with $(x,y)$ coordinates
- Each node has 2 DOF: displacement in $x$ and $y$
- Element stiffness in local coordinates (along bar axis)
- Transformation to global coordinates using rotation matrices
- Global stiffness matrix is $6 \times 6$ (3 nodes × 2 DOF/node)
- Apply BCs: Node 0 fixed ($u_x=0$, $u_y=0$)
- Load: Force $F$ in $x$-direction at Node 2

**Key equations:**
- Local stiffness: $\mathbf{k}_{\text{local}} = \frac{EA}{L} \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}$ (same as 1D!)
- Transformation matrix $\mathbf{T}$ using element angle $\theta$
- Global stiffness: $\mathbf{k}_{\text{global}} = \mathbf{T}^T \cdot \mathbf{k}_{\text{local}} \cdot \mathbf{T}$ ($4\times4$ for 2-node element)
- Assemble into $6\times6$ system

**This is challenging - requires understanding of coordinate transformations!**

---

### Challenge E: Material Comparison (Beginner)

**Goal:** Compare different materials

**Materials:**
- Steel: $E = 200$ GPa
- Aluminum: $E = 70$ GPa
- Titanium: $E = 110$ GPa

**Requirements:**
- Solve for all three materials
- Plot all three deformed shapes on same plot (different colors)
- Create a bar chart: material vs. maximum displacement
- Which material is stiffest?

---

## Submission

By end of Block 6, push to your fork:

```
fem-workshop/
├── fem_1d_beam.py          (Your original FEM from Block 4)
├── fem_improved.py         (After code review, Block 5)
├── fem_challenge_X.py      (Your chosen challenge, Block 6)
├── visualization_1.png     (From Block 4)
├── visualization_2.png     (From Block 5)
└── visualization_3.png     (From Block 6)
```

Create a PR to the main repository with title: `FEM Workshop - [Your Name]`

---

## Learning Outcomes

By completing this workshop, you've:

- ✅ Written FEM code from scratch (not copy-paste!)
- ✅ Understood element stiffness matrix assembly
- ✅ Applied boundary conditions correctly
- ✅ Debugged and improved code through peer review
- ✅ Visualized structural analysis results
- ✅ Extended a basic solver to more complex scenarios

**Most importantly: You can now read and modify FEM code with confidence!**

---

## Bonus: Theoretical Deep Dive

If you finish early and want to understand the theory better:

### Why This Stiffness Matrix?

The element stiffness matrix comes from:

1. **Strain-displacement:** $\varepsilon = \frac{du}{dx}$
2. **Stress-strain:** $\sigma = E \cdot \varepsilon$
3. **Virtual work principle**
4. **Integration over element length**

This gives: $\mathbf{k} = \frac{EA}{L} \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}$

### What About 2D/3D?

- 2D: Need transformation matrices (local to global coordinates)
- 3D: 6 DOF per node (3 translations + 3 rotations for beams)
- Still the same principle: k_local → Transform → Assemble → Solve

### Real FEM Software

Commercial software (Abaqus, Ansys) does this for:
- Millions of elements
- Complex geometries
- Nonlinear materials
- Dynamic analysis
- Contact mechanics

**But the fundamental principle is what you just coded!**
