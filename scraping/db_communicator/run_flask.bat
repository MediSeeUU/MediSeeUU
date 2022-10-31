@echo off
CALL enter_venv.bat
py -m pip install -r requirements.txt
flask run