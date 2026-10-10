# Lesson 03: Your First MLflow Experiment

Time to write real code. In this lesson you will train a simple classifier on the Iris flower dataset and use MLflow to record the settings, the result, and the trained model. Then you will open the MLflow interface and find them.

> **Operating system:** commands are for **Windows 11 with Windows PowerShell**.
>
> **Version note:** this tutorial targets **MLflow 3.17.0**. In MLflow 3, a model is logged with `name="..."`. Many older tutorials use `artifact_path="..."` instead, so code copied from older sources may not match.

---

## 1. Learning objectives

By the end of this lesson you will be able to:

- Load a dataset and split it into training and test sets.
- Train a simple classification model with scikit-learn.
- Connect a script to the MLflow tracking server.
- Create an experiment and start a run.
- Log parameters, a metric, and a trained model.
- Find and read the results in the MLflow interface.

## 2. Prerequisites

- Completed [Lesson 02](../02-setup/README.md): virtual environment created, packages installed, and you can start the tracking server.
- The Iris dataset needs no download. It is built into scikit-learn.

**Files reused from earlier lessons:** `requirements.txt`, the `.venv` folder, and the server command from Lesson 02.

**New file in this lesson:** `03-first-experiment/train.py`.

## 3. Concepts in plain English

### The Iris dataset

The Iris dataset has 150 flowers from three species. Each flower has four measurements (sepal length, sepal width, petal length, petal width), and your job is to predict the species from the measurements. It is small, clean, and well known, which makes it a good first example. It is a **classification** problem: the model picks one of three classes.

### Training and test sets

You split the data into two parts. The model **learns** from the training set. You then **measure** how well it does on the test set, which it has not seen. This tells you how well it is likely to do on new flowers. We use 80% of the flowers for training and 20% (30 flowers) for testing.

### Accuracy

Accuracy is the share of test flowers the model classified correctly. If it gets 29 of 30 right, accuracy is 29 / 30 = 0.9667.

### What we will record in MLflow

| Kind | What we log | Why |
|------|-------------|-----|
| Parameters | `model_type`, `max_iter`, `test_size`, `random_state` | The settings that produced this result |
| Metric | `accuracy` | The result |
| Model | The trained model | So we can use it later |

## 4. Step-by-step instructions

### Step 1: Start the tracking server

Follow Step 7 of [Lesson 02](../02-setup/README.md#step-7-start-the-mlflow-tracking-server). In **PowerShell window 2**, from the repository root, with the environment active:

```powershell
mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

Leave this window open. If the server is already running from before, you do not need to start it again.

### Step 2: Create the script file

Inside the repository root, create a folder named `03-first-experiment` (if you cloned the repository, it already exists). Save the code from the next section as `train.py` inside that folder, so the full path is:

```text
mlflow-for-beginners\03-first-experiment\train.py
```

### Step 3: Run the script

Use **PowerShell window 1** (not the server window). Go to the repository root, activate the environment if needed, and run the command in [Section 8](#8-commands-to-run).

## 5. The complete code

Save this as `03-first-experiment/train.py`:

```python
"""Lesson 03: your first MLflow experiment.

Trains a logistic regression classifier on the Iris dataset and records
the settings, the result, and the trained model in MLflow.

Before running this script, start the MLflow tracking server (see Lesson 02).
"""

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# --- Settings -----------------------------------------------------------
TRACKING_URI = "http://127.0.0.1:5000"   # the server from Lesson 02
EXPERIMENT_NAME = "iris-first-experiment"
TEST_SIZE = 0.2
RANDOM_STATE = 42
MAX_ITER = 200

# --- 1. Connect to MLflow and choose an experiment ----------------------
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

# --- 2. Load the data and split it --------------------------------------
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

# --- 3. Train and track inside one MLflow run ---------------------------
with mlflow.start_run(run_name="logistic-regression-baseline"):
    # Parameters: the settings we chose
    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_param("max_iter", MAX_ITER)
    mlflow.log_param("test_size", TEST_SIZE)
    mlflow.log_param("random_state", RANDOM_STATE)

    # Train the model
    model = LogisticRegression(max_iter=MAX_ITER, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    # Evaluate on the test set
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Metric: the result we measured
    mlflow.log_metric("accuracy", accuracy)

    # Save the trained model with the run
    mlflow.sklearn.log_model(sk_model=model, name="iris_model")

print(f"Test accuracy: {accuracy:.4f}")
print(f"Open {TRACKING_URI} and select the 'Model training' view to see the run.")
```

## 6. The code, section by section

**Imports.** `mlflow` and `mlflow.sklearn` are for tracking. The `sklearn` imports are for the data, the model, the accuracy measure, and the train/test split. All the imports are at the top, so you can see everything the script depends on.

**Settings.** Values you may want to change are in capital letters at the top. This avoids typing the same value in several places.

**Step 1: connect.** `mlflow.set_tracking_uri(...)` tells the script where the server is. Without it, MLflow would write to a local folder instead of your server. `mlflow.set_experiment(...)` picks the experiment and creates it if it does not exist yet.

**Step 2: load and split.** `load_iris(return_X_y=True)` returns the measurements (`X`) and the species (`y`). `train_test_split` divides them:

- `test_size=0.2` keeps 20% for testing.
- `random_state=42` makes the split the same every time, so your results are repeatable.
- `stratify=y` keeps the same mix of species in the training and test sets. Without it, a small test set could end up with too few flowers of one species.

**Step 3: the run.** `with mlflow.start_run(run_name=...):` opens a run. Everything inside the indented block is recorded in that run, and the run closes automatically when the block ends, even if an error occurs.

Inside the run:

- `mlflow.log_param(...)` records each setting. Parameters are stored as text, so `0.2` appears as `0.2` and `200` as `200`.
- `model.fit(...)` trains the model on the training data.
- `accuracy_score(...)` compares the model's predictions on the test set with the true species.
- `mlflow.log_metric("accuracy", accuracy)` records the result.
- `mlflow.sklearn.log_model(sk_model=model, name="iris_model")` saves the trained model with the run, under the name `iris_model`. Lesson 07 shows how to load it again.

**The last two lines** print a summary. They are not part of MLflow.

## 7. Files and storage

Nothing new is created in the lesson folder when you run the script. The script sends everything to the server, which stores the data where it was started:

| What | Where |
|------|-------|
| Parameters, metric, run information | `mlflow.db` in the repository root |
| The saved model files | the `mlartifacts` folder in the repository root |

Both are ignored by Git.

## 8. Commands to run

In **PowerShell window 1**, from the repository root, with `(.venv)` showing:

```powershell
python 03-first-experiment\train.py
```

This runs the script. You can run it from any folder as long as you give the correct path to `train.py`, but the repository root is simplest.

## 9. Expected output

In the terminal, you should see something like this. The date, the experiment number, and the long run ID will be different on your machine:

```text
2026/10/10 21:16:23 INFO mlflow.tracking.fluent: Experiment with name 'iris-first-experiment' does not exist. Creating a new experiment.
View run logistic-regression-baseline at: http://127.0.0.1:5000/#/experiments/2/runs/<a-long-id>
View experiment at: http://127.0.0.1:5000/#/experiments/2
Test accuracy: 0.9667
Open http://127.0.0.1:5000 and select the 'Model training' view to see the run.
```

- The first line appears only the first time, when the experiment is created.
- MLflow prints a small symbol in front of the "View run" and "View experiment" lines.
- The experiment number depends on how many experiments already exist. In this output it is `2` because the `setup-check` experiment from Lesson 02 was created first.
- The accuracy should be `0.9667`, which is 29 of 30 test flowers correct. Because the split is fixed with `random_state=42`, running the script again gives the same accuracy.

### What to inspect in the MLflow UI

Open `http://127.0.0.1:5000` and make sure **Model training** is selected in the top-left switch (see the note in [Lesson 02, Step 8](../02-setup/README.md#step-8-open-the-web-interface)).

1. Find the experiment **iris-first-experiment** and open it.
2. You should see one run named **logistic-regression-baseline**. Open it.
3. Look for the four parameters: `model_type`, `max_iter`, `test_size`, and `random_state`.
4. Look for the metric `accuracy`.
5. Look for the logged model. Go back to the experiment page and open its **Models** tab. A model from this run is listed there. In the code, you saved it with `name="iris_model"`.
6. Look at the details MLflow added on its own, such as the run's status and start time. You did not log these. MLflow records them automatically, and Lesson 04 explains more.

## 10. Common errors and solutions

| Problem | Cause and fix |
|---------|---------------|
| The script seems to freeze, then fails with `API request to http://127.0.0.1:5000/... failed` | The server is not running. Start it (Step 1) and run the script again. See [Lesson 02](../02-setup/README.md#10-common-errors-and-solutions) |
| `ModuleNotFoundError: No module named 'mlflow'` (or `sklearn`) | The environment is not active. Run `.\.venv\Scripts\Activate.ps1` and try again |
| `can't open file ... train.py` | You are in the wrong folder, or the path is wrong. Run `Get-Location` and check that `03-first-experiment\train.py` exists below it |
| The web page shows "Traces", "Sessions", or "No data available" | You are in the **GenAI** view. Click **Model training** at the top-left |
| I cannot find my experiment | Check the experiment name for typos. A different name creates a different experiment. Also check that the server was started from the repository root (Lesson 02) |
## 11. Practice exercises

1. **Run it again.** Run the script a second time. How many runs does the experiment have now? Is the accuracy the same? Why?
2. **Change a parameter.** Set `MAX_ITER = 100`, run the script, and compare the two runs in the UI. Did the accuracy change?
3. **Change the split.** Set `TEST_SIZE = 0.3`, run the script, and look at the `test_size` parameter in the new run.
4. **Change the seed.** Set `RANDOM_STATE = 7`, run the script, and see whether the accuracy changes. What does that tell you about a single accuracy number from a small test set?

## 12. Small challenge

Create a copy of `train.py` called `train_knn.py` in the same folder. Replace `LogisticRegression` with scikit-learn's `KNeighborsClassifier` (imported from `sklearn.neighbors`), and log `n_neighbors` as a parameter instead of `max_iter`. Give it a different `run_name` and change `model_type` to match. Run it, then find both runs in the same experiment.

## 13. Summary

- A script connects to the server with `mlflow.set_tracking_uri(...)` and chooses an experiment with `mlflow.set_experiment(...)`.
- `with mlflow.start_run():` opens a run, and everything logged inside belongs to it.
- `log_param` records settings, `log_metric` records results, and `log_model` saves the trained model.
- A fixed `random_state` makes the split, and so the result, repeatable.
- Each time you run the script, a new run is created in the same experiment.
- Results are viewed in the **Model training** view of the MLflow interface.

## 14. Next lesson and official documentation

**Next:** [Lesson 04: Understanding Experiment Tracking](../04-tracking-fundamentals/README.md) (planned). It extends this same example.

Official documentation for this lesson:

- [MLflow Tracking Quickstart](https://mlflow.org/docs/latest/ml/tracking/quickstart/)
- [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/)
- [Tracking APIs](https://mlflow.org/docs/latest/ml/tracking/tracking-api/)

---

## Testing status

| Part | Status |
|------|--------|
| `train.py` runs without errors or warnings against a SQLite-backed MLflow 3.17.0 server, and the logged parameters, metric, and model were read back | Run successfully on **Linux** (test environment). Accuracy `0.9667`, identical on a second run |
| `train.py` on Windows 11 (PowerShell, Python 3.13.3) | Run successfully, reported by the author. Same output as on Linux, accuracy `0.9667`, no warnings |
| Results in the Model training view | Confirmed by the author on Windows: the four parameters and the `accuracy` metric are shown on the run, and the model is listed in the experiment's Models tab |