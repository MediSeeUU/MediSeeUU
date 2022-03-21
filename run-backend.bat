@echo off
cd medctrl-backend
CALL venv/scripts/activate.bat
cd api
py manage.py migrate
py manage.py runserver
