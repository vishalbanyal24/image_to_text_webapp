@echo off
echo Setting up environment for Image to Text Generator...
echo.

:: Ask for API Key input
echo Please enter your Google API Key:
set /p GOOGLE_API_KEY="API Key: "

:: Show the entered key
echo You entered: %GOOGLE_API_KEY%

echo.
echo Setting environment variable GOOGLE_API_KEY...
setx GOOGLE_API_KEY "%GOOGLE_API_KEY%" >nul

echo.
echo Current value of GOOGLE_API_KEY:
echo %GOOGLE_API_KEY%

echo.
echo Environment variable set successfully!
echo.
echo Now you can run:
echo   python test_setup.py
echo   python manage.py runserver
echo.
echo Note: Using 'setx' makes the variable permanent for future sessions.
echo You may need to open a new terminal for it to take effect.
echo.
pause
