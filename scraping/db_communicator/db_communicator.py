import json
import requests
import datetime
# from .app import send_data
import time
# import os
# from .app import


class DbCommunicator:
    def __init__(self):
        # Initialize values
        self.api_key = ""
        self.last_retrieval = datetime.datetime(2000, 1, 1, 12, 0, 00, 0)
        # self.username = username maybe niet nodig

        success = self.request_token()

        if not success:
            print("terminate something idk, shit goes wrong")

    def __del__(self):
        success_token_delete = self.delete_token()
        # Maybe also close the flask server and open it at the start
        if success_token_delete:
            print("db_communicator terminated correctly")
        else:
            print("db_communicator failed to delete the token")

    def request_token(self) -> bool:
        api_endpoint = 'http://localhost:8000/api/scraper/token/'
        response = requests.get(api_endpoint)
        print(response)  # LOGGER
        success = self.receive_token()
        return success

    def receive_token(self) -> bool:
        token_url = 'http://localhost:5000/token/'
        response = requests.get(url=token_url)
        print(response)  # LOGGER

        if response.status_code == 200:
            self.api_key = response.json()['key']
            self.last_retrieval = datetime.datetime.now()
            print("New api key acquired")
            return True
        else:
            print("Could not retrieve token, are the flask server and the backend server running?")
            return False

    def send_data(self, data):
        post_url = 'http://localhost:8000/api/scraper/medicine/'

        if not self.token_valid():
            print("token not valid")
            return "No token"

        api_headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.api_key
        }

        response = requests.post(url=post_url, headers=api_headers, data=data)
        print("Status code: ", response.status_code)
        print("Printing Entire Post Request")
        print(response.json())
        return "200"

    def delete_token(self) -> bool:
        print("send request for deleting the token")

    # should refresh the token if it is old
    def refresh_token(self):
        return "not implemented"

    def token_valid(self) -> bool:
        token_age = datetime.datetime.now() - self.last_retrieval
        # Requires at least 100 seconds for a task, can be another value
        if token_age.days < 0.99:
            return True
        return False
