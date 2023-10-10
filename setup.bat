@echo off
setlocal

rem Check if Python is installed
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    
    rem Download the Python installer (adjust the URL as needed)
    bitsadmin /transfer "PythonInstaller" https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe %TEMP%\python-installer.exe

    rem Install Python silently
    %TEMP%\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    rem Check the installation status
    if %errorlevel% neq 0 (
        echo Failed to install Python.
    ) else (
        echo Python is now installed.
    )

    rem Clean up the installer
    del %TEMP%\python-installer.exe
) else (
    echo Python is already installed.
)

endlocal

./venv/Scripts/activate


