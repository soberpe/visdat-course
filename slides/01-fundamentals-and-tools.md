---
marp: true
theme: visdat
paginate: true
footer: "FH OÖ Wels · Visualisierung & Datenaufbereitung"
---

<!-- _class: title -->

# Programming Fundamentals & Tools

## How we work for the rest of the semester

Lecture 1 · Stefan Oberpeilsteiner

<!--
First session. Two things matter today: that everyone leaves with a working
environment, and that everyone has opened one pull request. The programming
content is a map, not a syntax course. The syntax is in the script.
-->

---

# Today

1. **Organisation**: how the course runs, how you hand in, how it is graded
2. **Paradigms**: the three ways to structure a program, and why we mix them
3. **Two languages**: what C++ is for, what Python is for
4. **Git**: the model behind it, then the commands
5. **Hands on**: environment, first pull request

<p class="note">Everything shown here is in the script. What is not in the script is the reasoning.</p>

---

<!-- _class: ask -->

# A colleague sends you a 2 GB result file and needs a plot by tomorrow. Where do you start?

<!--
Collect answers. Expect Excel, expect ParaView, expect "I'd ask what they want
to see". The last one is the right instinct. Use this to frame the semester:
the whole chain from that file to a picture someone can act on, and everything
in between is what we practise.
-->

---

# What you build this semester

<div class="boxes">
<div><b>Data</b>Read, clean and store engineering data that does not fit in a spreadsheet.</div>
<div><b>Pictures</b>2D and 3D, chosen for the question, not for the chart menu.</div>
<div><b>A tool</b>A desktop application with your own interface that someone else can use.</div>
</div>

The final assignment is your own project along this chain. Everything before it
is practice for it.

---

# How the course runs

- **Course material** is public: this site, the slides, the sample data
- **Your work** goes into a private repository, one folder per student
- **Every assignment** is a pull request, reviewed, then merged
- **Assessment**: the assignments during the semester, the final project, and
  your presentation of it

<p class="note">Details: Course Organization and Submission Workflow on the course site.</p>

<!--
Stress the private repository and why: their names, accounts and commit
metadata are personal data and do not belong in a public repo. Invitations go
out this week, so collect GitHub usernames today.
-->

---

# Three ways to structure a program

<div class="boxes">
<div><b>Procedural</b>Steps in order, data passed along. Most scripts start here.</div>
<div><b>Object oriented</b>State and the operations on it, kept together. Qt is built this way.</div>
<div><b>Functional</b>Pure functions, no hidden state. NumPy and pandas think this way.</div>
</div>

> Nobody picks one. You use the one that fits the problem, and a single file
> often contains all three.

---

# Structured programming is three constructs

<div class="cols">
<div>

```cpp
for (int i = 0; i < 5; ++i) {
  if (i % 2 == 0) continue;
  std::cout << i << " ";
}
```

</div>
<div>

```python
for i in range(5):
    if i % 2 == 0:
        continue
    print(i, end=" ")
```

</div>
</div>

**Sequence**, **selection**, **iteration**. Every language you will meet offers
these three, and almost nothing else at this level.

<p class="note">The syntax differs. The structure does not. That is why a second language is cheap once you have the first.</p>

---

# Compiled or interpreted

<div class="cols">
<div>

**Compiled**

A separate step turns your source into machine code. The compiler sees the whole
program, checks types, and optimises.

Fast to run, slower to change. C, C++, Rust, Fortran.

</div>
<div>

**Interpreted**

The source is executed as it is read, statement by statement.

Fast to change, slower to run. Python, MATLAB, JavaScript.

</div>
</div>

> This one difference explains most of what confuses people later: why NumPy is
> fast, why `pip install` sometimes compiles, why CMake exists, and why Python
> threads do not speed up computation.

<!--
Do not treat this as a language comparison. It is a category, and they will meet
the consequences of it in every later block. Ask which of the two a solver like
CalculiX is, and why.
-->

---

# The two languages in this course

<div class="cols">
<div>

**C++**, the compiled one

Our representative for the whole class. Memory and layout under your control,
and the libraries you use from Python are written in it.

You read it, you compile it, and you use it where speed decides.

</div>
<div>

**Python**, the interpreted one

Quick to write, the scientific ecosystem, the glue between the tools.

You write most of the semester in it, including the final project.

</div>
</div>

<p class="note">Syntax for both is in the script, with exercises. We are not spending the lecture on semicolons.</p>

---

<!-- _class: section -->

# Git

## The part that pays off for the rest of your career

---

<!-- _class: ask -->

# Your script worked yesterday. Today it does not, and you do not know what you changed.

<!--
Everyone has lived this. That is the entire motivation for version control, and
it lands better than "industry standard". Follow up: what did you do last time?
Usually a folder called "final_v3_really_final".
-->

---

# A change lives in four places

<div class="boxes">
<div><b>Working directory</b>Your files, as you edit them right now.</div>
<div><b>Staging area</b>What you have selected for the next snapshot. <code>git add</code></div>
<div><b>Local repository</b>The snapshots on your machine. <code>git commit</code></div>
<div><b>Remote</b>The copy on GitHub that others see. <code>git push</code></div>
</div>

Most Git confusion is not knowing which of the four you are looking at.
`git status` always tells you.

---

<!-- _class: live -->

# The four commands

```bash
git status                       # where am I, what changed
git add submissions/octocat/     # select for the snapshot
git commit -m "Add introduction" # take the snapshot
git push                         # publish it
```

Then: change a file, run `git status` again, and read the output together.

<!--
Type it, do not paste. Make a deliberate mistake: commit without add, and let
them see that nothing happened. The point is that status answers every question
they will have for the next three weeks.
-->

---

# Why a branch, and why a pull request

```bash
git checkout -b submission/kickoff/octocat
```

- The branch keeps your unfinished work away from `main`
- The pull request is where the **review** happens, before it becomes part of
  the repository
- Corrections are more commits on the **same** branch, not a second pull request

> This is not a course convention. It is how the code you will write after
> graduating gets into a product.

---

# Two repositories

<div class="cols">
<div>

**visdat-course**, public

Script, slides, sample data. You clone it and read from it. You never push to it.

</div>
<div>

**visdat-abgaben-ws2627**, private

Your submissions, one folder per student named after your GitHub account. You
are invited as a collaborator.

</div>
</div>

<p class="note">Invitation comes by email this week. Give me your GitHub username today.</p>

---

<!-- _class: live -->

# Your first pull request, end to end

```bash
git clone https://github.com/soberpe/visdat-abgaben-ws2627.git
cd visdat-abgaben-ws2627
git checkout -b submission/kickoff/octocat

mkdir -p submissions/octocat/01-kickoff
# write the file, then
git add submissions/octocat
git commit -m "Add kickoff introduction"
git push -u origin submission/kickoff/octocat
```

Then on GitHub: open the pull request, watch the automatic check run.

<!--
Do this on the projector with a throwaway account or your own folder. Show the
check going red once on purpose, by touching a file outside the folder, so they
recognise the message when it happens to them.
-->

---

<!-- _class: section -->

# Environment

## Everything installed before you leave the room

---

# Python and the virtual environment

```bash
python -m venv .venv                    # if python is on PATH
C:\Python313\python.exe -m venv .venv   # Windows, when it is not

.venv\Scripts\activate                  # Windows
source .venv/bin/activate               # macOS, Linux

pip install -r requirements.txt
```

A virtual environment keeps this course's packages out of your system Python,
and makes `requirements.txt` mean something.

<p class="note">In VS Code: Ctrl+Shift+P, "Python: Create Environment", does the same thing with fewer chances to get it wrong.</p>

---

# VS Code extensions

Python, Pylance, Python Debugger, Python Environments
C/C++ and C/C++ Themes
Git Graph, GitHub Pull Requests and Issues
Marp for VS Code

<p class="note">Open the course repository as a folder and the Marp theme is configured for you.</p>

---

# Protect your email address

```bash
git config --global user.name "Your Real Name"
git config --global user.email 12345678+username@users.noreply.github.com
```

On GitHub, **Settings → Emails**: enable *Keep my email addresses private* and
*Block command line pushes that expose my email*.

> Your FH address contains your student ID, and a commit history is permanent.
> Set this before your first commit, not after.

<!--
Last year several submissions carried the FH address with the matriculation
number in every commit. It cannot be removed afterwards without rewriting
history. Two minutes now saves that.
-->

---

<!-- _class: section -->

# Kickoff assignment

## Due in two weeks

---

# What to do

1. Install Git, VS Code and Python, configure your identity
2. Clone both repositories, accept the invitation
3. Create your folder `submissions/<your-github-username>/01-kickoff/`
4. Write a short profile and an introduction, in Markdown
5. Build a 4 to 5 slide Marp deck about yourself
6. Open the pull request and get the automatic check to pass

<p class="note">Full description: Kickoff Assignment on the course site.</p>

---

# Grading

| Criterion | Points |
|---|---|
| Environment set up and working | 20 |
| Git workflow: branch, commits, pull request | 25 |
| Documentation quality | 25 |
| Marp presentation | 20 |
| Instructions followed | 10 |

<p class="note">Commit history counts. Six small commits tell me more than one big one, and they help you more too.</p>

---

# Hands on, the rest of today

1. **Environment**, 30 minutes: Git, VS Code, Python, identity, SSH key
2. **Repositories**, 20 minutes: clone both, create your branch
3. **The assignment**, remaining time: write, commit, push, open the pull request

Work in pairs. Raise a hand early rather than late.

---

# Next week

Data formats and processing: CSV, Excel, HDF5, and pandas on real sensor data.

```python
import pandas as pd

df = pd.read_csv("data/sensor_data.csv")
df.describe()
```

<p class="note">Bring your laptop with the environment working. We start with data, not with installation.</p>
