# INSTALLATION GUIDE: Timer CLI Application

This guide provides step-by-step instructions to set up and run `timerCLI.py` on a Linux system.

## 🚀 Prerequisites

*   **Operating System:** Linux (This application uses kernel-level input event monitoring).
*   **Runtime:** Python 3.x (Standard Python library usage only).

## 🛠️ Step 1: Obtain the Code

If you haven't already, clone the project repository:
```bash
git clone <repository-url>
cd timer-cli
```

## 🔐 Step 2: Configure Input Permissions (CRITICAL)

The `timerCLI.py` script must read from the `/dev/input/event*` devices to detect user activity. By default, standard users do not have the necessary permissions. You must add your user to the `input` group.

Execute the following command:
```bash
sudo usermod -aG input $USER
```

**🛑 IMPORTANT WARNING:** For this change to take effect, you **must log out of your current session and log back in** (or reboot your system).

## ▶️ Step 3: Run the Application

Once permissions are set and you have logged back in, you can execute the script:

```bash
python3 timerCLI.py
```

The application will begin monitoring and displaying your active/idle time.