# PRODIGY_CS_04 - Simple Keylogger (Educational)

**Task-04** for the Prodigy InfoTech Cyber Security internship: a minimal program that **records keystrokes** and **appends them to a log file**, to study how such tools behave and why **permissions and ethics** matter.

## Legal and ethical use (read before running)

- Use **only** on a computer **you own**, or where you have **clear written permission** (e.g. lab agreement, employer authorization).
- Deploying a keylogger **without consent** on shared, work, school, or third-party systems may violate **computer misuse / privacy laws** and **policies**. You are responsible for compliance.
- This project is for **defensive awareness** (how attacks work, how to detect them, why endpoint controls matter), **not** for covert monitoring.


If you cannot meet these conditions, **do not run** the program.

## What this project does

- Listens for key **presses** and writes a human-readable representation to a file (default `keystroke_log.txt`).
- Adds **UTC session start/end** markers.
- Stops when you press **F12** (on some laptops: **Fn+F12**).
- **Suppresses terminal/app key echo by default** so captured keys do not spill into the prompt.
- **Refuses to start** unless you pass **`--consent`**, so running it is always a deliberate choice.

## Requirements

- Python **3.10+**
- Windows, macOS, or Linux (OS may ask for **accessibility/input monitoring** permissions).

Install:

```bash
pip install -r requirements.txt
```

## How to run

**Consent is mandatory:**

```bash
python simple_keylogger.py --consent
```

Custom log path:

```bash
python simple_keylogger.py --consent -o ./my_session_log.txt
```

Optional (not recommended): allow keys to also reach the active terminal/app:

```bash
python simple_keylogger.py --consent --no-suppress
```

Help:

```bash
python simple_keylogger.py --help
```

While it runs, keys are captured and suppressed from the active prompt by default. Open the log file to see output, and press **F12** to stop.

## Repository layout

| File | Purpose |
|------|---------|
| `simple_keylogger.py` | Listener + file logging + CLI |
| `README.md` | Quick start, ethics, usage |
| `requirements.txt` | Dependency list |

## Author

**Mario Makhlouta** - intern at Prodigy InfoTech (April 2026). Project: **PRODIGY_CS_04**.
