from flask import Flask, request
import time
import datetime
import json
import requests

app = Flask(__name__)
api_key = ""
expiry_days = 2
# Arbitrary date from the past
last_key_request = datetime.datetime(2000, 1, 1, 10, 0, 0, 0)


def request_token():
    api_endpoint = 'http://localhost:8000/api/scraper/token/'
    response = requests.get(api_endpoint)
    print(response)  # LOGGER
    # success = self.receive_token()
    response.status_code = 200
    return response


# Initially request the key
request_token()


@app.route('/token/', methods=['POST'])
def receive_token():
    """

    Returns:
        object: 
    """
    token = request.form['token']
    print("Token received")
    global api_key
    api_key = "Token " + token
    success_response = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return success_response


@app.route('/token/', methods=['GET'])
def return_token():
    """

    Returns:
        object: 
    """
    has_key = check_key()
    if has_key:
        print(json.dumps({'key': api_key}), 200, {'ContentType': 'application/json'})
        return json.dumps({'key': api_key}), 200, {'ContentType': 'application/json'}
    return "500"


# This function is a stub
def check_key() -> bool:
    """
    Checks if there is an api key and if it is still valid. If it isn't it updates the key

    Returns:
        object:
    """
    if api_key == "":
        received = wait_key()
        if not received:
            print("Can't receive key, communication error")
    return True


def wait_key() -> bool:
    tries = 1
    max_tries = 5
    while api_key == "" and tries <= max_tries:
        print(str(tries) + " of " + str(max_tries) + " tries.")
        tries += 1
        time.sleep(1)
    if api_key == "":
        return False
    return True
