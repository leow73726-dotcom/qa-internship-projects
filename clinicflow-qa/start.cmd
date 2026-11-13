@echo off
cd /d "%~dp0.."
if not exist ".venv\Scripts\python.exe" python setup.py
".venv\Scripts\python.exe" tooling\launcher.py --project clinicflow-qa
pause
