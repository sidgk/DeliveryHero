import unittest
from configparser import ConfigParser

import requests
import responses
from unittest.mock import patch, mock_open

from app.getcurrency import CurrencyDownloader

config = ConfigParser()
config.read('../config/config.ini')
url = config.get('URLS', 'URL')

class TestBasicFunction(unittest.TestCase):
    def setUp(self):
        self.currencyDownloader = CurrencyDownloader(url)

    @responses.activate
    def test_checkURL(self):
        responses.add(**{
            'method': responses.GET,
            'url': self.currencyDownloader.url,
            'body': '{"error": "reason"}',
            'status': 404,
            'content_type': 'application/json'
        })

        response = requests.get(url)

        self.assertEqual({'error': 'reason'}, response.json())
        self.assertEqual(404, response.status_code)

if __name__ == '__main__':
    unittest.main()