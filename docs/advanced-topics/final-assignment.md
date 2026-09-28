---
title: Final Assignment
sidebar_position: 3
---

# Final Assignment - Individual Project

## Overview

The final assignment is an **individual project** where you demonstrate your skills in scientific data handling and visualization. You have the freedom to choose a project that interests you, as long as it involves meaningful data processing or visualization with appropriate complexity.

**Deadline:** announced in class (Pull Request submission, end of January)  
**Presentation:** Last January session (each student presents their work)

## Project Requirements

### 1. Individual Work

This is an **individual assignment**. While you can discuss concepts with classmates, your code and implementation must be your own work.

### 2. Topic Flexibility

You may work on:
- **Extension of semester projects**: Add functionality or complexity to work done during the course (GUI features, data processing pipelines, visualization enhancements)
- **New project**: Create something original related to scientific data handling/visualization
- **Real-world application**: Solve a problem from your thesis, research, or professional work

:::tip Project Ideas
- Extend the FEM viewer with advanced features (clipping planes, multiple views, animation)
- Build a data analysis dashboard for specific engineering data
- Create interactive 3D visualizations of simulation results
- Implement parallel data processing pipelines
- Develop custom data format converters
- Build specialized plotting tools for your field
:::

### 3. Complexity

Your project should demonstrate **significant effort** and mastery of course concepts. Consider including:
- Multiple integrated components (data loading, processing, visualization)
- User interaction or GUI elements
- Performance optimization or parallel processing
- Proper error handling and code organization
- Clean, documented, maintainable code

Projects that are "too simple" (e.g., basic plot script with no additional features) will not receive full credit.

### 4. Code Must Run

**Critical requirement**: Your code must run on the instructor's machine without additional dependencies beyond what's in the course environment.

:::warning Dependency Management
- Use only libraries already in `requirements.txt` **OR**
- If you need additional packages, include an updated `requirements.txt` in your submission folder
- Document any special setup steps clearly in your README
- Test your code in a fresh virtual environment before submission
:::

### 5. Documentation

Your project must be **well-documented** so it's clear:
- What your project does
- How to run it
- What problems it solves
- What technologies/techniques you used
- Evidence of substantial work and thought

## Deliverables

### Folder Structure

The final assignment goes into the `final/` subfolder of your submission folder
in the submissions repository, next to the assignments you handed in during the
semester:

```
visdat-abgaben-ws2627/
└── submissions/
    └── your-github-username/
        ├── 01-kickoff/               # Your earlier submissions
        ├── ...
        └── final/
            ├── README.md             # Project documentation
            ├── code/                 # Your implementation
            │   ├── main.py           # Entry point (if applicable)
            │   ├── src/              # Source modules
            │   ├── data/             # Sample data files (if small)
            │   └── requirements.txt  # Additional dependencies (if needed)
            ├── slides.md             # Marp presentation slides
            └── assets/               # Images, screenshots for slides
                └── screenshots/
```

:::note Folder Naming
This is the folder you created during the kickoff assignment, named after your
GitHub username. Use it, and do not create a second one.
:::

:::warning File size
No file may be larger than 5 MB, and the automatic check rejects pull requests
that contain one. If your project needs large input data, commit a small sample
and describe in your README where the full dataset comes from.
:::

### 1. Working Code

- **Entry point**: Clear starting point (e.g., `python main.py` or `python run_application.py`)
- **Organized structure**: Separate modules/files for different functionality
- **Comments**: Explain non-obvious code sections
- **Error handling**: Graceful handling of common errors
- **Clean code**: Follow Python conventions (PEP 8)

### 2. README.md

Document your project thoroughly. Your README should include:

**Project Title**
- Brief description of what your project does and why

**Features**
- List main features/capabilities
- Highlight interesting aspects

**Technologies Used**
- Python libraries (NumPy, PyQt6, PyVista, etc.)
- Any special techniques (parallel processing, custom algorithms)

**Installation & Setup**
```bash
cd submissions/your-folder/final/code
pip install -r requirements.txt  # if needed
```

**Usage**
```bash
python main.py
# Or describe GUI workflow steps
```

**Data**
- What data does it use?
- Where is sample data located?
- Format/structure of expected data

**Implementation Details**
- Interesting algorithms or approaches
- Challenges you solved
- Performance considerations

**Screenshots**
- Include screenshots showing your application in action

**Future Improvements** (optional)
- Ideas for extending the project

### 3. Presentation Slides (Marp)

Create `slides.md` using Marp format for your presentation:

```markdown
---
marp: true
theme: default
paginate: true
---

# Your Project Title
**Your Name**
Visualization & Data Processing - Final Project

---

## Problem / Motivation
- What problem are you solving?
- Why is this useful?

---

## Approach
- High-level overview of your solution
- Key technologies used

---

## Implementation Highlights
- Interesting code/algorithm details
- Screenshots of your application

---

## Demo
Live demonstration or video/GIF

---

## Results
- What works well
- Performance metrics (if applicable)

---

## Challenges & Solutions
- What was difficult
- How you overcame it

---

## Lessons Learned
- What you learned from this project
- Skills you developed

---

## Thank You
Questions?
```

Aim for **5-8 minutes total** presentation time, including any live demo or code walkthrough.

## Grading Criteria

Your project will be evaluated on:

### Individual Ideas & Creativity (30%)
- Originality and personal contribution
- Problem-solving approach
- Going beyond basic requirements

### Code Quality & Functionality (40%)
- **Does it run?** (Critical - code must execute without errors)
- Code organization and structure
- Proper error handling
- Performance and efficiency
- Appropriate use of course concepts

### Documentation & Presentation (30%)
- Clear README with setup/usage instructions
- Well-structured presentation
- Demonstrates understanding of what you built
- Evidence of substantial effort and time investment

:::tip Success Criteria
**Must Have:**  
✓ Runs on instructor's machine  
✓ Clear documentation of what it does  
✓ Demonstrates significant effort  
✓ Uses concepts from course  

**Nice to Have:**  
✓ Solves real problem elegantly  
✓ Clean, maintainable code  
✓ Good performance  
✓ Impressive presentation  
:::

## Submission Process

1. **Develop locally** in the submissions repository, on a branch created for
   this assignment:
   ```bash
   git checkout main
   git pull
   git checkout -b submission/final/[your-github-username]
   ```
2. **Test thoroughly** in a fresh environment
3. **Commit in small steps** while you work, not once at the end:
   ```bash
   git add submissions/[your-folder]/final/
   git commit -m "Add mesh comparison view to the results window"
   git push -u origin submission/final/[your-github-username]
   ```
4. **Create Pull Request** against `main` of the submissions repository:
   - Title: `Final Assignment - [Your Name]`
   - Fill in the pull request template, including the section on AI tools
   - Deadline: see above

5. **Check that the automatic check passes.** It verifies that your pull request
   only touches your own folder and that no file is too large. If it fails, push
   a fix to the same branch.

6. **Prepare presentation** for the last January session

The complete workflow is described in
[Submission Workflow](../tools-workflow/submission-workflow.md).

## Timeline

- **Now - January**: Work on your project
  - Use January sessions for development and questions
  - Work at home as needed
  - Test your code regularly

- **End of January, exact date announced in class**: Pull Request deadline
  - All code must be committed
  - Documentation complete
  - Presentation slides ready

- **Last January Session**: Presentations
  - Each student presents (5-8 minutes)
  - Live demo or recorded demonstration
  - Q&A with instructor and peers

## Tips for Success

### Start Early
Don't underestimate the time needed for:
- Planning and design
- Implementation and debugging
- Testing in clean environment
- Writing documentation
- Creating presentation

### Keep It Focused
Better to do one thing really well than many things poorly:
- ✓ Small, polished project with excellent documentation
- ✗ Large, buggy project with poor documentation

### Test on Clean Environment
Before submission:
```bash
# Create fresh virtual environment
python -m venv test_env
test_env\Scripts\activate
pip install -r requirements.txt

# Test your code
python main.py
```

### Ask Questions
- Use January sessions to get feedback
- Ask about technical approaches
- Clarify requirements if unclear

### Version Control
- Commit regularly (not just once at the end)
- Use meaningful commit messages
- Start each assignment from an up to date `main`

## Example Project Scopes

### Appropriate Complexity

**Good examples:**
- Interactive FEM results viewer with field selection, deformation, clipping, and export
- Batch data processing pipeline with parallel execution and progress tracking
- Time-series analysis dashboard with multiple plot types and filtering
- 3D mesh comparison tool with difference visualization
- Custom data format converter with validation and error reporting

**Too simple:**
- Single script that makes one plot
- Basic calculator with GUI
- Simple file reader without processing
- Minimal examples from documentation

**Too ambitious for timeframe:**
- Complete FEM solver implementation
- Large machine learning framework
- Full-featured CAD application

Aim for something that shows mastery of 2-3 major course topics and demonstrates thoughtful engineering.

## FAQs

**Q: Can I use libraries not covered in class?**  
A: Yes, but include them in `requirements.txt` and ensure they install easily via pip.

**Q: Can I work on a project related to my thesis?**  
A: Absolutely! Just ensure it demonstrates course concepts appropriately.

**Q: What if my code doesn't completely work?**  
A: Document what works, what doesn't, and what you tried. Partial credit for effort and learning.

**Q: How long should my presentation be?**  
A: Aim for 5-8 minutes. Practice beforehand to stay within time.

**Q: Can I use C++ code?**  
A: Yes, if integrated with Python and documented clearly. But Python-focused projects are recommended.

**Q: Do I need to present live demos?**  
A: Live demos are great but risky. Pre-record a backup video or use screenshots.

## Resources

### Course Materials
- Review all documentation on this site
- Reference example projects from workshops
- Consult assignment examples from semester

### External Resources
- [Real Python](https://realpython.com/) - Python tutorials
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [PyVista Examples](https://docs.pyvista.org/examples/index.html)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)

### Getting Help
- Email instructor with specific questions
- Use January sessions for feedback

---

**Good luck with your final project! This is your chance to showcase what you've learned and create something you're proud of.**

