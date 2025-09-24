@echo off
REM Navigate to the working directory
cd /d "C:\Working Directory\stock-trading-python-app"

REM Activate the virtual environment
call pythonenv\Scripts\activate.bat

REM Run the scheduled Python script
python python.py
