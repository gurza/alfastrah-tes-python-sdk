# -*- coding: utf-8 -*-
import os

import pytest

from tes import AlfaStrahClient

api_key = os.getenv('ALFASTRAH_KEY')
client = AlfaStrahClient(api_key)


class TestBasic:
    def test_client_create(self):
        assert client is not None

    def test_api_access(self):
        assert False
