# -*- coding: utf-8 -*-
import os

import pytest

from tes import AlfaInsTESClient

api_key = os.getenv('ALFASTRAH_KEY')
client = AlfaInsTESClient(api_key)
client.api_host = 'https://uat-tes.alfastrah.ru'


class TestBasic:
    def test_client_create(self):
        assert client

    def test_api_access(self):
        resp = client.request('GET', '/products')
        assert resp
