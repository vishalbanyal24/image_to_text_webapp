@echo off
echo Setting up environment for Image to Text Generator...
echo.

echo Please enter your Google API Key:
set /p GOOGLE_API_KEY="API Key:AIzaSyD7Jb7ePYDGYAFm2vVbC6o8t3ylNlhhWX4 "

echo.
echo Setting environment variables...
set GOOGLE_API_KEY=%AIzaSyD7Jb7ePYDGYAFm2vVbC6o8t3ylNlhhWX4%

echo.
echo Environment variables set successfully!
echo.
echo Now you can run:
echo   python test_setup.py
echo   python manage.py runserver
echo.
echo Note: These environment variables are only set for this session.
echo To make them permanent, add them to your system environment variables.
echo.
pause


