@REM This program has been developed by students from the bachelor Computer Science at
@REM Utrecht University within the Software Project course.
@REM © Copyright Utrecht University (Department of Information and Computing Sciences)
@echo off
cd medctrl-backend
CALL venv/scripts/activate.bat
cd api
py manage.py migrate
py manage.py runserver
