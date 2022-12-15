import requests
import datetime
import time
import logging
from scraping.db_communicator.handlers.login_handler import login
from scraping.db_communicator.handlers.logout_handler import logout
import scraping.utilities.definitions.communicator_urls as urls

log = logging.getLogger("db_communicator")


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
            self.login()
            if self.token is None:
                log.error(
                    "DbCommunicator couldn't initialise with token. Make sure the backend is running before "
                    "initialising DbCommunicator with token")
            else:
                log.info("DbCommunicator successfully initialised")
        else:
            log.info("DbCommunicator successfully initialised without token")

    def send_data(self, data: str) -> bool:
        """
        Sends all data received in the argument to the database using a valid token

        Args:
            data (str): The data which is sent to the database in json format

        Returns:
            Response: The response object of the request
        """
        self.token_checker()
        post_url = 'http://localhost:8000/api/scraper/medicine/'

        api_headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.token["token"]
        }

        response = requests.post(url=urls.scraper, headers=api_headers, data=data)
        print(response)
        if response.status_code == 200:
            return True
        else:
            return False

    def token_checker(self):
        """
        Checks if there is a valid token. If the token is not valid it requests a new key.
        """
        if self.token is None:
            login()
        token_age = datetime.datetime.now() - self.token['expiry_date']
        if token_age.seconds <= 120:
            self.refresh_token()

    def refresh_token(self):
        """
        Refreshes the token by first logging out, and logging in afterwards.
        """
        self.logout()
        username, password = self.get_credentials()
        self.token = login(username, password)

    def login(self):
        """
        Calls the login function from the login_handler with user credentials taken from the get_credentials function
        and sets the value of the current token to that of the returned token
        """
        username, password = self.get_credentials()
        self.token = login(username, password)

    def logout(self):
        """
        Calls the logout function from the logout_handler with its current token and empties the current token
        """
        self.token = logout(self.token)

    # Temp function, this should grab the user credentials from a safe space in the server
    def get_credentials(self) -> (str, str):
        """
        Gets the credentials of a user from somewhere safe

        Returns:
            (str, str): Returns a tuple of username and password
        """
        return "scraper", "VeranderDitWachtwoord123!"
