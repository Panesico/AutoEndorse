@echo off
setlocal

REM Define variables
set PYTHON_URL=https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe
set PYTHON_INSTALLER=python_installer.exe
set VENV_DIR=myenv

REM Download Python installer
echo Downloading Python...
powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"

REM Install Python silently
echo Installing Python...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

REM Ensure Python and pip are in PATH
set "PATH=%PATH%;C:\Program Files\Python310;C:\Program Files\Python310\Scripts"

REM Verify Python installation
python --version
if %errorlevel% neq 0 (
    echo Python installation failed.
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv %VENV_DIR%

REM Activate virtual environment
call %VENV_DIR%\Scripts\activate

REM Upgrade pip in the virtual environment
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo Installing Selenium and python-dotenv...
pip install selenium python-dotenv colorama

REM Keep the terminal open in the virtual environment
echo Virtual environment setup complete. The terminal will remain open.
cmd /k

endlocal
