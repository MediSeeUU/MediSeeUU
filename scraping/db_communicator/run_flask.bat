@echo off
CALL enter_venv.bat
py -m pip install -r requirements.txt
flask --app token_handler.py run
