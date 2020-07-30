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
    PolicyStatus, Segment, ServiceClass, Ticket,
)
from tes import TESException


@pytest.fixture(scope='class')
def client_connector():
    api_key = os.getenv('ALFASTRAH_TES_KEY')
    client = AlfaStrahTESClient(api_key)
    client.api_host = 'https://uat-tes.alfastrah.ru'
    yield client


def random_pnr():
    """Returns random PNR number."""
    letters = string.ascii_uppercase
    pnr_number = ''.join(random.choice(letters) for _ in range(6))
    return pnr_number


def random_ticket_number():
    """Returns random Air France ticket number."""
    return '057-' + ''.join(str(random.choice(range(10))) for _ in range(10))


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
                nationality='RU',
                ticket=Ticket(number=random_ticket_number())
            ),
            Person(
                first_name='Louisa',
                last_name='Hawkins',
                gender=Gender.FEMALE,
                birth_date=datetime.date(1977, 4, 10),
                document=Document(type=DocumentType.PASSPORT, number='3809468921'),
                nationality='RU',
                ticket=Ticket(number=random_ticket_number())
            )
        ]

    @pytest.fixture
    def product(self):
        product_code = os.getenv('ALFASTRAH_TES_PRODUCT_CODE')
        yield InsuranceProduct(product_code)

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

    def test_get_products(self, client_connector, product):
        products = client_connector.get_products(product_type='AIR')
        products_codes = [product.code for product in products]
        assert product.code in products_codes

    def test_quote(self, client_connector, product, segments):
        resp = client_connector.quote(product=product, segments=segments)
        assert resp.quotes[0].policies[0].rate[0].value > 0

    def test_issue(self, client_connector, insureds, product, segments):
        resp = client_connector.create(insureds,
                                       product=product, segments=segments, pnr=random_pnr())
        ids = [policy.policy_id for policy in resp.policies]
        assert len(ids) == len(insureds)
        for policy_id in ids:
            _ = client_connector.confirm(policy_id)
            policy = client_connector.get_policy(policy_id)
            assert policy.status == PolicyStatus.CONFIRMED
