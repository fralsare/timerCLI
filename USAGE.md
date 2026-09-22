# USAGE GUIDE: Timer CLI Application

The `timerCLI.py` application is a simple yet effective tool for tracking active usage time by detecting user input on a Linux system.

## ⏱️ How It Works

The script continuously monitors a list of input device files (`/dev/input/event*`). If it detects input (keyboard press, mouse movement, touch event), the active timer resets. If no input is detected for a defined period (`IDLE_LIMIT`, default 30 seconds), the timer enters a paused state.

## 💻 Running the Application

1.  Ensure you have completed the installation steps (especially the permission setup in `INSTALL.md`).
2.  Open your terminal in the project directory.
3.  Execute the script using Python 3:
    ```bash
    python3 timerCLI.py
    ```

## ⚙️ Features Overview

| Feature | Description |
| :--- | :--- |
| **Real-Time Tracking** | Displays `Idle: [s]` and `Active: [MM:SS]` in the console. |
| **Automatic Pausing** | Pauses when idle for `IDLE_LIMIT` seconds. |
| **Resumption** | Automatically resumes immediately upon any detected input. |
| **Graceful Exit** | Press `Ctrl+C` to stop the program cleanly and see the final statistics. |

## 💡 Customization

The idle limit is controlled by the `IDLE_LIMIT` constant within the code (`timerCLI.py`). You can modify this value if you wish to change how quickly the timer pauses.

---
*This application is designed for local, Linux-based use.*