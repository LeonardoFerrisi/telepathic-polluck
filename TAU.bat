@echo off

CD "C:\Users\leofe\neurotech\telepathic-polluck"

echo Currently in: %cd%
echo ------------------------------------------


call .esp\Scripts\activate.bat

pause

echo.

echo Union Neurotech 2023. (www.unionneurotech.com) 
echo Telepathic Polluck Program. 
echo For Inquires please contact ferrisil@union.edu
echo. 
pause

echo Starting ThinkingAboutU. This may take a moment to load.
echo.

python main\run.py