import json
import requests
import datetime
# from .app import send_data
import time
# import os
# from .app import
from scraping.__main__ import db_communicator


def main(directory: str):
    # Read all data, for now use a test file
    json_file = open('db_communicator/example_data/json_example_file.json')
    data = json.loads(json_file.read())
    data = json.dumps(data)
    print(data)

    db_communicator.send_data(data=data)
    # self.request_token()
    # has_token = receive_token()
    # print(last_retrieval)
    # if not has_token:
    #     print("Error setting up db_uploader, please try again...")
    #     return


# The follow functions can only be invoked if the api_key has been required
# def send_data(self, data):
#     sender_url = 'http://localhost:5000/send_data/'
#     sender_headers = {
#         'Content-type': 'application/json',
#         'Accept': 'application/json'
#     }
#     response = requests.post(url=sender_url, headers=sender_headers, json=data)
#     print(response)
#
#
# def receive_token(self) -> bool:
#     token_url = 'http://localhost:5000/token/'
#     response = requests.get(url=token_url)
#     print(response)
#     global api_key
#     if response.status_code == 200:
#         api_key = response.json()['key']
#         print("New api key acquired")
#         return True
#     else:
#         api_key = ""
#         print("Could not retrieve token, are the flask server and the backend server running?")
#         return False
#
#
# def request_token(self):
#     api_endpoint = 'http://localhost:8000/api/scraper/token/'
#     # userdata = json.dumps({'username': 'scraper', 'password': ''})
#     # print(userdata)
#     response = requests.get(api_endpoint)
#     print(response)

# @app.route('/send_data/', methods=['POST'])
# def send_data():
#     print("I AM HERE")
#     data = request.get_json()
#     post_url = 'http://localhost:8000/api/scraper/medicine/'
#     # Dit zou die mee moeten krijgen
#     print(api_key)
#     print(data)
#
#     if not check_key():
#         print("Didn't find a valid token. Did you initialize correctly/is your session older than a day?")
#         return "No token"
#
#     # going to force break the api_key
#     # api_key = "a"
#
#     api_headers = {
#         'Content-type': 'application/json',
#         'Accept': 'application/json',
#         'Authorization': api_key
#     }
#
#     response = requests.post(url=post_url, headers=api_headers, data=data)
#     print("Status code: ", response.status_code)
#     print("Printing Entire Post Request")
#     print(response.json())
#     return "200"
