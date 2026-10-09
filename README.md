# MLflow for Beginners

**A practical, beginner-friendly guide to machine learning experiment tracking and model management.**

Learn how to use MLflow step by step, from understanding the fundamentals to tracking experiments, comparing models, and working with saved machine learning models.

No prior experience with MLflow is required.

[Official MLflow Documentation](https://mlflow.org/docs/latest/) · [MLflow Tracking Quickstart](https://www.mlflow.org/docs/latest/ml/getting-started/quickstart/)

---

## Why this project?

Imagine training three machine learning models with different parameters. Each produces different results.

- Which model performed best?
- What parameters did you use?
- Can you reproduce the experiment later?
- Where did you save the trained model?

Without a systematic approach, keeping track of experiments can quickly become confusing.

**MLflow helps you organize and track machine learning experiments** by recording parameters, evaluation metrics, models, and other outputs. Its tracking interface makes it easier to inspect and compare your work.

This repository introduces these concepts through practical examples that you can run on your own computer.

## What you'll learn

- Understand what MLflow is and why it is useful.
- Set up MLflow in a Python environment.
- Create experiments and track individual runs.
- Log parameters, metrics, and artifacts.
- Explore experiment results using the MLflow UI.
- Use autologging with supported machine learning libraries.
- Compare models using evaluation metrics.
- Save, load, and manage trained models.
- Build a small end-to-end machine learning project.

## Learning roadmap

| Lesson | Topic | What you'll build or learn |
|---|---|---|
| 01 | Introduction to MLflow | Understand the concepts and terminology. |
| 02 | Installation and setup | Run MLflow locally on Windows. |
| 03 | Your first experiment | Train a classifier and log your first run. |
| 04 | Tracking fundamentals | Record parameters, metrics, tags, and artifacts. |
| 05 | Autologging | Automatically capture supported training information. |
| 06 | Comparing experiments | Compare models and evaluate their results. |
| 07 | Model management | Load saved models and explore model versioning. |
| 08 | Mini project | Apply the concepts in a complete workflow. |

Each lesson will include explanations, runnable code, step-by-step instructions, expected results, and exercises.

## Who is this for?

This repository is designed for:

- Students learning machine learning and MLOps.
- Python learners who want to improve their ML workflow.
- Beginners who want hands-on experience with MLflow.
- Developers who want to understand experiment tracking.

You should have basic Python knowledge and a general idea of how machine learning models are trained. You do not need previous MLflow experience.

## Prerequisites

Before starting, you will need:

- Python installed on your computer.
- A code editor, such as Visual Studio Code.
- Basic familiarity with Python scripts and the command line.
- A willingness to experiment, make mistakes, and learn.

**Platform:** Windows PowerShell is the primary environment used in these tutorials. Instructions for other platforms may be added later.

## Getting started

The recommended approach is to follow the lessons in order.

1. Read [Lesson 01 — Introduction to MLflow](01-introduction/README.md).
2. Follow [Lesson 02 — Installation and Setup](02-setup/README.md).
3. Run your first experiment in [Lesson 03 — Your First Experiment](03-first-experiment/README.md).

The lesson links will become available as the tutorials are added to the repository.

## Tools and technologies

- **Python** — machine learning implementation.
- **MLflow** — experiment tracking and model management.
- **scikit-learn** — beginner-friendly machine learning examples.
- **Git and GitHub** — version control and sharing the tutorials.

The initial examples will use a small, built-in classification dataset so you can focus on learning MLflow rather than spending time collecting and cleaning data.

## Repository structure

```text
mlflow-for-beginners/
├── README.md
├── requirements.txt
├── .gitignore
├── 01-introduction/
├── 02-setup/
├── 03-first-experiment/
├── 04-tracking-fundamentals/
├── 05-autologging/
├── 06-comparing-experiments/
├── 07-model-management/
├── 08-mini-project/
├── resources/
└── article/
```

Each lesson will have its own README, with code and supporting resources where needed.

## What makes this repository different?

This is intended to be a learning resource, not just a collection of code snippets.

- Concepts are explained in plain English.
- Commands are written for beginners and introduced step by step.
- Examples build on one another.
- Results are explored through the MLflow interface.
- Exercises encourage you to apply what you've learned.
- Common errors and troubleshooting tips are documented along the way.

Code examples and setup instructions will be tested as the lessons are developed.

## Further learning

- [Official MLflow Documentation](https://mlflow.org/docs/latest/)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking/)
- [MLflow Tracking Quickstart](https://www.mlflow.org/docs/latest/ml/getting-started/quickstart/)

## Project status

**In progress** — tutorials, examples, and setup instructions are being developed incrementally.

## Contributing and feedback

Found an issue or have a suggestion? Feel free to open a GitHub issue or suggest an improvement. The goal is to make MLflow easier for beginners to understand and use.

## Author

Created as a learning and portfolio project to explore machine learning experiment tracking, reproducibility, and MLOps fundamentals.

---

**Happy learning, and happy experimenting!**
