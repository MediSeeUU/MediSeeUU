import json
import requests
# from .app import send_data
import time
# import os
# from .app import

# global key
api_key = ""


def main(directory: str):
    request_token()
    json_file = open('db_communicator/example_data/json_example_file.json')
    data = json.loads(json_file.read())
    data = json.dumps(data)
    print(data)
    send_data(data)
    # url_endpoint
    # send_data()


# invoke only after request_token has been invoked
def send_data(data):
    sender_url = 'http://localhost:5000/send_data/'
    sender_headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post(url=sender_url, headers=sender_headers, json=data)
    print(response)


def request_token():
    API_ENDPOINT = 'http://localhost:8000/api/scraper/token/'
    # userdata = json.dumps({'username': 'scraper', 'password': ''})
    # print(userdata)
    response = requests.get(API_ENDPOINT)
    print(response)
