import requests
import datetime
import time


class DbCommunicator:
    """
    Handles all communication between the database and the modules
    """
    def __init__(self):
        """
        The init of the class which is invoked when a new DBCommunicator is created. It declares global variables
        `api_key` of type string, `last_retrieval` of type datetime and `tries` of type int. Then it sends a get request
        for this key to the token_handler
        """
        # Initialize values
        self.api_key = ""
        self.last_retrieval = datetime.datetime(2000, 1, 1, 12, 0, 00, 0)
        self.tries = 0

        # Updates the api_key and the last_retrieval value
        success = self.request_token()

        if success:
            print("Terminate the class, not implemented yet")

    def request_token(self) -> bool:
        """
        Requests a token from the token_handler server and updates the member variables `api_key`, `last_retrieval` and
        `tries`

        Returns:
            bool: True if a valid token has been received, False otherwise
        """
        token_url = 'http://localhost:5000/token/'
        response = requests.get(url=token_url)

        if response.status_code == 200:
            self.api_key = response.json()['key']
            self.last_retrieval = datetime.datetime.now()
            self.tries = 0
            print("New api key acquired")
            return True
        elif response.status_code == 503 and self.tries < 5:
            self.tries += 1
            print("Failed to retrieve key, retrying...")
            time.sleep(1)
            self.request_token()
        else:
            print("Could not retrieve token, are the flask server and the backend server running?")
            return False

    def send_data(self, data: str) -> str | tuple:
        """
        Sends all data received in the argument to the database using a valid api_key

        Args:
            data (dict): The data which is sent to the database

        Returns:
            Response: The response object of the request
        """
        post_url = 'http://localhost:8000/api/scraper/medicine/'

        if not self.key_valid():
            print("token not valid")
            return "No token"

        # This should not be duplicate code
        api_headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.api_key
        }

        requests.post(url=post_url, headers=api_headers, data=data)
        return "correct", 200

    # Not fully functional
    def key_valid(self) -> bool:
        """
        Checks if there is a valid api key. If the key is not valid it requests a new key.

        Returns:
            bool: True if the token is still valid, False otherwise
        """
        token_age = datetime.datetime.now() - self.last_retrieval
        # Requires at least 100 seconds for a task, can be another value
        if token_age.days < 0.99:
            return True
        return False
