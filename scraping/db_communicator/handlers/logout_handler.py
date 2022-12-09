import requests
import logging
import time
import scraping.utilities.definitions.communicator_urls as urls

log = logging.getLogger("db_communicator.logout")


def logout(token: dict) -> None:
    """
    Handles logging a user out of the backend

    Args:
        token (str): The token of the user that is being logged out

    Returns:
        bool: True if the user was successfully logged out, False otherwise
    """
    if token is None:
        log.info("There is no token to log out")
        return None

    api_headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': token['token']
    }
    success = logout_attempt(api_headers)

    if not success:
        log.info("Failed to log out the current token")

    return None


def logout_attempt(api_headers: dict, attempt=1) -> bool:
    """
    Attempts to log out using the given parameters, if this fails it retries up to 5 times

    Args:
        api_headers (dict): A dictionary containing required information for sending a logout request
        attempt (int): The current attempt of the logout_attempt function. First attempt = 1 and last attempt = 5

    Returns:
        bool: True if the user was successfully logged out, False otherwise
    """
    if attempt <= 5:
        response = requests.post(urls.logout, headers=api_headers)
        if response.status_code == 200 or response.status_code == 204:
            log.info("Successfully logged out the current token")
            return True
        else:
            log.info("Failed to log out the current token, attempt " + str(attempt) + " out of 5. retrying...")
            attempt += 1
            time.sleep(1)
            logout_attempt(api_headers, attempt)
    else:
        return False
