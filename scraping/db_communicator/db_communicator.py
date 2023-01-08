import requests
import datetime
import logging
import unicodedata
from scraping.db_communicator.handlers.login_handler import login
from scraping.db_communicator.handlers.logout_handler import logout
import scraping.utilities.definitions.communicator_urls as urls

log = logging.getLogger("db_communicator")
medicine_log = logging.getLogger("db_communicator.medicine_info")


class DbCommunicator:
    """
    Handles all communication between the database and the modules
    """

    def __init__(self, username="scraper", start_with_token=True):
        """
        The init of the class which is invoked when a new DbCommunicator is created. It declares global variables `token`
        of type dict. If `start_with_token` is True it requests a token from the backend_api using the login function.

        Args:
            start_with_token (bool): Whether to initialise the class with a token or not. Standard value is true
            username(str): The username of the user, this defaults to scraper if no other user is specified
        """
        self.token = None
        self.user = username
        if start_with_token:
            self.login()
            if self.token is None:
                log.error(
                    "DbCommunicator couldn't initialise with token. Make sure the backend is running before "
                    "initialising DbCommunicator with token, and the user credentials are correct")
                raise Exception("Cannot create object")
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

        api_headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.token["token"]
        }

        response = requests.post(url=urls.scraper, headers=api_headers, data=data)
        for failed_medicine in response.json():
            error_string = str(failed_medicine)
            error_string = unicodedata.normalize("NFKD", error_string).encode('utf-8', 'ignore')
            medicine_log.warning(f"Backend failed to insert medicine: {error_string}")

        if response.status_code == 200:
            return True
        else:
            return False

    def token_checker(self):
        """
        Checks if there is a valid token. If the token is not valid it requests a new key.
        """
        if self.token is None:
            self.login()
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
        Calls the login function from the login_handler with a username and sets the value of the current token to that
        of the returned token
        """
        self.token = login(self.user)
        print(self.token)

    def logout(self):
        """
        Calls the logout function from the logout_handler with its current token and empties the current token
        """
        self.token = logout(self.token)
