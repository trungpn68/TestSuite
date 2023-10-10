@echo off
setlocal

rem Define the name of the virtual environment
set VENV_NAME=venv

rem Check if the virtual environment already exists
if not exist %VENV_NAME% (
    echo Creating virtual environment %VENV_NAME%...
    python -m venv %VENV_NAME%
)

rem Activate the virtual environment
call %VENV_NAME%\Scripts\activate

rem Install packages from requirements.txt
echo Installing packages from requirements.txt...
pip install -r requirements.txt

rem Deactivate the virtual environment
deactivate

echo Virtual environment setup and package installation completed.
exit /b 0
