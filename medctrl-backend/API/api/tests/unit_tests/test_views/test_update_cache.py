from django.test import TestCase
from unittest.mock import patch
from api.views.update_cache import update_cache


class TestUpdateCache(TestCase):
    """
    Test api.update_cache
    """
    public_medicine_data = {
        "eu_pnumber": 10,
        "eu_legal_basis": ["article 8.3"],
    }
    urls_data = {
        "ema_url": "ema.com",
        "ec_url": "ec.com",
    }

    @patch('api.views.update_cache.cache.set')
    @patch('api.views.update_cache.UrlsSerializer')
    @patch('api.views.update_cache.PublicMedicineSerializer')
    def test_update_cache(self, public_medicine_serializer, urls_serializer, cache_set):
        """
        Test update_cache() function

        Args:
            public_medicine_serializer (MagicMock): The mock object for the PublicMedicineSerializer
            urls_serializer (MagicMock): The mock object for the UrlsSerializer
            cache_set (MagicMock): The mock object for cache.set()
        """
        # Set return value for mocks
        public_medicine_serializer.return_value.data = self.public_medicine_data
        urls_serializer.return_value.data = self.urls_data

        # Call update_cache() function from api.update_cache
        update_cache()

        # Test if cache_set() has been correctly called twice
        cache_medicine_data = cache_set.call_args_list[0].args[1]
        self.assertEqual(cache_medicine_data, self.public_medicine_data)

        cache_urls_data = cache_set.call_args_list[1].args[1]
        self.assertEqual(cache_urls_data, self.urls_data)
