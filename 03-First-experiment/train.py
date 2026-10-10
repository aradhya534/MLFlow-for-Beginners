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