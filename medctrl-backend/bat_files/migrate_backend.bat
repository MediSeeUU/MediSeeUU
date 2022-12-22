CALL entervenv.bat
cd API
python manage.py makemigrations
python manage.py migrate
cmd \k