---
marp: true
theme: visdat
paginate: true
footer: "FH OÖ Wels · Visualisierung & Datenaufbereitung"
---

<!-- _class: title -->

# FEM Coding Challenge

## The solver behind the colours

Workshop 8 · A 1D bar in pairs, reviewed by the room

<!--
The last two sessions showed FE results. Today everyone writes the part that
produces them, on the smallest problem that still has all the steps: element
stiffness, assembly, boundary conditions, solve. The instructions are on the
course site under Visualization, FEM Coding Challenge.
-->

---

<!-- _class: ask -->

# The solver says 6.9 MPa. How do you know it is right?

<!--
Collect answers: hand calculation, a mesh study, a second solver, experience.
All of them assume you know what the solver does inside. That is today.
-->

---

# Today

<div class="boxes">
<div><b>Block 1 · Pair programming</b>A 1D bar solver from an empty file, two people, one keyboard.</div>
<div><b>Block 2 · Code review</b>Read someone else's solver, then improve your own.</div>
<div><b>Block 3 · Extensions</b>One challenge of your choice, from more elements to a 2D truss.</div>
</div>

<p class="note">Submission at the end: one pull request per person, details on the last slides.</p>

---

<!-- _class: section -->

# Block 1

## Pair programming

<p>45 minutes · switch roles every 10 minutes</p>

---

# Driver and navigator

<div class="cols">
<div>

**Driver**

Has the keyboard. Types what the navigator says, and nothing else.

</div>
<div>

**Navigator**

Reads the instructions aloud, thinks one step ahead, catches the errors. Does not touch the keyboard.

</div>
</div>

<p class="note">The navigator dictates in words, not in code. If you can say it, you have understood it.</p>

<!--
Pairs of two, form them now. The roles feel awkward for five minutes and then
start to work. The script contains the code skeletons, but the navigator is
asked not to show them: the driver has to build the code from the spoken
description.
-->

---

# The problem

```
Fixed wall |----Element 1----|----Element 2----| → F
           0                 1                 2      x [m]
         Node 0            Node 1            Node 2
```

<div class="cols">
<div>

- Steel, $E = 200$ GPa
- Cross section $A = 0.01$ m²
- Node 0 fixed, $u_0 = 0$
- $F = 1000$ N at node 2

</div>
<div>

$$
\mathbf{k}_e = \frac{EA}{L}
\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}
$$

**Find** $u_1$ and $u_2$.

</div>
</div>

<!--
A bar, not a beam: it carries only axial force and each node has one degree of
freedom. That is why the element matrix is 2 by 2.
-->

---

# Five steps

| Step | What | Time |
|---|---|---|
| 1 | Node positions and material, in SI units | 5 min |
| 2 | `stiffness_1d_bar(E, A, L)` returns the 2 × 2 matrix | 5 min |
| 3 | Assemble both elements into a 3 × 3 `K_global` | 10 min |
| 4 | Fix node 0: drop its row and column, build `F_reduced` | 5 min |
| 5 | `np.linalg.solve`, print, plot with PyVista | 10 min |

<p class="note">Switch the driver after step 2 and after step 4.</p>

---

# Assembly is addition

<div class="cols">
<div>

```python
K = np.zeros((3, 3))
K[0:2, 0:2] += k1   # nodes 0 and 1
K[1:3, 1:3] += k2   # nodes 1 and 2
```

Each element adds its matrix where its nodes are. Where two elements share a
node, the entries add up.

</div>
<div>

$$
\mathbf{K} = \frac{EA}{L}
\begin{bmatrix}
1 & -1 & 0 \\
-1 & 2 & -1 \\
0 & -1 & 1
\end{bmatrix}
$$

Symmetric, and singular until node 0 is fixed.

</div>
</div>

<!--
The 2 in the middle is the shared node. Ask what happens if you call solve on
the full matrix before applying the boundary condition: numpy raises
LinAlgError, because a bar that is not held anywhere can move freely and has no
unique displacement.
-->

---

# Check your result

<div class="cols">
<div>

**By hand**

$EA = 200 \cdot 10^9 \cdot 0.01 = 2 \cdot 10^9$ N

One element stretches by
$FL/EA = 1000 / (2 \cdot 10^9) = 5 \cdot 10^{-7}$ m

</div>
<div>

**Expected**

$u_1 = 5 \cdot 10^{-7}$ m

$u_2 = 1 \cdot 10^{-6}$ m

</div>
</div>

<p class="note">Off by a power of ten? Check that E is in Pa and A in m².</p>

---

# Making a micrometre visible

```python
scale = 1e5
deformed = nodes + scale * u
# draw the deformed bar at y = -0.2, below the original
```

- A bar under tension moves **along its own axis**. Drawn at the same height, the deformed line hides behind the original.
- The scale factor is part of the picture: put it in the title.

<!--
Same question as with the beam in session 6, at a much larger factor: what does
the factor do to the truth? Here it turns one micrometre into ten centimetres.
-->

---

<!-- _class: section -->

# Block 2

## Code review

<p>45 minutes · 15 reading, 5 talking, 25 improving</p>

---

# Musical chairs

<div class="cols">
<div>

1. Leave your code open on the screen
2. Move one desk clockwise
3. Read, and write on paper:
   - **2** things done well
   - **3** things to improve
   - **1** idea for an extension
4. Do not change the code
5. Back to your own desk, read the notes

</div>
<div>

**Good review comments**

- are about the code, not the person
- name the line
- say why, not only what

*"Line 12: the 3 is the number of nodes. With `len(nodes)` it would also work for 6 nodes."*

</div>
</div>

<!--
This is the same review that happens in every pull request in this course, on
paper and face to face. It is also the first time most people read someone
else's solution to the same problem, which is where most of the learning is.
-->

---

# Improve one thing

Pick **one** point from your review and implement it.

<div class="boxes">
<div><b>Structure</b>Functions instead of repeated code, any number of elements</div>
<div><b>Safety</b>Check inputs, for example a length of zero</div>
<div><b>Clarity</b>Comments, units in the output, a plot with labels</div>
</div>

<p class="note">Write one sentence for the pull request: "We improved ___ because ___."</p>

---

<!-- _class: section -->

# Block 3

## Extensions

<p>45 minutes · one challenge, from scratch</p>

---

# Pick one

| | Challenge | Level |
|---|---|---|
| A | More elements: 5 elements, 6 nodes | Beginner |
| E | Material comparison: steel, aluminium, titanium | Beginner |
| B | Distributed load: 500 N at node 1 and node 2 | Intermediate |
| C | Animation: the load grows from 0 to 1000 N | Intermediate |
| D | 2D truss: two degrees of freedom per node, rotated elements | Advanced |

<p class="note">D needs the transformation from local to global coordinates. It is the step from this toy to a real solver.</p>

---

<!-- _class: ask -->

# More elements: is it more accurate?

<!--
Challenge A asks exactly this. Compare the displacement at x = 1 m and x = 2 m:
it is 5e-7 m and 1e-6 m, the same as with two elements. For a bar with a point
load at the end the strain is constant, and linear elements reproduce it
exactly, so refining changes nothing. The tip moves further only because the
bar in challenge A is 2.5 m long. With stress concentrations like in the beam,
refining would change the result. Knowing when a model is already exact is part
of verification.
-->

---

# Submission

Branch `submission/fem-challenge/<your-github-username>`

```
submissions/<your-github-username>/04-fem-challenge/
├── fem_1d_bar.py          Block 1
├── fem_improved.py        Block 2
├── fem_challenge_X.py     Block 3
├── visualization_1.png
├── visualization_2.png
└── visualization_3.png
```

Pull request title: `FEM Challenge - <your name>`

<p class="note">Both partners submit, each in their own folder.</p>

---

# Recap

- An FE solver is **element matrices, assembly, boundary conditions, solve**
- Assembly **adds** each element where its nodes are
- Without boundary conditions the stiffness matrix is **singular**
- A hand calculation is the cheapest **check** there is
- A scale factor changes the picture, **not the result**. Say what it is.

---

<!-- _class: section -->

# Next

## User interfaces

<p>From scripts to windows: Qt, signals and slots, PyVista inside your own application.</p>
