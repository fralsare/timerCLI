@echo off
rem Launcher for timerCLI_windows.py — run it from an existing terminal
rem window so the timer stays in the same terminal:
rem
rem     .\timerCLI_windows.bat
rem
rem (Double-clicking this file will, like any console app, open its own
rem  new terminal window.)
python "%~dp0timerCLI_windows.py" %*
