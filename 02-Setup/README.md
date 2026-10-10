# Lesson 02: Installation and Setup

In this lesson you will get a working MLflow setup on your computer: a virtual environment, the right packages, and a running MLflow tracking server with its web interface. By the end you will log a tiny test run and see it in your browser.

> **Operating system:** every command in this lesson is for **Windows 11 with Windows PowerShell**. Other systems use different commands and are not covered here.
>
> **Version note:** this tutorial targets **MLflow 3.17.0** on **Python 3.13**. See the [root README](../README.md#technology-stack) for all versions.

---

## 1. Learning objectives

By the end of this lesson you will be able to:

- Check which Python version you have.
- Create, activate, and deactivate a virtual environment.
- Install the exact package versions used in this tutorial.
- Explain the difference between local file tracking and a tracking server.
- Start and stop the MLflow tracking server and open its web interface.
- Run a Python script that logs a run to the server.
- Fix the most common setup problems.

## 2. Prerequisites

- Completed [Lesson 01](../01-introduction/README.md).
- A Windows 11 computer with Python 3.13 installed.
- Git installed, if you want to clone the repository. You can also download the repository as a ZIP file from GitHub.

## 3. Concepts in plain English

### What is a virtual environment?

A **virtual environment** is a private folder of Python packages for one project. Without one, every project on your computer shares the same packages, and a package update for one project can break another. With one, this tutorial gets its own set of packages with the exact versions it needs.

### Two ways MLflow can store your data

MLflow always needs somewhere to keep two kinds of information:

- **Metadata:** parameters, metrics, tags, run names. Small pieces of information.
- **Artifacts:** files such as trained models.

You can set this up in two main ways:

| | Local file tracking | Tracking server (used in this tutorial) |
|---|---|---|
| How it works | Your script writes files directly into a local folder (by default `mlruns`) | A separate MLflow program runs in the background. Your script sends data to it, and it stores the data |
| Web interface | Start it separately when you want to look | Built in, always available while the server runs |
| Extra setup | None | Start the server in a second terminal window |
| Model Registry (Lesson 07) | Needs a database-backed store, so not available with plain files | Available when the server uses a database |

The official documentation describes the default as logging to a local `mlruns` directory, and says the Model Registry requires a database-backed store ([MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/)).

### The configuration used in this tutorial

Every lesson from here on uses the same setup:

| Setting | Value |
|---------|-------|
| Server address | `http://127.0.0.1:5000` |
| Metadata storage | A SQLite database file named `mlflow.db` |
| Artifact storage | A folder named `mlartifacts` |
| Where the server is started | The **repository root folder** |

SQLite is a small database stored in a single file, and it needs no installation. Using a database from the start means the Model Registry in Lesson 07 works without changing your setup.

`127.0.0.1` means "this computer". The server is reachable only from your own machine.

## 4. Step-by-step instructions

Every command below is run in **Windows PowerShell**. To open it, press the Windows key, type `PowerShell`, and press Enter.

### Step 1: Check your Python version

```powershell
python --version
```

This prints the version of Python that PowerShell finds. This tutorial was tested with **Python 3.13.3**.

If you see an error such as `python is not recognized`, Python is not installed or not on your PATH. See [Common errors](#10-common-errors-and-solutions).

To see all Python versions installed on your computer, you can also run:

```powershell
py -0p
```

### Step 2: Get the project folder

If you are following along from the GitHub repository, clone it (replace the placeholder with the real address):

```powershell
git clone <repository-url>
cd mlflow-for-beginners
```

`git clone` downloads a copy of the repository. `cd` ("change directory") moves PowerShell into that folder.

If you are creating the project from scratch instead:

```powershell
mkdir mlflow-for-beginners
cd mlflow-for-beginners
```

From now on, **the repository root** means this `mlflow-for-beginners` folder. You can check where you are at any time with:

```powershell
Get-Location
```

### Step 3: Create a virtual environment

Run this in the repository root:

```powershell
python -m venv .venv
```

This creates a folder named `.venv` containing a private copy of Python. The folder is listed in `.gitignore`, so it is never committed to Git.

### Step 4: Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

When it works, your prompt starts with `(.venv)`, like this:

```text
(.venv) PS C:\...\mlflow-for-beginners>
```

That prefix tells you the environment is active. **You must activate the environment in every new PowerShell window** before running tutorial commands.

If you get an error about running scripts being disabled, see [Common errors](#10-common-errors-and-solutions).

To leave the environment later:

```powershell
deactivate
```

### Step 5: Install the required packages

Make sure `(.venv)` is showing, then run:

```powershell
python -m pip install -r requirements.txt
```

This reads the file `requirements.txt` and installs the exact versions listed there. It can take a few minutes. The file contains:

```text
mlflow==3.17.0
scikit-learn==1.9.1
pandas==3.0.6
numpy==2.5.3
```

Using `python -m pip` instead of plain `pip` makes sure packages go into the Python that is currently active.

### Step 6: Verify the installation

```powershell
python -m pip check
```

Expected output:

```text
No broken requirements found.
```

Then check that everything imports and that you have the expected versions:

```powershell
python -c "import mlflow, sklearn, pandas, numpy; print(mlflow.__version__, sklearn.__version__, pandas.__version__, numpy.__version__)"
```

Expected output:

```text
3.17.0 1.9.1 3.0.6 2.5.3
```

If your numbers differ, repeat Step 5 and make sure `(.venv)` is showing.

### Step 7: Start the MLflow tracking server

Open a **second PowerShell window**. Keep your first window open too.

In the **second window**, move to the repository root and activate the environment:

```powershell
cd <path-to>\mlflow-for-beginners
.\.venv\Scripts\Activate.ps1
```

Then start the server:

```powershell
mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

What the options mean:

| Option | Meaning |
|--------|---------|
| `--backend-store-uri sqlite:///mlflow.db` | Store metadata in a SQLite file named `mlflow.db` in the current folder |
| `--host 127.0.0.1` | Accept connections only from this computer |
| `--port 5000` | Listen on port 5000 |

The server keeps running and prints log lines. **That is normal.** The window will not give you a prompt back while the server is running, which is why you use a second window for everything else.

Because artifact serving is on by default, the server stores artifacts in a local `mlartifacts` folder in the folder where it was started ([Tracking Server documentation](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/)). This is why you start the server from the repository root: `mlflow.db` and `mlartifacts` are created there, and Git ignores both.

### Step 8: Open the web interface

Open your browser and go to:

```text
http://127.0.0.1:5000
```

You should see the MLflow interface. There is nothing in it yet except a default experiment. That is expected.

> **Two views: GenAI and Model training.** In MLflow 3.17.0, the top-left of the interface (under the version number) has a switch with two options: **GenAI** and **Model training**. GenAI is for tracing LLM and agent applications. This tutorial is about training ordinary machine learning models, so **always use Model training**. If you land on a page with "Traces", "Sessions", or "No data available", you are in the GenAI view. Click **Model training** to switch.

### Step 9: Run a Python script that logs to the server

Go back to your **first PowerShell window** (the one with `(.venv)` showing, not the server window). Make sure you are in the repository root, then run:

```powershell
@'
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("setup-check")

with mlflow.start_run(run_name="hello-mlflow"):
    mlflow.log_param("greeting", "hello")
    mlflow.log_metric("answer", 42)

print("Logged one run. Open http://127.0.0.1:5000 to see it.")
'@ | python -
```

This sends a small Python program straight to Python, so you do not need to create a file. (From Lesson 03 onward you will use real script files.) Be careful to copy everything, including the first line `@'` and the last line `'@ | python -`, and make sure `'@` is at the very start of its line.

What the code does:

- `mlflow.set_tracking_uri(...)` tells your script to send data to the server you started.
- `mlflow.set_experiment("setup-check")` selects the experiment, creating it if needed.
- `mlflow.start_run(run_name="hello-mlflow")` opens a run with a readable name.
- `mlflow.log_param(...)` and `mlflow.log_metric(...)` record one parameter and one metric.

## 5. Expected output

In the script window you should see lines similar to these (the long ID will be different):

```text
View run hello-mlflow at: http://127.0.0.1:5000/#/experiments/1/runs/<a-long-id>
View experiment at: http://127.0.0.1:5000/#/experiments/1
Logged one run. Open http://127.0.0.1:5000 to see it.
```

MLflow may add small symbols in front of the first two lines. The exact text can vary.

## 6. What to inspect in the MLflow UI

Refresh `http://127.0.0.1:5000` in your browser, make sure **Model training** is selected (see the note in Step 8), and check:

1. An experiment named **setup-check** appears in the list.
2. Click it. A run named **hello-mlflow** is listed.
3. Click the run. You should see the parameter `greeting = hello` and the metric `answer = 42`.

Back in your repository folder, you should also now see `mlflow.db` and, once a model has been logged (from Lesson 03), a `mlartifacts` folder.

## 7. Stopping the server

In the **server window**, press **Ctrl+C**. The server stops and you get your prompt back.

Your data is not lost. It is stored in `mlflow.db` and `mlartifacts`. Next time, start the server again with the same command, from the same folder, and your earlier runs will still be there.

> **Important:** always start the server from the repository root. If you start it from a different folder, MLflow creates a new, empty `mlflow.db` there, and your earlier runs will seem to be missing.

## 8. Your daily routine

Every time you sit down to work through the tutorial:

1. Open PowerShell window 1, go to the repository root, and run `.\.venv\Scripts\Activate.ps1`.
2. Open PowerShell window 2, go to the repository root, activate the environment, and run the `mlflow server ...` command from Step 7.
3. Run your scripts in window 1. View results at `http://127.0.0.1:5000`.
4. When finished, press Ctrl+C in window 2 and run `deactivate` in both windows.

## 9. Files in this lesson

| File | Status |
|------|--------|
| `requirements.txt` | New. Created at the repository root. Reused by all later lessons |
| `.gitignore` | New. Created at the repository root. Keeps `.venv`, `mlflow.db`, and `mlartifacts` out of Git |

## 10. Common errors and solutions

### `python` is not recognized

Python is not installed or is not on your PATH. Install Python 3.13 from [python.org](https://www.python.org/downloads/) and tick **Add python.exe to PATH** in the installer. Then open a **new** PowerShell window. You can also try `py --version`, which uses the Windows Python launcher.

### Activation error: running scripts is disabled on this system

Windows blocks PowerShell scripts by default. The error mentions `Activate.ps1` and "running scripts is disabled". To allow scripts you wrote or downloaded for your own user only, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Confirm when asked, then run the activation command again. This changes a Windows setting for your user account, so only do it if you are comfortable with that.

### Prompt does not show `(.venv)`

The environment is not active. Run the activation command from Step 4 in this window. You can check which Python you are using with:

```powershell
Get-Command python
```

The path shown should end with `.venv\Scripts\python.exe`.

### `ModuleNotFoundError: No module named 'mlflow'`

You are probably using a Python that does not have MLflow installed. Check that `(.venv)` is showing, then run Step 5 again.

### `mlflow` is not recognized when starting the server

The environment is not active in that window (each new window needs activation), or the install did not finish. Activate the environment, then try:

```powershell
python -m mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

### The port is already in use

Starting the server prints an error saying the address is already in use. Either another MLflow server is still running (look for another PowerShell window), or another program is using port 5000.

To see what is using the port:

```powershell
Get-NetTCPConnection -LocalPort 5000 | Select-Object LocalAddress, State, OwningProcess
```

Then look up the process using the number shown under `OwningProcess`:

```powershell
Get-Process -Id <number>
```

If it is an old MLflow server you no longer need, stop it with `Stop-Process -Id <number>`. If you would rather keep it running, start the new server on another port, for example `--port 5001`. If you do, use `http://127.0.0.1:5001` everywhere this tutorial says `http://127.0.0.1:5000`.

### My script seems to freeze for a long time

If you run a script and the server is not running, MLflow retries the connection many times before giving up. The script can look frozen for a long time. When it finally fails, the message looks like this:

```text
mlflow.exceptions.MlflowException: API request to http://127.0.0.1:5000/api/2.0/mlflow/experiments/get-by-name failed with exception HTTPConnectionPool(host='127.0.0.1', port=5000): Max retries exceeded ...
```

Press Ctrl+C to stop the script, start the server (Step 7), and run the script again.

### The browser page does not load

Check that the server window is still open and shows no error. Make sure the address is exactly `http://127.0.0.1:5000`. If you used a different port, use that port number.

### My runs disappeared

You probably started the server from a different folder, which created a new empty `mlflow.db`. Stop the server, move to the repository root, and start it again.

### Server startup fails

Read the last lines the server printed. Common causes are the port problem above and an environment that is not active. If you are stuck, copy the full error text when asking for help.

## 11. Practice exercises

1. Stop the server with Ctrl+C. Start it again and refresh the browser. Is the `setup-check` experiment still there? Why?
2. Run the script from Step 9 twice. How many runs are in the `setup-check` experiment now?
3. Change the metric value from `42` to `7` and run the script again. Find both runs in the UI and compare the values.
4. Run `deactivate`, then `python -m pip list`. Does the list look different from before? Activate the environment again afterward.

## 12. Small challenge

Start the server on port `5001` instead of `5000`. Update the script to match, run it, and find the run in your browser. Then switch back to port `5000`.

## 13. Summary

- A virtual environment gives this project its own Python packages.
- `requirements.txt` pins the exact versions so that everyone gets the same setup.
- A **tracking server** receives data from your scripts, stores metadata in `mlflow.db`, and stores artifacts in `mlartifacts`.
- Start the server from the repository root, in its own window, and leave it running while you work.
- Press Ctrl+C in the server window to stop it. Your data stays on disk.
- A script that cannot reach the server may appear to freeze before it fails.

## 14. Next lesson and official documentation

**Next:** [Lesson 03: Your First MLflow Experiment](../03-first-experiment/README.md) (planned)

Official documentation for this lesson:

- [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/)
- [MLflow Tracking Server](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/)
- [Tracking experiments with a local database](https://mlflow.org/docs/latest/ml/tracking/tutorials/local-database/)

---

## Testing status

| Part | Status |
|------|--------|
| Package install and versions (`pip check`, imports) | Run successfully on Windows 11, Python 3.13.3 (author's machine, reported by the author) |
| Server start, test script, data location, restart persistence | Run successfully on **Linux** with MLflow 3.17.0 in a test environment |
| PowerShell commands in this lesson (activation, server start on Windows, the here-string in Step 9, port lookup, Ctrl+C) | **Not yet confirmed on Windows.** To be updated after the author runs them |