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
    def test_get_products(self, client_connector, product_code):
        products = client_connector.get_products(product_type='AIR')
        products_codes = [product.code for product in products]
        assert product_code in products_codes

    def test_quote(self, client_connector, product_code, insureds, segments, trip_additional_data):
        booking_price = trip_additional_data.get('booking_price')
        service_class = trip_additional_data.get('service_class')
        fare_type = trip_additional_data.get('fare_type')
        fare_code = trip_additional_data.get('fare_code')
        end_date = segments[-1].arrival.date
        quote = client_connector.quote(product_code, insureds, segments, booking_price,
                                       service_class, fare_type, fare_code, end_date)
        assert quote
