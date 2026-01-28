---
title: Development Tools & Workflow
---

# Development Tools & Workflow

## Overview

Modern software development relies on a robust set of tools that enable collaboration, version control, and reproducible workflows. This course emphasizes industry-standard practices that you'll encounter in professional engineering environments.

> **📽️ Quick Reference:** See Lecture 1 Slides (01-fundamentals-and-tools-marp.html) for a condensed overview and live demos.

## Git & Version Control

### What is Git?

Git is a distributed version control system that tracks changes in files and coordinates work between multiple developers. It's essential for:

- **Tracking Changes:** Every modification to your code is recorded
- **Collaboration:** Multiple people can work on the same project simultaneously
- **Backup:** Your code history is preserved and can be recovered
- **Branching:** Work on features in isolation before merging

### Basic Git Concepts

```bash
# Clone a repository
git clone https://github.com/username/repository.git

# Check status of your changes
git status

# Add files to staging area
git add filename.py
git add .  # Add all changes

# Commit changes with a message
git commit -m "Add data processing function"

# Push changes to remote repository
git push origin main
```

### Branching Strategy

```bash
# Create and switch to a new branch
git checkout -b feature/data-analysis

# Work on your changes...
# Commit your changes...

# Switch back to main branch
git checkout main

# Merge your feature branch
git merge feature/data-analysis
```

## GitHub Workflow

### Repository Structure

Our course follows this repository pattern:

```
visdat-course/
├── docs/           # Course documentation (Docusaurus)
├── slides/         # Lecture slides (Marp)
├── assignments/    # Student assignments
├── examples/       # Code examples
├── data/          # Sample datasets
└── README.md      # Project overview
```

### Pull Request Process

1. **Fork** the main repository to your GitHub account
2. **Clone** your fork to your local machine
3. **Create a branch** for your work
4. **Make changes** and commit them
5. **Push** your branch to your fork
6. **Create a Pull Request** back to the main repository
7. **Review** and iterate based on feedback
8. **Merge** once approved

### Pull Request Best Practices

- **Clear Title:** Describe what the PR accomplishes
- **Detailed Description:** Explain the changes and why they were made
- **Small, Focused Changes:** Easier to review and less likely to have conflicts
- **Test Your Code:** Ensure everything works before submitting

## Markdown

### Why Markdown?

Markdown is a lightweight markup language that's:

- **Easy to Learn:** Simple syntax for formatting text
- **Version Control Friendly:** Plain text that Git can track effectively
- **Universal:** Supported by GitHub, VS Code, Jupyter, and many other tools
- **Flexible:** Can be converted to HTML, PDF, slides, and more

### Essential Markdown Syntax

```markdown
# Main Heading
## Sub Heading
### Sub-sub Heading

**Bold text**
*Italic text*
`Code inline`

- Bullet point 1
- Bullet point 2
  - Nested bullet

1. Numbered list
2. Second item

[Link text](https://example.com)

![Image alt text](image.png)

```python (cpp, markdown, cs, bash)
# Code block with syntax highlighting
def process_data(data):
    return data.clean().transform()
``` (end of code block)

> Blockquote for important notes

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

### Documentation as Code

In this course, we treat documentation like code:

- **Version Controlled:** All docs are in Git repositories
- **Collaborative:** Multiple contributors through Pull Requests
- **Automated:** Documentation builds automatically from Markdown
- **Living Documents:** Updated alongside code changes

### Marp for Presentations

Marp converts Markdown to slide presentations:

#### Creating Slides
```markdown
---
marp: true
paginate: true
footer: "Your Footer"
---

# Slide Title

Content goes here

---

# Next Slide

More content
```

#### Exporting to HTML
**Method 1: VS Code Extension**
1. Install "Marp for VS Code" extension
2. Open your `.md` file
3. `Ctrl+Shift+P` → "Marp: Export slide deck"
4. Choose "HTML" format

**Method 2: Command Line**
```bash
# Install Marp CLI (one-time)
npm install -g @marp-team/marp-cli

# Export slides
marp presentation.md --html --output presentation.html
```

## Development Environment Setup

### Required Software

1. **Git:** Download from [git-scm.com](https://git-scm.com/)
2. **VS Code:** Download from [code.visualstudio.com](https://code.visualstudio.com/)
3. **Python:** Download from [python.org](https://python.org/) (version 3.8+)
4. **Node.js:** Download from [nodejs.org](https://nodejs.org/) (for documentation tools)

### Git Configuration (First Time Setup)

⚠️ **IMPORTANT:** Before making your first commit, configure Git with your identity:

```bash
# Set your name and email (required for commits)
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global user.name
git config --global user.email
```

> **Note:** Use the same email address associated with your GitHub account. This ensures your commits are properly linked to your GitHub profile.

### VS Code Extensions

Install these extensions for the best development experience:

**Essential Extensions:**
- **C/C++** (Microsoft)
- **C/C++ Themes** (Microsoft)
- **Git Graph** (mhutchie)
- **GitHub Pull Requests and Issues** (GitHub)
- **Marp for VS Code**
- **Python** (Microsoft)
- **Python Debugger** (Microsoft)
- **Python Environments** (Microsoft)
- **Pylance** (Microsoft)

**What they do:**
- **C/C++**: Language support and IntelliSense for C++
- **Git Graph**: Visual git history and branching
- **GitHub Pull Requests**: Complete GitHub workflow integration
- **Marp**: Create and preview Markdown presentations
- **Python**: Python language support with IntelliSense
- **Pylance**: Fast, feature-rich Python language server

**Installation:**
1. Open VS Code
2. Go to Extensions view (`Ctrl+Shift+X`)
3. Search for each extension by name
4. Click "Install" for each one

### SSH Key Setup

For secure Git operations:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard (Windows)
type ~/.ssh/id_ed25519.pub | clip

# Add to GitHub: Settings > SSH and GPG keys > New SSH key
```

## Project Workflow Example

### Starting a New Assignment

```bash
# 1. Fork the course repository on GitHub
# 2. Clone your fork
git clone git@github.com:yourusername/visdat-course.git

# 3. Navigate to project
cd visdat-course

# 4. Create feature branch
git checkout -b assignment/week1-data-processing

# 5. Work on your assignment
# Edit files, create new ones, etc.

# 6. Commit your work
git add .
git commit -m "Complete week 1 data processing assignment"

# 7. Push to your fork
git push origin assignment/week1-data-processing

# 8. Create Pull Request on GitHub
```

### Continuous Integration

Our repositories use automated checks:

- **Code Quality:** Linting and formatting checks
- **Tests:** Automated testing of code examples
- **Documentation:** Ensure documentation builds correctly
- **Security:** Scan for potential security issues

## Best Practices

### Commit Messages

Write clear, descriptive commit messages:

```bash
# Good examples
git commit -m "Add data validation function for CSV imports"
git commit -m "Fix memory leak in image processing pipeline"
git commit -m "Update documentation for new API endpoints"

# Poor examples
git commit -m "fix stuff"
git commit -m "update"
git commit -m "changes"
```

### File Organization

- **Consistent Naming:** Use clear, descriptive file names
- **Logical Structure:** Group related files in folders
- **Documentation:** Include README.md files in each major directory
- **Ignore Files:** Use .gitignore to exclude temporary and build files

### Collaboration Etiquette

- **Review Others' Code:** Provide constructive feedback on Pull Requests
- **Ask Questions:** Use GitHub Issues for questions and discussions
- **Share Knowledge:** Document solutions to common problems
- **Be Patient:** Remember that everyone is learning

## Troubleshooting Common Issues

### Git Configuration Issues

**Problem:** `git commit` fails with error: "Please tell me who you are"

**Solution:** Configure your Git identity first:
```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"
```

### Git Problems

```bash
# Forgot to commit before pulling? Stash your changes
git stash
git pull
git stash pop

# Want to undo the last commit?
git reset --soft HEAD~1

# Accidentally committed to wrong branch?
git checkout correct-branch
git cherry-pick commit-hash
```

### Merge Conflicts

When Git can't automatically merge changes:

1. **Open the conflicted file** in VS Code
2. **Review the conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`)
3. **Choose which changes to keep** or combine them
4. **Remove the conflict markers**
5. **Commit the resolved file**

## Next Steps

Now that you understand the tools and workflow, you're ready to:

- Set up your development environment
- Fork the course repository
- Complete your first assignment
- Create your first Pull Request

The combination of Git, Markdown, and collaborative workflows will serve you well throughout this course and in your professional career!