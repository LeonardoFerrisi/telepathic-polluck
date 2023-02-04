@echo off
echo Currently in %~dp0
echo.
echo This script will require administrator permissions to set an environment variable so that the main script can run.
echo.
pause
SETX TAU %~dp0
echo Environment Variable "TAU" set to %~dp0
pause