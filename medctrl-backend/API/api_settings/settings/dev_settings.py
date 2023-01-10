from api_settings.settings.common import *
 
SECRET_KEY = "secret"
 
DEBUG = True
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'medisee_db',
        'USER': 'root',
        'PASSWORD': 'pharmagoblins123',
        'HOST': '',
    }
}
