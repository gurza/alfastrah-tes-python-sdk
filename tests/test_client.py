# -*- coding: utf-8 -*-
import os

import pytest

from tes import AlfaInsTESClient
from tes import TESException

api_key = os.getenv('ALFASTRAH_KEY')
client = AlfaInsTESClient(api_key)
client.api_host = 'https://uat-tes.alfastrah.ru'


class TestBasic:
    def test_client_create(self):
        assert client

    def test_api_access(self):
        products = client.get_products()
        assert products

    def test_nonjson_response(self):
        with pytest.raises(TESException):
            client.request('GET', '/404')
        assert client.status_code == 404
