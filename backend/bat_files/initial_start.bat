cd helper
CALL newvenv.bat
python -m pip install -r requirements.txt
cd API
python manage.py makemigrations
python manage.py migrate
python manage.py create_column_permissions
python manage.py init_setup
python manage.py createsuperuser