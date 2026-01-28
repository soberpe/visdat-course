---
title: Kickoff Assignment
---

# Kickoff Assignment

## Overview

Welcome to the Visualization & Data Processing course! This kickoff assignment will help you set up your development environment, familiarize yourself with the course workflow, and complete your first hands-on tasks.

> **📽️ Quick Reference:** See Lecture 1 Slides (01-fundamentals-and-tools-marp.html) for a condensed overview of today's material.

## Learning Objectives

By completing this assignment, you will:

- Set up a complete development environment for the course
- Practice Git and GitHub workflows (as shown in the lecture slides)
- Create your first Markdown documents
- Understand the course repository structure
- Submit your first Pull Request

> **💡 Pro Tip:** Follow along with the live demo from today's lecture!

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
Download Python 3.8+ from [python.org](https://python.org/)

```bash
# Verify Python installation
python --version
# or
python3 --version
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

### Step 1: Fork the Course Repository

1. Go to the course repository: `https://github.com/soberpe/visdat-course`
2. Click the "Fork" button in the top-right corner
3. Choose your GitHub account as the destination

### Step 2: Clone Your Fork

```bash
# Clone using SSH (recommended)
git clone git@github.com:[your-username]/visdat-course.git

# Or clone using HTTPS
git clone https://github.com/[your-username]/visdat-course.git

# Navigate to the repository
cd visdat-course
```

### Step 3: Set Up Upstream Remote

```bash
# Add upstream remote to stay in sync with the main repository
git remote add upstream git@github.com/soberpe/visdat-course.git

# Verify remotes
git remote -v
```

### Step 4: Create Your Working Branch

```bash
# Create and switch to a new branch for your work
git checkout -b assignment/kickoff-[your-name]

# Example:
git checkout -b assignment/kickoff-john-doe
```

## Part 3: Complete the Tasks

### Task 1: Update README.md

1. Open the repository in VS Code:
   ```bash
   code .
   ```

2. Find and open `README.md` in the root directory

3. Add a new section called "Students" and include your information:
   ```markdown
   ## Students

   ### [Your Name]
   - **GitHub:** [@your-username](https://github.com/your-username)
   - **Program:** Master Mechanical Engineering
   - **Interests:** [List 2-3 areas of interest related to data visualization]
   - **Background:** [Brief description of your programming/engineering background]
   ```

### Task 2: Create Your Introduction Document

1. Create a new file: `docs/students/[your-lastname]-introduction.md`

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

1. Create a new file: `slides/students/[your-lastname]-introduction.md`

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

Thank you! 🚀
```

### Task 4: Practice Git Workflow

Track your changes:

```bash
# Check status of your changes
git status

# Add specific files
git add README.md
git add docs/students/[your-lastname]-introduction.md
git add slides/students/[your-lastname]-introduction.md

# Or add all changes
git add .

# Commit your changes
git commit -m "Add student introduction and update README

- Added personal introduction in docs/students/
- Created Marp presentation for self-introduction
- Updated README with student information"
```

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
4. Save as `[your-lastname]-introduction.html`

**Method 2: Command Line (Advanced)**
```bash
# Install Marp CLI (one-time setup)
npm install -g @marp-team/marp-cli

# Export to HTML
marp slides/students/[your-lastname]-introduction.md --html --output slides/students/[your-lastname]-introduction.html
```

## Part 4: Submission

### Step 1: Push Your Changes

```bash
# Push your branch to your fork
git push origin assignment/kickoff-[your-name]
```

### Step 2: Create a Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request" (should appear after pushing)
3. Set the base repository to the instructor's repository
4. Set the base branch to `main`
5. Set the compare branch to your assignment branch

### Step 3: Fill Out Pull Request Template

Use this template for your PR description:

```markdown
## Kickoff Assignment Submission

### Student Information
- **Name:** [Your Full Name]
- **GitHub Username:** @[your-username]
- **Branch:** assignment/kickoff-[your-name]

### Completed Tasks
- [ ] Environment setup (Git, VS Code, Python, Node.js)
- [ ] Repository forked and cloned
- [ ] Updated README.md with student information
- [ ] Created personal introduction document
- [ ] Created Marp presentation
- [ ] All changes committed and pushed

### Files Modified/Added
- `README.md` - Added student information
- `docs/students/[your-lastname]-introduction.md` - Personal introduction
- `slides/students/[your-lastname]-introduction.md` - Marp presentation

### Questions/Comments
[Include any questions you have or challenges you encountered]

### Confirmation
I confirm that:
- [ ] All required software is installed and working
- [ ] I can successfully run Git commands
- [ ] VS Code is set up with required extensions
- [ ] My Marp slides render correctly
- [ ] I understand the course workflow
```

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

# If you need to sync with upstream
git fetch upstream
git merge upstream/main
```

### Markdown/Marp Issues
- Use VS Code's Markdown preview
- Check Marp documentation: [marp.app](https://marp.app/)
- Validate your YAML frontmatter

## Timeline

- **Week 1:** Complete environment setup and repository fork
- **Week 2:** Finish all documentation tasks
- **Week 3:** Submit Pull Request and address any feedback

## Next Steps

After completing this assignment:

1. **Keep your fork updated:**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   git push origin main
   ```

2. **Explore the repository structure**
3. **Read through other course materials**
4. **Prepare for Week 2 content on data formats**

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

Good luck with your kickoff assignment! 🎯