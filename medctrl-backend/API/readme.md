# Backend

## Settings

In the `API_settings/settings/` folder there is a common settings file (`common.py`), these settings are the same for everyone.\
Some settings, like database credentials, are different for each developer/server.\
These settings are stored in separate files that are excluded by the version control system.

### Settings setup
To configure your local settings follow these steps:

1. Create a file called `dev_settings.py` in the `API_settings/settings/` folder.
2. Paste the example settings from below into the file you just created:
```py
from API_settings.settings.common import *

SECRET_KEY = "random secret key"

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "Database name",
        "USER": "Database username",
        "PASSWORD": "Database password",
        "HOST": "Database host",
        "PORT": "Database port",
    }
}

```
3. **IMPORTANT**: Make sure to actually change the settings values that you just pasted in.
4. *(optional)*: Any file in `API_settings/settings/` that has the following pattern: `local_*.py` as filename can be used
as a local settings file. \
To switch between settings files you have to set the environment variable `DJANGO_SETTINGS_MODULE` to a dot-seperated path to your settingsfile.\
Example: if you have a `local_mysettings.py` settings file, you have to set `DJANGO_SETTINGS_MODULE` to `API_settings.settings.local_mysettings` for Django to pickup the local settings file

## Linting and formatting
We make use of Black and Pylint as our linter/formatter. 
These tools are already installed if you ran the `pip install -r requirements.txt` command.

To format all python files, run the following commands:
* To just see what will be changed: `black --diff .` 
* To actually format the files: `black .`

To check for errors using Pylint run the following command:
* On Unix systems: ``pylint `git ls-files **/*.py` ``
* On Windows: # TODO

Most editors have support for Black and Pylint built in.
