# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
import os
import random
import string

import pytest

from tes import AlfaStrahTESClient
from tes import (
    Amount, Document, DocumentType, FareType,
    Gender, InsuranceProduct, Person, Point,
    Segment, ServiceClass,
)
from tes import TESException


@pytest.fixture(scope='class')
def client_connector():
    api_key = os.getenv('ALFAINS_TES_KEY')
    client = AlfaStrahTESClient(api_key)
    client.api_host = 'https://uat-tes.alfastrah.ru'
    yield client


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


class TestApiIntegration:
    @pytest.fixture
    def insureds(self):
        yield [
            Person(
                first_name='Arthur',
                last_name='Conan Doyle',
                gender=Gender.MALE,
                birth_date=datetime.date(1979, 5, 22),
                document=Document(type=DocumentType.PASSPORT, number='4509511410'),
                nationality='RU'
            ),
            Person(
                first_name='Louisa',
                last_name='Hawkins',
                gender=Gender.FEMALE,
                birth_date=datetime.date(1977, 4, 10),
                document=Document(type=DocumentType.PASSPORT, number='3809468921'),
                nationality='RU'
            )
        ]

    @pytest.fixture
    def product(self):
        product_code = os.getenv('ALFAINS_TES_PRODUCT_CODE')
        yield InsuranceProduct(product_code)

    @pytest.fixture
    def pnr(self):
        letters = string.ascii_uppercase
        record_locator = ''.join(random.choice(letters) for i in range(6))
        yield record_locator

    @pytest.fixture
    def segments(self):
        outbound_datetime = datetime.datetime.now() + datetime.timedelta(days=30)
        inbound_datetime = datetime.datetime.now() + datetime.timedelta(days=39)

        yield [
            Segment(
                transport_operator_code='AF',
                route_number='1845',
                departure=Point(date=outbound_datetime, point='SVO'),
                arrival=Point(date=outbound_datetime + datetime.timedelta(minutes=260), point='CDG'),
            ),
            Segment(
                transport_operator_code='AF',
                route_number='1144',
                departure=Point(date=inbound_datetime, point='CDG'),
                arrival=Point(date=inbound_datetime + datetime.timedelta(minutes=225), point='SVO')
            ),
        ]

    @pytest.fixture
    def trip_additional_data(self):
        yield {
            'booking_price': Amount(Decimal(115000), currency='RUB'),
            'service_class': ServiceClass.BUSINESS,
            'fare_type': FareType.REFUNDABLE,
            'fare_code': 'CRT',
        }

    def test_get_products(self, client_connector, product):
        products = client_connector.get_products(product_type='AIR')
        products_codes = [product.code for product in products]
        assert product.code in products_codes

    def test_quote(self, client_connector, product, insureds, segments, trip_additional_data):
        booking_price = trip_additional_data.get('booking_price')
        service_class = trip_additional_data.get('service_class')
        fare_type = trip_additional_data.get('fare_type')
        fare_code = trip_additional_data.get('fare_code')
        end_date = segments[-1].arrival.date
        resp = client_connector.quote(product.code, insureds, segments, booking_price,
                                      service_class, fare_type, fare_code, end_date)
        assert resp.quotes[0].policies[0].rate[0].value > 0

    def test_issue(self, client_connector, insureds, product, segments, pnr):
        resp = client_connector.create(insureds,
                                       product=product, segments=segments, pnr=pnr)
        ids = [policy.policy_id for policy in resp.policies]
        if not ids:
            assert False
        for policy_id in ids:
            assert client_connector.confirm(policy_id)
