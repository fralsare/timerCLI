# Timer CLI Application

Timer CLI is a lightweight command-line utility designed for Linux systems that tracks the amount of active usage time versus idle time. It automatically pauses the active timer when no keyboard, mouse, or touch input is detected for a defined duration (default: 30 seconds; change the `IDLE_LIMIT` constant to adjust).

## 🖼️ Demo

Here is a screenshot demonstrating the application in action:
![Application Demo](./timerCLI_image1.png)

## Installation

### No-install option: AppImage (Linux x86_64)

Prefer not to clone the repo? Download `TimerAppCLI-x86_64.AppImage` from the [Releases page](https://github.com/fralsare/timerCLI/releases), make it executable, and run it:

```bash
chmod +x TimerAppCLI-x86_64.AppImage
./TimerAppCLI-x86_64.AppImage
```

(The input-permission setup in the steps below still applies.)

### Windows: standalone .exe

Download `TimerAppCLI-x86_64.exe` from the [Releases page](https://github.com/fralsare/timerCLI/releases). No Python install and no admin rights required.

*   **Run in an existing terminal:** open PowerShell or cmd in the file's folder and run `.\TimerAppCLI-x86_64.exe`
*   **New window:** just double-click it

(Prefer source? `python timerCLI_windows.py` works with Python 3.8+ — standard library only.)

### Prerequisites

*   A Linux operating system (The input monitoring mechanism relies on Linux kernel features).
*   Python 3.8+

### Setup Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/fralsare/timerCLI
    cd timerCLI
    ```
2.  **Install Dependencies (None required for this specific version, but good practice):**
    *This script only uses standard Python libraries.*
3.  **Grant Permissions (Crucial Step!):**
    Since the application needs to read input device events, your user account must have read access to `/dev/input/event*`. This is typically achieved by adding your user to the `input` group.

    **Run this command in your terminal:**
    ```bash
    sudo usermod -aG input $USER
    ```
    **⚠️ IMPORTANT:** After running this command, you must **log out and log back in** (or reboot) for the group change to take effect.

## Usage

### Running the Timer

After completing the setup and logging back in, you can run the application from your terminal:

```bash
./timerCLI.py
```

(or `python3 timerCLI.py` — both work, the script has a shebang and the executable bit set.)

The application will start monitoring your input devices.

*   **Idle Period:** When no input is detected for the configured `IDLE_LIMIT` (default: 30 seconds), the timer will automatically pause.
*   **Resumption:** The timer will resume as soon as any input event is detected.
*   **Stopping:** Press `Ctrl+C` to stop the application and view the final usage statistics.

---

## 🙏 Support open-source tool development

Your donation keeps this project maintained and funds new open-source projects, while supporting my CyberSecurity studies. Even a small amount makes a real difference. Thank you for supporting independent open-source work!

- **PayPal** — [paypal.com/ncp/payment/KKFBWQP97XUCN](https://www.paypal.com/ncp/payment/KKFBWQP97XUCN)
- **Razorpay** — [rzp.io/rzp/TdksERz](https://rzp.io/rzp/TdksERz)

## 📜 License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for the full license text.

<details>
<summary>MIT License (summary)</summary>

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software. The only requirement is that you include the original copyright notice and this permission notice in all copies or substantial portions of the software.

Copyright (c) 2026 fralsare
</details>

*This application is designed to be a learning project and relies on specific Linux kernel interfaces.*
