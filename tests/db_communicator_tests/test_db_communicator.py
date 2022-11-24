# from scraping.db_communicator import __main__ as m

import datetime
import unittest
from unittest.mock import patch, MagicMock
from scraping.db_communicator import DbCommunicator
import logging
log = logging.getLogger("db_communicator.temporary_tests")


class TestDbCommunicator(unittest.TestCase):
    """
    This class contains the tests for the non-existent functions in the db_uploader module
    """

    @classmethod
    def setUpClass(cls):
        cls.test_token = "token b694a84a142b35e2701fce36e6c2043c2fe8485b393bb49d84b683dc4fcbc046"
        cls.test_datetime = datetime.datetime(2010, 2, 4, 6, 0, 10, 0)

    @patch("scraping.db_communicator.db_communicator.datetime")
    @patch("scraping.db_communicator.db_communicator.requests")
    def test_request_token_success(self, mock_requests, mock_datetime):
        # Initialize the class (without key)
        comm = DbCommunicator(start_with_key=False)

        # Initialize mocks
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "key": self.test_token}

        mock_requests.get.return_value = mock_response
        mock_datetime.datetime.now.return_value = self.test_datetime

        self.assertTrue(comm.request_token())
        self.assertEqual(comm.api_key, self.test_token)
        self.assertEqual(comm.last_retrieval, self.test_datetime)

    @patch("scraping.db_communicator.db_communicator.requests")
    def test_request_token_instant_failure(self, mock_requests):
        # Initialize the class (without key)
        comm = DbCommunicator(start_with_key=False)

        # Initialize mocks
        mock_response = MagicMock()
        mock_response.status_code = -1
        mock_response.json.return_value = {
            "key": self.test_token}

        mock_requests.get.return_value = mock_response
        initial_date = comm.last_retrieval

        self.assertFalse(comm.request_token())
        self.assertEqual(comm.api_key, "")
        self.assertEqual(comm.last_retrieval, initial_date)
