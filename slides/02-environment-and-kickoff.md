---
marp: true
theme: visdat
paginate: true
footer: "FH OÖ Wels · Visualisierung & Datenaufbereitung"
---

<!-- _class: title -->

# Environment & Kickoff

## From an empty laptop to your first pull request

Lecture 2 · Stefan Oberpeilsteiner

<!--
Second session. Two things matter today: that everyone leaves with a working
environment, and that everyone has opened a pull request. A problem found
today can be solved together in the room. The same problem found the evening
before the deadline cannot.
-->

---

# Today

1. **Git, continued**: two repositories, your first pull request
2. **Environment**: Python 3.13, a virtual environment, VS Code, your identity
3. **Kickoff assignment**: what to do, and how it is graded
4. **Hands on**: everything installed before you leave the room

---

# Last time

<div class="boxes">
<div><b>Working directory</b>Your files, as you edit them. <code>git status</code></div>
<div><b>Staging area</b>The selection for the next snapshot. <code>git add</code></div>
<div><b>Local repository</b>The snapshots on your machine. <code>git commit</code></div>
<div><b>Remote</b>The copy on GitHub that others see. <code>git push</code></div>
</div>

Work happens on a **branch**, and it gets into `main` through a **pull
request**, after a review.

---

# Two repositories

<div class="cols">
<div>

**visdat-course**, public

Script, slides, sample data. You clone it and read from it. You never push to it.

</div>
<div>

**visdat-abgaben-&lt;semester&gt;**, private

Your submissions, one folder per student named after your GitHub account. You
are invited as a collaborator. A new one is created every semester.

</div>
</div>

<p class="note">The invitation comes by email, with the exact link. Accept it before you clone.</p>

---

<!-- _class: live -->

# Your first pull request, end to end

```bash
git clone <link from the invitation email>
cd visdat-abgaben-<semester>
git checkout -b submission/kickoff/octocat

mkdir -p submissions/octocat/01-kickoff
# write the file, then
git add submissions/octocat
git commit -m "Add kickoff introduction"
git push -u origin submission/kickoff/octocat
```

Then on GitHub: open the pull request, watch the automatic check run.

<!--
Shown live on the projector, including one failing check: touching a file
outside your own folder turns the automatic check red. The message is worth
recognising before it happens to you.
-->

---

<!-- _class: section -->

# Environment

## Everything installed before you leave the room

---

# Python 3.13, and nothing newer

<div class="cols">
<div>

**Why not the latest**

VTK and PyTables publish no builds for 3.14 yet. The install then fails with a
compiler error that looks much worse than the problem is.

</div>
<div>

**Also avoid**

The "free-threaded binaries" option in the Windows installer. It is
experimental, and numba and VTK have nothing for it.

</div>
</div>

```bash
python --version                                          # Python 3.13.x
python -c "import struct; print(struct.calcsize('P')*8)"  # 64
```

<p class="note">On Windows, tick "Add python.exe to PATH" during installation.</p>

<!--
This slide exists because the wrong version costs an afternoon. The download
button on python.org always offers the newest release, and that is the one the
packages do not support yet. Worth saying twice, and worth checking again during
the installation block.
-->

---

# The virtual environment

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

- **Python**: Python, Pylance, Python Debugger, Python Environments
- **C++**: C/C++, C/C++ Themes
- **Git**: Git Graph, GitHub Pull Requests and Issues
- **Slides**: Marp for VS Code

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
A commit history is permanent, and the FH address contains the student ID. Once
it is in, it cannot be taken out again without rewriting history, which is far
more work than it sounds. Two minutes here prevents it.
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

# Next time

Programming basics: what a name, a reference and an object are, in Python and
in C++, and why it matters as soon as you work with data.

<p class="note">Bring your laptop with the environment working and your kickoff branch pushed.</p>
