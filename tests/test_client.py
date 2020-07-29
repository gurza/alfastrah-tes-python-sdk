# -*- coding: utf-8 -*-
import pytest

from tes import (
    InsuranceProduct,
)
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


@pytest.mark.incremental
class TestMainFlow:
    @pytest.fixture(autouse=True, scope='class')
    def state(self):
        yield {}

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
        resp = client_connector.quote(product_code, insureds, segments, booking_price,
                                      service_class, fare_type, fare_code, end_date)
        assert resp.quotes[0].policies[0].rate[0].value > 0

    def test_create(self, state, client_connector, insureds, product_code, segments, pnr):
        product = InsuranceProduct(product_code)
        resp = client_connector.create(insureds,
                                       product=product, segments=segments, pnr=pnr)
        state['ids'] = [policy.policy_id for policy in resp.policies]
        assert len(state['ids']) > 0
        assert all(state['ids'])

    def test_confirm(self, state, client_connector):
        for policy_id in state['ids']:
            assert client_connector.confirm(policy_id)
