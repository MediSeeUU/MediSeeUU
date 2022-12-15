CALL entervenv.bat
python -m pip install -r requirements.txt
cd API
python manage.py makemigrations
python manage.py migrate
cmd \k