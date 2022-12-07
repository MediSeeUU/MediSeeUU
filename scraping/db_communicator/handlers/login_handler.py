import requests
import logging
import json
import scraping.db_communicator.urls as urls
import time

log = logging.getLogger("db_communicator.login")


def login(username: str, password: str) -> dict:
    """
    Handles logging a user into the backend and returns a token dict if this was successful

    Args:
        username (str): A string containing the username information of the user
        password (str): A string containing the password information of the user

    Returns:
        dict: Returns a dict of elements token and expiry_date. The dict is None if the token retrieval was unsuccessful
    """
    login_data = {
        "username": username,
        "password": password
    }
    login_json = json.dumps(login_data)
    api_headers = {
        'Content-type': 'application/json',
    }
    return login_attempt(login_json, api_headers)


def login_attempt(login_data: dict, api_headers: dict, attempt=1) -> dict:
    """
    Attempts to log in using the given parameters, if this fails it retries up to 5 times

    Args:
        login_data (dict): A dictionary containing all information required for logging the user in
        api_headers (dict): A dictionary containing required information for sending a login request
        attempt (int): The current attempt of the login_attempt function. First attempt = 1 and last attempt = 5

    Returns:
        dict: Returns a dict of elements token and expiry_date. The dict is None if the token retrieval was unsuccessful
    """
    if attempt <= 5:
        response = requests.post(urls.login, headers=api_headers, data=login_data)
        if response.status_code == 200:
            response_data = response.json()
            token = {
                "token": "Token " + response_data["token"],
                "expiry_date": response_data["expiry"]
            }
            return token
        else:
            log.info("Failed to retrieve token, attempt " + str(attempt) + " out of 5. retrying...")
            attempt += 1
            time.sleep(1)
            login_attempt(login_data, api_headers, attempt)
    else:
        return None
