---
title: Submission Workflow
---

# Submission Workflow

Every assignment in this course is submitted as a pull request. This page
describes the workflow once, so that the individual assignments only need to
describe their content. Read it before your first submission and come back to it
whenever you start a new assignment.

## Two repositories

The course uses two repositories, and it matters which one you work in.

**Course material**, public: [github.com/soberpe/visdat-course](https://github.com/soberpe/visdat-course)

This is the repository behind the site you are reading. It holds the script, the
slides and the sample datasets. You clone it to have the data available locally.
You do not change anything in it. If you find a mistake, open an issue.

**Submissions**, private: `soberpe/visdat-abgaben-ws2627`

This is where your work goes. You are invited as a collaborator at the start of
the semester, so you work in it directly and do not need a fork. It is private,
which means your submissions are visible to you, your fellow students and the
lecturer, and to nobody else.

:::warning Keep your work out of the public repository
Never push your assignments to the course material repository, and never open a
pull request against it. Everything you hand in belongs in the private
submissions repository.
:::

## Your submission folder

You own exactly one folder under `submissions/`, named after your GitHub
username in lowercase:

```
submissions/
└── your-github-username/
    ├── 01-kickoff/
    ├── 02-data-processing/
    ├── 03-imu-workshop/
    ├── 04-mesh-visualization/
    ├── 05-fem-challenge/
    ├── 06-qt-workshop/
    └── final/
```

All students submit into the same repository. If several people changed the same
file, their submissions would conflict and none of them could be merged. The
folder rule avoids this: your changes never overlap with anyone else's, so your
pull request can always be merged, and a merged pull request is the confirmation
that your submission was accepted.

This mirrors how teams work on shared code in practice. The rules feel formal at
first, but they exist for the same reason they exist in industry: they keep a
shared repository reviewable when many people contribute at the same time.

## Protect your email address

Git writes your name and email address into every commit, and those stay in the
history permanently. Before your first commit, switch on email privacy in your
GitHub account settings:

1. **Settings → Emails**: enable *Keep my email addresses private* and
   *Block command line pushes that expose my email*.
2. Copy the `@users.noreply.github.com` address shown there.
3. Use it for your commits:

```bash
git config --global user.name "Your Real Name"
git config --global user.email 12345678+username@users.noreply.github.com
```

Your name should be your real name, so that your work can be attributed to you.
Your university address does not belong in a commit history, because it contains
your student ID.

## One branch per assignment

Create a new branch for every assignment, and create it from an up to date
`main`:

```bash
cd visdat-abgaben-ws2627

git checkout main
git pull

git checkout -b submission/kickoff/your-github-username
```

The naming scheme is `submission/<assignment>/<your-github-username>`.

:::tip Why a fresh branch each time
If you keep working on one long living branch, every later commit ends up in the
same pull request. The diff then covers the whole semester instead of one
assignment, and it can no longer be reviewed. A fresh branch keeps your pull
request limited to the work it is about.
:::

## Submitting

1. Commit your work in small steps while you are working, not once at the end.
   Write commit messages that say what changed.
2. Push your branch:
   ```bash
   git push -u origin submission/kickoff/your-github-username
   ```
3. Open a pull request from your branch to `main`.
4. Fill in the pull request template. It appears automatically, so you only have
   to replace the placeholders.
5. Wait for the automatic check and for the review.

:::note One pull request per assignment
If you need to correct something after submitting, push more commits to the same
branch. They appear in the same pull request automatically. Do not open a second
pull request for the same assignment.
:::

## The automatic check

Every pull request runs a check that verifies three things:

1. All changed files are inside your own folder under `submissions/`.
2. No file is larger than 5 MB.
3. No template placeholder such as `[Your Name]` is left in your files.

If the check fails, open it through the **Details** link in the pull request and
read the summary. It names the file and the change that is needed. Push a fix to
the same branch and the check runs again.

The check also reports warnings, which do not block the merge. One of them
appears when your commits carry the example identity from the kickoff assignment
instead of your real name.

:::warning Large files
Git stores every version of every file forever. A 50 MB result file committed
once stays in the repository history of everyone who clones it, even after you
delete it. Keep sample data small, store only the data your code actually needs,
and generate large intermediate results with a script instead of committing them.
:::

## Review and acceptance

The lecturer reviews your pull request and may ask questions or request changes
directly in it. Answer in the pull request and push your corrections to the same
branch. This discussion is part of the assignment, not an extra step: being able
to explain and defend your own work is one of the learning goals of this course.

When the submission is accepted, the pull request is merged.

## Checklist

Before you open a pull request:

- [ ] I am working in the submissions repository, not in the course material
- [ ] All my changes are inside `submissions/<my-github-username>/`
- [ ] My branch was created from an up to date `main`
- [ ] My commits carry my real name and a protected email address
- [ ] No template placeholders are left in my files
- [ ] No file is larger than 5 MB
- [ ] My code runs in a fresh virtual environment
