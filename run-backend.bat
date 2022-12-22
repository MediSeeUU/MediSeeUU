@REM This program has been developed by students from the bachelor Computer Science at
@REM Utrecht University within the Software Project course.
@REM © Copyright Utrecht University (Department of Information and Computing Sciences)
@echo off
cd backend
CALL venv/scripts/activate.bat
cd api
python manage.py migrate
python manage.py runserver
