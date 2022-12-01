from flask import Flask, request
import datetime
import json
import requests
import time
import logging

app = Flask(__name__)
api_key = ''
expiry_days = 2
error_state = False
# Arbitrary date from the past
last_key_request = datetime.datetime(2000, 1, 1, 10, 0, 0, 0)

log = logging.getLogger("db_communicator")


def request_token() -> requests.models.Response:
    """
    Sends a request to the api_endpoint requesting a new token. The token will not be received in the same call but in
    the function receive_token instead

    Returns:
        Response: The response object of the request
    """
    # Reset api_key
    global api_key
    api_key = ''

    api_endpoint = 'http://localhost:8000/api/scraper/token/'
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        log.info("Successfully requested a token")
    else:
        global error_state
        error_state = True
        log.error("Something went wrong when requesting a token, is the backend server running?")
    return response


# Initially request the key
request_token()


@app.route('/token/', methods=['POST'])
def receive_token() -> requests.models.Response | tuple:
    """
    Receives incoming token post requests from the backend. When the token is received the api_key and last_key_request
    member variables are updated

    Returns:
        Response: The response object of the request
    """
    token = request.form['token']
    log.info("Token received")
    global api_key
    api_key = "Token " + token
    success_response = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return success_response


@app.route('/token/', methods=['GET'])
def return_token() -> requests.models.Response | tuple:
    """
    Receives token get requests from the db_communicator and then sends a valid api_key back to the db_communicator. If
    there is no valid key, a new key will be requested via the check_key() function.

    Returns:
        Response: The response object of the request
    """
    has_key = check_key()
    global error_state
    if error_state:
        return "Could not get a token", 500
    if has_key:
        return json.dumps({'key': api_key}), 200, {'ContentType': 'application/json'}
    else:
        return "Retry later", 503


# This function is a stub
def check_key() -> bool:
    """
    Checks if there is a valid api key. If the key is not valid it requests a new key.

    Returns:
        bool: Returns True if there is a valid key, False otherwise
    """
    # Check if there is a starting key
    if api_key == "":
        return False

    time_left = last_key_request + datetime.timedelta(days=expiry_days) - datetime.datetime.now()
    log.info("Time left: " + str(time_left.seconds))
    if time_left.seconds < 3600:
        request_token()
    return True


#  This is a stub function, not functional
def wait_key() -> bool:
    """
    Waits until a key is found with a maximum amount of time (5 seconds)

    Returns:
        bool: True if a key was found after the wait, False otherwise
    """
    tries = 1
    max_tries = 5
    while api_key == "" and tries <= max_tries:
        log.info(str(tries) + " of " + str(max_tries) + " tries.")
        tries += 1
        time.sleep(1)
    if api_key == "":
        return False
    return True


# Not fully functional (token does not always get deleted)
def delete_token() -> bool:
    """
    Sends a request to delete the given token. This is used when the server gets closed while the current token hasn't
    expired yet.

    Returns:
        bool: True if it was successfully deleted, False otherwise
    """
    post_url = 'http://localhost:8000/api/scraper/token/'
    api_headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': api_key
    }
    log.info("send request for deleting the token")
    response = requests.post(url=post_url, headers=api_headers)
    log.info(response)
    if response.status_code == 200:
        return True
    return False
