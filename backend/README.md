# Backend

This project is mainly build with the Django-Rest framework. For authentication the Django-Rest-Knox framework is utilized. 

## Initialization
Make sure python 3.x.x is installed on your device and that the 'setting setup' is correctly followed in 'readme.md' located in the /API/ folder.

<TODO: Add here how to install MySQL>

1. navigate to the 'backend' folder
2. run the following command: ```py -m venv venv```
3. run the following command: ```venv/scripts/activate```
4. run the following command: ```pip install -r requirements.txt```

## File structure
There are four main types of files that are used in the Django-Rest framework. These are 'Models', 'Views', 'Serializers' and 'URLs'. Each of these files has it own purpose, to create an endpoint all components are needed.

### Models
Django-Rest utilises a SQL database at its core. Each Model describes a table in the database. When migrating the backend, Django-Rest interfaces with the SQL database to create and/or update its tables.

### Serializers
Serialization is the process in which a data structure, such as a Python dictionary, is prepared for transmission. Each serializer targets a specific model for which it can serialize data.

### Views
A view takes a web request and returns a web response. Each view is connected to an endpoint and when a request is sent to that endpoint the view returns the suitable response. For this project all endpoints return JSON data.

### URLs
The URL files contain all valid Paths that can be accessed using a URL. When a web request is made to the server the URL file is used to see if the URL in the webrequest is valid. When the url is valid the request is forwarded to the right view.  

## Local deployment
Using powershell is recommended when working on a local machine. 

1. navigate to the '\backend' folder
2. run the following command: ```venv/Scripts/activate```
3. navigate to the '\backend\API' folder
4. run the following command: ```py manage.py migrate```
5. run the following command: ```py manage.py runserver```

All valid URLs can now be accessed via the browser at 'http://#HOST:PORT/PATH' -> example: 'http://127.0.0.1:8000/account/login/'.

## Copyright statement

This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.

© Copyright Utrecht University (Department of Information and Computing Sciences)
