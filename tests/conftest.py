# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
import os
import random
import string
import typing

import pytest

from tes import AlfaInsTESClient
from tes import (
    Amount, Document, DocumentType, FareType,
    Gender, Person, Point, Segment,
    ServiceClass,
)

# store history of failures per test class name and per index in parametrize (if parametrize used)
_test_failed_incremental: typing.Dict[str, typing.Dict[typing.Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None:
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))


@pytest.fixture
def client_connector():
    api_key = os.getenv('ALFAINS_TES_KEY')
    client = AlfaInsTESClient(api_key)
    client.api_host = 'https://uat-tes.alfastrah.ru'
    yield client


@pytest.fixture
def insureds():
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
def product_code():
    yield os.getenv('ALFAINS_TES_PRODUCT_CODE')


@pytest.fixture
def pnr():
    letters = string.ascii_uppercase
    record_locator = ''.join(random.choice(letters) for i in range(6))
    yield record_locator


@pytest.fixture
def segments():
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
def trip_additional_data():
    yield {
        'booking_price': Amount(Decimal(115000), currency='RUB'),
        'service_class': ServiceClass.BUSINESS,
        'fare_type': FareType.REFUNDABLE,
        'fare_code': 'CRT',
    }
