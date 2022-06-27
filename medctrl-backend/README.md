# Backend

This project is mainly build with the Django-Rest framework. For authentication the Django-Rest-Knox framework is utilized. 

## Initialization
Make sure python 3.x.x is installed on your device and that the 'setting setup' is correctly followed in 'readme.md' located in the /API/ folder.

1. naviagte to the 'medctrl-backend' folder
2. run the following command: ```py -m venv venv```
3. run the following command: ```venv/scripts/activate```
4. run the following command: ```pip install -r requirements.txt```

## File structure
There are four main types of files that are used in the Django-Rest framework. Ths are 'Models', 'views', 'serializers' and 'urls'. Each of these files has it own purpose, to create an endpoint all components are needed.

### Models
Django-Rest utilises a SQL database at its core. Each Model describes a table in the databse. When migrating the backend, Django-Rest interfaces with the SQL database to create and/or update its tables.

### Serializers
Serialization is the process in which a data structure, such as a python dictionary, is prepared for transmission. Each serializer targets a spesific model for wich it can serialize data.

### Views
A view takes a web request and returns a web response. Each view is connected to an endpoint and when a request is send to that endpoint the view returns the suitable response. For this project all endpoints return JSON data.

### Urls
The Url files contain all valid Paths that can be accessed using a URL. When a  web request is made to the server the url file is used to see if the url in the webrequest is valid. When the url is valid the request is forewarded to the right view.  

## Local deployment
Using powershell is recomened when working on a local machine. 

1. naviagte to the '\medctrl-backend' folder
2. run the following command: ```venv/scripts/activate```
3. naviagte to the '\medctrl-backend\API' folder
4. run the following command: ```py manage.py migrate```
5. run the following command: ```py manage.py runserver```

All valid urls can now be accessed via the browser at 'http://#HOST:PORT/PATH' -> example: 'http://127.0.0.1:8000/account/login/'.

## Copyright statement

This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.

© Copyright Utrecht University (Department of Information and Computing Sciences)
