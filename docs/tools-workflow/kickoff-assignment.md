---
title: Kickoff Assignment
---

# Kickoff Assignment

## Overview

Welcome to the Visualization & Data Processing course! This kickoff assignment will help you set up your development environment, familiarize yourself with the course workflow, and complete your first hands-on tasks.

> **Quick Reference:** The [slides of sessions 1 and 2](../slides.md) give a condensed overview of this material.

## Learning Objectives

By completing this assignment, you will:

- Set up a complete development environment for the course
- Practice Git and GitHub workflows (as shown in the lecture slides)
- Create your first Markdown documents
- Understand the course repository structure
- Submit your first Pull Request

:::info Read this first
All assignments in this course are submitted the same way. The rules for branch
names, folders and pull requests are described once in
[Submission Workflow](./submission-workflow.md). This assignment walks you
through them for the first time.
:::

> ** Pro Tip:** Follow along with the live demo from today's lecture!

## Prerequisites

Before starting, ensure you have:

- A computer with internet access (Windows, macOS, or Linux)
- Administrative privileges to install software
- A GitHub account (create one at [github.com](https://github.com) if needed)

## Part 1: Environment Setup

### Step 1: Install Required Software

#### Git
Download and install Git from [git-scm.com](https://git-scm.com/)

**Windows:**
```bash
# Check if Git is installed
git --version
```

**macOS:**
```bash
# Install using Homebrew (recommended)
brew install git

# Or download from git-scm.com
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install git
```

#### VS Code
Download and install VS Code from [code.visualstudio.com](https://code.visualstudio.com/)

#### Python

Install **Python 3.13**, 64 bit, from [python.org](https://www.python.org/downloads/).

:::warning Not the newest version, and not the free-threaded one
Two traps that cost a whole afternoon if you walk into them.

**Take 3.13, not 3.14 or newer.** The front page of python.org offers you the
latest release. Some of the packages this course uses, VTK and PyTables among
them, do not publish builds for it yet, and the installation then fails with a
compiler error that looks far worse than the problem is.

**Leave "free-threaded binaries" unticked** in the Windows installer. It is an
experimental build of Python, and numba and VTK have no packages for it.
:::

During installation on Windows, tick **"Add python.exe to PATH"**. It saves you
from typing the full path later.

```bash
# Verify Python installation
python --version         # expected: Python 3.13.x

# Verify it is the 64 bit build
python -c "import struct; print(struct.calcsize('P') * 8)"   # expected: 64
```

### Step 2: Configure Git

Set up your Git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Set Up SSH Keys (Recommended)

Generate SSH keys for secure GitHub access:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent (Windows Git Bash/macOS/Linux)
eval "$(ssh-agent -s)"

# Add key to SSH agent
ssh-add ~/.ssh/id_ed25519
```

Copy your public key (.ssh directory in user directory must exist):

```bash
# Windows
type ~/.ssh/id_ed25519.pub | clip

# macOS
pbcopy < ~/.ssh/id_ed25519.pub

# Linux
cat ~/.ssh/id_ed25519.pub
```

Add the SSH key to GitHub:
1. Go to GitHub → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste your public key
4. Give it a descriptive title

### Step 4: Install VS Code Extensions

Install these essential extensions:

**Required Extensions:**
- **C/C++** (Microsoft)
- **C/C++ Themes** (Microsoft) 
- **Git Graph** (mhutchie)
- **GitHub Pull Requests and Issues** (GitHub)
- **Marp for VS Code**
- **Python** (Microsoft)
- **Python Debugger** (Microsoft)
- **Python Environments** (Microsoft)
- **Pylance** (Microsoft)

## Part 2: Repository Setup

The course uses two repositories. The **course material** is public and contains
the script, the slides and the sample datasets, and you only read from it. Your
**submissions** go into a separate private repository, in which you are invited
as a collaborator. [Submission Workflow](./submission-workflow.md) explains the
split in detail.

### Step 1: Clone the Course Material

```bash
git clone https://github.com/soberpe/visdat-course.git
```

You need this copy because the workshops use the datasets in `data/`. Keep it up
to date during the semester with `git pull`.

### Step 2: Accept the Invitation and Clone the Submissions Repository

You receive an invitation by email in the first week. Accept it, then clone:

```bash
git clone https://github.com/soberpe/visdat-abgaben-<semester>.git
cd visdat-abgaben-<semester>
```

`<semester>` stands for the current semester, for example `ws2627` for the
winter semester 2026/27. The exact link is in your invitation email.

### Step 3: Protect Your Email Address

Git writes your name and email address into every commit, permanently. Switch on
email privacy before your first commit:

1. On GitHub, go to **Settings → Emails** and enable *Keep my email addresses
   private* and *Block command line pushes that expose my email*
2. Copy the `@users.noreply.github.com` address shown there, exactly as it is
3. Configure git with your real name and that address:

```bash
git config --global user.name "Your Real Name"
git config --global user.email 12345678+username@users.noreply.github.com
```

:::warning Copy the number, do not invent it
The noreply address starts with a number, your GitHub account ID. GitHub
assigns every commit to an account by this number. With a wrong one, for
example the `12345678` from the line above, your commits appear under a
stranger's account, and that stranger shows up as a contributor. Copy your own
address from **Settings → Emails**, where it stands ready under *Keep my email
addresses private*.
:::

:::warning Not your university address
Your FH address contains your student ID, and a commit history is forever. Use
the noreply address.
:::

### Step 4: Create Your Working Branch

Create a new branch for every assignment, named
`submission/<assignment>/<your-github-username>`:

```bash
# Create and switch to a new branch for your work
git checkout -b submission/kickoff/[your-github-username]

# Example:
git checkout -b submission/kickoff/octocat
```

:::warning Do not work on main
Never commit your assignments to `main`. Your own work lives on assignment
branches and reaches `main` through a reviewed pull request. See
[Submission Workflow](./submission-workflow.md) for the reason behind this.
:::

## Part 3: Complete the Tasks

### Task 1: Create Your Submission Folder

Every student owns one folder under `submissions/` and works only inside it.
This is what makes it possible to merge more than twenty submissions into the
same repository without conflicts.

1. Open the submissions repository in VS Code:
   ```bash
   code .
   ```

2. Create your folder, named after your GitHub username in **lowercase**:
   ```bash
   mkdir -p submissions/[your-github-username]/01-kickoff

   # Example, for the account "Octocat":
   mkdir -p submissions/octocat/01-kickoff
   ```

   :::warning Lowercase, even if your username has capitals
   GitHub shows your username the way you registered it, for example
   `Octocat`. Your folder is always written in lowercase: `octocat`. The
   automatic check compares the folder name with the author of your pull
   request, and a single capital letter makes it fail.
   :::

   :::tip Folder already created with capitals?
   Do not rename it in the Explorer or in VS Code. Windows does not distinguish
   upper and lower case in file names, so Git does not notice the change, and
   the check keeps failing. Rename it with Git instead, in two steps, and commit
   once:

   ```bash
   git mv submissions/Octocat submissions/octocat-tmp
   git mv submissions/octocat-tmp submissions/octocat
   git commit -m "Rename my folder to lowercase"
   ```

   The result is one clean commit with the correct folder name.
   :::

3. Create the file `submissions/[your-folder]/01-kickoff/about.md` with your
   profile:

   ```markdown
   # [Your Name]

   - **GitHub:** [@your-username](https://github.com/your-username)
   - **Program:** Master Mechanical Engineering
   - **Interests:** [List 2-3 areas of interest related to data visualization]
   - **Background:** [Brief description of your programming/engineering background]
   ```

:::warning Replace every placeholder
The square brackets above mark places where your own text goes. The automatic
check rejects pull requests that still contain placeholders such as
`[Your Name]`.
:::

### Task 2: Create Your Introduction Document

1. Create a new file: `submissions/[your-folder]/01-kickoff/introduction.md`

2. Write a personal introduction following this template:

```markdown
# Introduction - [Your Full Name]

## About Me

Write a brief introduction about yourself (2-3 paragraphs):
- Your educational background
- Previous experience with programming or data analysis
- Why you're taking this course
- What you hope to learn

## Technical Experience

### Programming Languages
- **Experienced:** [Languages you know well]
- **Basic Knowledge:** [Languages you've used but aren't expert in]
- **Want to Learn:** [Languages you're interested in learning]

### Tools and Technologies
List tools you've used:
- Development environments (VS Code, Visual Studio, etc.)
- Version control (Git, SVN, etc.)
- Data analysis tools (Excel, MATLAB, R, etc.)
- CAD software (SolidWorks, AutoCAD, etc.)

## Course Goals

What do you want to achieve in this course?
1. [Specific goal 1]
2. [Specific goal 2]
3. [Specific goal 3]

## Sample Data Interest

Describe a type of engineering data you work with or are interested in analyzing:
- What kind of data is it? (measurements, simulations, sensor data, etc.)
- What challenges does it present?
- What insights would you like to extract from it?

## Questions

List any questions you have about:
- The course content
- Programming concepts
- Data visualization techniques
- Tools we'll be using
```

### Task 3: Create a Marp Slide Presentation

1. Create a new file: `submissions/[your-folder]/01-kickoff/introduction-slides.md`

2. Create a 4-5 slide presentation about yourself using Marp:

```markdown
---
marp: true
paginate: true
footer: "VIS3VO · Student Introduction · [Your Name]"
---

# Student Introduction
## [Your Full Name]

Master Mechanical Engineering · 3rd Semester  
FH OÖ Wels

---

## About Me

- **Background:** [Your educational/professional background]
- **Experience:** [Relevant experience]
- **Interests:** [Your interests related to the course]

---

## Technical Skills

### Programming
- **Comfortable with:** [Languages/tools you know]
- **Learning:** [What you're currently learning]

### Engineering Tools
- [List relevant engineering software/tools]

---

## Course Expectations

### What I want to learn:
- [Expectation 1]
- [Expectation 2]
- [Expectation 3]

### Data I work with:
- [Describe your data interests]

---

## Questions & Goals

### Questions:
- [Question about course content]
- [Question about tools/methods]

### Goals:
- [Specific learning goal]
- [Project aspiration]

Thank you!
```

### Task 4: Practice Git Workflow

Track your changes:

```bash
# Check status of your changes
git status

# Add specific files
git add submissions/[your-folder]/01-kickoff/about.md
git add submissions/[your-folder]/01-kickoff/introduction.md
git add submissions/[your-folder]/01-kickoff/introduction-slides.md

# Or add everything inside your own folder
git add submissions/[your-folder]

# Commit your changes
git commit -m "Add kickoff submission

- Added profile and personal introduction
- Created Marp presentation for self-introduction"
```

:::tip Commit in small steps
Commit each task on its own instead of committing everything at the end. Your
commit history shows how you worked, and it is part of what is assessed in this
course. It is also the only thing that helps you when you need to undo a change.
:::

### Task 5: Test Your Marp Slide

1. Open your slide file in VS Code
2. Use `Ctrl+Shift+P` and search for "Marp: Show preview"
3. Verify your slides render correctly
4. Make any necessary adjustments

### Task 6: Export to HTML (Optional)

To create a standalone HTML version of your slides:

**Method 1: VS Code Command**
1. Open your `.md` slide file
2. `Ctrl+Shift+P` → "Marp: Export slide deck"
3. Choose "HTML" format
4. Save it next to your slide file as `introduction-slides.html`

**Method 2: Command Line (Advanced)**
```bash
# Install Marp CLI (one-time setup)
npm install -g @marp-team/marp-cli

# Export to HTML
marp submissions/[your-folder]/01-kickoff/introduction-slides.md --html \
  --output submissions/[your-folder]/01-kickoff/introduction-slides.html
```

## Part 4: Submission

### Step 1: Push Your Changes

```bash
# Push your branch to the submissions repository
git push -u origin submission/kickoff/[your-github-username]
```

### Step 2: Create a Pull Request

1. Go to the submissions repository on GitHub
2. Click "Compare & pull request" (should appear after pushing)
3. Set the base branch to `main`
4. Set the compare branch to your assignment branch

You do not have to wait until everything is finished. An open pull request
updates itself: every further push to your branch appears in it automatically,
and the automatic check runs again each time.

### Step 3: Fill Out the Pull Request Template

The description of your pull request is prefilled with a template. Replace the
placeholders and tick the boxes of the self check. The section on AI tools is
part of the submission: using them is allowed, describing how you used them is
required.

### Step 4: Wait for the Automatic Check

When your pull request is open, an automatic check verifies that it only touches
your own folder, that no file is too large and that no placeholders are left. It
usually finishes within a minute.

If it fails, open the **Details** link, read the summary and push a fix to the
same branch. The check then runs again on its own. If it passes, your submission
is ready for review.

:::note Corrections
Never open a second pull request for the same assignment. Push more commits to
the same branch instead, and they show up in the existing pull request
automatically.
:::

## Grading Criteria

This assignment will be evaluated based on:

| Criteria | Points | Description |
|----------|--------|-------------|
| **Environment Setup** | 20 | All required software installed and configured |
| **Git Workflow** | 25 | Proper use of Git commands, branching, and PR creation |
| **Documentation Quality** | 25 | Well-written introduction document with all required sections |
| **Marp Presentation** | 20 | Functional slide presentation with good content and formatting |
| **Following Instructions** | 10 | All tasks completed as specified |

**Total: 100 points**

## Getting Help

If you encounter issues:

### Technical Problems
1. Check the course documentation
2. Search online for error messages
3. Ask questions in the course repository Issues
4. Attend office hours

### Git/GitHub Issues
Common solutions:
```bash
# If you make a mistake in commit message
git commit --amend -m "New commit message"

# If you need to add more files to last commit
git add forgotten-file.md
git commit --amend --no-edit

# If you need to get the latest state of main
git checkout main
git pull
```

### Markdown/Marp Issues
- Use VS Code's Markdown preview
- Check Marp documentation: [marp.app](https://marp.app/)
- Validate your YAML frontmatter

## Timeline

The assignment is handed out in session 2 and is due two weeks later.

- **Session 2, in class:** environment set up, both repositories cloned, your
  branch created
- **Session 3, in class:** first commits pushed, pull request open, even if the
  work in it is not finished yet
- **By the deadline:** all tasks done, automatic check passing, feedback
  addressed

## Next Steps

After completing this assignment:

1. **Keep both clones up to date:**
   ```bash
   # In the course material
   git pull

   # In the submissions repository, before each new assignment
   git checkout main
   git pull
   ```

2. **Explore the repository structure**
3. **Read through other course materials**
4. **Prepare for the data processing session**

## Bonus Challenges (Optional)

For additional practice:

1. **Advanced Git:** Try rebasing your commits to clean up history
2. **Markdown Extensions:** Add a table of contents to your introduction
3. **Marp Themes:** Customize your presentation with a custom theme
4. **VS Code:** Set up custom shortcuts and workspace settings

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Marp Documentation](https://marp.app/)
- [VS Code Documentation](https://code.visualstudio.com/docs)

Good luck with your kickoff assignment!