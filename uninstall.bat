@echo off
setlocal

REM Define variables
set VENV_DIR=myenv
set PYTHON_DIR=C:\Program Files\Python311

REM Deactivate virtual environment if active
if defined VIRTUAL_ENV (
    echo Deactivating virtual environment...
    call %VENV_DIR%\Scripts\deactivate
)

REM Remove the virtual environment directory
if exist %VENV_DIR% (
    echo Removing virtual environment directory...
    rmdir /s /q %VENV_DIR%
) else (
    echo Virtual environment directory not found.
)

REM Uninstall Python
echo Uninstalling Python...
REM The below command assumes the Python uninstaller is located in the Python installation directory
REM If not, adjust the path accordingly or provide the full path to the uninstaller executable
if exist "%PYTHON_DIR%\uninstall.exe" (
    "%PYTHON_DIR%\uninstall.exe" /quiet
) else (
    echo Python uninstaller not found.
)

REM Remove Python directories from PATH
echo Removing Python from PATH...
setx PATH "%PATH%" /M
REM Note: The following lines attempt to remove the paths from the current session's PATH variable.
REM This does not persist across new Command Prompt sessions.
set "PATH=%PATH:C:\Program Files\Python311;=%"
set "PATH=%PATH:C:\Program Files\Python311\Scripts;=%"

REM Remove Python installation directory
if exist "%PYTHON_DIR%" (
    echo Removing Python installation directory...
    rmdir /s /q "%PYTHON_DIR%"
) else (
    echo Python installation directory not found.
)

echo Uninstallation complete.
endlocal
