import requests
import datetime
import time
import logging
from scraping.db_communicator.handlers.login_handler import login
from scraping.db_communicator.handlers.logout_handler import logout
from threading import Thread

log = logging.getLogger("db_communicator")
# Modify this when the backend location is changed
backend_url = "http://localhost:8000"


class DbCommunicator:
    """
    Handles all communication between the database and the modules
    """

    def __init__(self, start_with_token=True):
        """
        The init of the class which is invoked when a new DbCommunicator is created. It declares global variables `token`
        of type dict. If `start_with_token` is True it requests a token from the backend_api using the login function.

        Args:
            start_with_token (bool): Whether to initialise the class with a token or not. Standard value is true
        """
        self.token = None

        if start_with_token:
            username, password = self.get_credentials()
            self.token = login(username, password)
            print(self.token)
            if self.token is None:
                log.error(
                    "DbCommunicator couldn't initialise with token. Make sure the backend is running before "
                    "initialising DbCommunicator with token")
            else:
                log.info("DbCommunicator successfully initialised")
        else:
            log.info("DbCommunicator successfully initialised without token")

    # def __del__(self):
    #     """
    #     Is called whenever the db_communicator object is destroyed. Will attempt to log out with the current token if it has one.
    #     """
    #     print("finna logout")
    #     print(self.token)
    #     if not (self.token is None):
    #         logout(self.token)
    #         # t = Thread(target=logout, args=(None,))
    #         # zamn = t.start()
    #         # print("shoudlve logged out")
    #         # success = logout(self.token["token"])
    #         # if success:
    #         #     log.info("Successfully logged the DbCommunicator out in the backend")
    #         # else:
    #         #     log.warning("Couldn't logout the DbCommunicator in the backend")
    #     log.info("DbCommunicator terminated")

    def logout(self):
        logout(self.token['token'])

    def send_data(self, data: str) -> str | tuple:
        """
        Sends all data received in the argument to the database using a valid api_key

        Args:
            data (str): The data which is sent to the database

        Returns:
            Response: The response object of the request
        """
        self.token_checker()
        post_url = 'http://localhost:8000/api/scraper/medicine/'

        # This should not be duplicate code
        api_headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.token["token"]
        }

        requests.post(url=post_url, headers=api_headers, data=data)
        return "correct", 200

    # Not fully functional
    def token_checker(self):
        """
        Checks if there is a valid token. If the token is not valid it requests a new key.
        """
        token_age = datetime.datetime.now() - self.token['']
        # Requires at least 100 seconds for a task, can be another value

    def refresh_token(self):
        logout(self.token['token'])
        username, password = self.get_credentials()
        self.token = login(username, password)

    # Temp function, this should grab the user credentials from a safe space in the server
    def get_credentials(self) -> (str, str):
        return "test_user", "Coolwachtwoord123!"
