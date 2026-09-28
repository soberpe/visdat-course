---
title: Course Organization
---

# Course Organization

## Course Overview

**Course Title:** Visualization & Data Processing (VIS3VO)  
**Program:** FH OÖ Wels · Master Mechanical Engineering  
**Semester:** 3rd Semester  
**Lecturer:** Stefan Oberpeilsteiner

## Course Goals

This course aims to provide students with comprehensive skills in modern data processing and visualization:

### Primary Objectives

- Build **robust data pipelines** that can handle real-world engineering data
- Create **clear, meaningful visualizations** that communicate insights effectively
- Work with **3D content** using libraries like VTK, PyVista, and formats like glTF
- Design **interactive user interfaces** using Qt/PyQt, Dash, and other frameworks
- Practice **version control** and ensure reproducibility in all projects

### Learning Outcomes

By the end of this course, students will be able to:

- Design and implement end-to-end data processing workflows
- Choose appropriate visualization techniques for different types of engineering data
- Work collaboratively using Git and GitHub workflows
- Build interactive applications for data exploration
- Handle various data formats commonly used in engineering (HDF5, CSV, JSON, etc.)
- Apply both procedural and object-oriented programming paradigms effectively

## Course Structure

### Weekly Topics Overview

1. **Week 1-3:** Introduction & Tools (Git, Markdown, Python/C++ basics)
2. **Week 4:** Data formats, Pandas/Polars, HDF5
3. **Week 5:** 2D Visualization (Matplotlib/Plotly)
4. **Upcoming weeks:** 3D content, interactive UIs, advanced topics

### Learning Approach

The course follows a **hands-on, project-based approach**:

- **Theory + Practice:** Each concept is immediately applied in practical exercises
- **Collaborative Learning:** Work in teams using industry-standard Git workflows
- **Real-world Problems:** Projects based on actual engineering scenarios
- **Iterative Improvement:** Continuous feedback through pull request reviews

## Workflow & Collaboration

### Repository-Based Learning

1. **Course Content:** The script, the slides and the sample data live in a public GitHub repository
2. **Student Work:** Submissions go into a separate private repository in which every student is a collaborator
3. **Submission:** Create Pull Requests for assignment submissions
4. **Review Process:** Instructor review in the Pull Request before merging
5. **Documentation:** All course materials written in Markdown for easy collaboration

### Submission Rules

All assignments are submitted the same way. The workflow is described in detail
in [Submission Workflow](./tools-workflow/submission-workflow.md), and these are
the rules it comes down to:

- Your work goes into the **private submissions repository**, never into the
  public course material.
- You own one folder there, named after your GitHub username in lowercase, and
  you work only inside it.
- Every assignment gets its own branch, named
  `submission/<assignment>/<your-github-username>`, created from an up to date
  `main`.
- One Pull Request per assignment. Corrections are pushed to the same branch,
  never submitted as a second Pull Request.
- Every Pull Request runs an automatic check. It has to pass before the
  submission is reviewed.
- A merged Pull Request means the submission was accepted.

:::info Why submissions are private
Submissions carry your name, your GitHub account and your own work. Keeping them
in a private repository means they stay visible to you, your fellow students and
the lecturer, and to nobody else. The course material stays public, so you can
keep using it after the course.
:::

:::tip Why the folder rule matters
More than twenty students submit into the same repository. As long as everyone
stays inside their own folder, no two submissions can conflict and every one of
them can be merged. This is the same reason why teams in industry split a shared
repository into clearly owned areas.
:::

### Version Control Benefits

- **Reproducibility:** Every change is tracked and can be recreated
- **Collaboration:** Multiple students can work on the same project safely
- **Learning History:** Students can see their progress over time
- **Industry Preparation:** Mirror professional software development practices

## Assessment & Grading

*Detailed grading criteria and assignment weights will be provided in subsequent course materials.*

## Resources & Prerequisites

### Required Tools

- **Git:** Version control system
- **GitHub Account:** For repository hosting and collaboration
- **Python:** Primary programming language for data processing
- **C++:** For performance-critical components
- **VS Code:** Mandatory development environment

### Recommended Background

- Basic programming experience in any language
- Fundamental understanding of data structures
- Willingness to learn new tools and technologies

## Getting Help
- **MS Teams:** Stefan Oberpeilsteiner (in FH OÖ tenant)
- **Email:** [stefan.oberpeilsteiner@fh-wels.at](mailto:stefan.oberpeilsteiner@fh-wels.at)
- **Course Repository:** Use Issues for technical questions
- **Peer Learning:** Collaborate through Pull Request discussions
- **Documentation:** Comprehensive guides available in this documentation site