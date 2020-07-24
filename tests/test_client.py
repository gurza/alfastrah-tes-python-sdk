# -*- coding: utf-8 -*-
import pytest

from tes import TESException


class TestBasic:
    def test_create_client(self, client_connector):
        assert client_connector

    def test_api_access(self, client_connector):
        products = client_connector.get_products()
        assert products

    def test_handle_nonjson_response(self, client_connector):
        with pytest.raises(TESException):
            client_connector.request('GET', '/404')
        assert client_connector.status_code == 404


class TestApi:
    def test_get_products(self, client_connector):
        products = client_connector.get_products(product_type='AIR')
        assert products
