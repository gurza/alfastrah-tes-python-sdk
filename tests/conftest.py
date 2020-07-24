# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal

import pytest

from tes import (
    Amount, Document, DocumentType, FareType,
    Gender, Person, Point, Segment,
    ServiceClass,
)


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
    ]


@pytest.fixture
def trip():
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
