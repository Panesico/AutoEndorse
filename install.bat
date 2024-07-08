@echo off
setlocal

REM Define variables
set PYTHON_URL=https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe
set PYTHON_INSTALLER=python_installer.exe
set VENV_DIR=myenv
set CHROME_URL=https://dl.google.com/chrome/install/126/chrome_installer.exe
set CHROME_INSTALLER=chrome_installer.exe

REM Download Python installer
echo Downloading Python...
powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"

REM Install Python silently
echo Installing Python...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

REM Ensure Python and pip are in PATH
set "PATH=%PATH%;C:\Program Files\Python311;C:\Program Files\Python311\Scripts"

REM Verify Python installation
python --version
if %errorlevel% neq 0 (
    echo Python installation failed.
    exit /b 1
)

REM Download Google Chrome installer
echo Downloading Google Chrome...
powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri %CHROME_URL% -OutFile %CHROME_INSTALLER%"

REM Install Google Chrome silently
echo Installing Google Chrome...
%CHROME_INSTALLER% /silent /install

REM Create virtual environment
echo Creating virtual environment...
python -m venv %VENV_DIR%

REM Activate virtual environment
call %VENV_DIR%\Scripts\activate

REM Upgrade pip in the virtual environment
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages

REM Keep the terminal open in the virtual environment
echo Virtual environment setup complete. Opening virtual environment...
cmd /k

echo Installing Selenium and python-dotenv...
pip install -r requirements.txt

endlocal
