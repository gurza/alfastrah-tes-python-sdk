# -*- coding: utf-8 -*-
import pytest

from alfastrah import AlfaStrahClient

client = AlfaStrahClient()


class TestBasic:
    def test_client_create(self):
        assert client is not None

    def test_api_access(self):
        assert False
