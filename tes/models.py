# -*- coding: utf-8 -*-

"""
tes.models
~~~~~~~~~~
This module contains the primary objects.
"""

from decimal import Decimal
from enum import Enum
import datetime
import uuid

PRODUCT_TYPES = ['AIR']
SERVICE_CLASSES = ['ECONOM', 'COMFORT', 'BUSINESS']


class ApiProblem:
    """Description of the error that occurred while handling your request."""

    def __init__(self, title=None, status=None, detail=None):
        """Init.

        :param title: (optional) Short error description, e.g. 'POLICY_NOT_FOUND'.
        :type title: str or None
        :param status: (optional) Status code, e.g. 'PNF_002'.
        :type status: str or None
        :param detail: (optional) Full error description,
            e.g. 'Policy with id 12345 not found or does not belong to agent'.
        :type detail: str or None
        """
        self.title = title
        self.status = status
        self.detail = detail


class InsuranceProduct:
    """Insurance product."""

    def __init__(self, code, type=None, description=None, currency=None):
        """Init.

        :param code: Code of insurance product, e.g. 'ON_ANTICOVID_AVIA_1'.
        :type code: str
        :param type: (optional) Type of insurance product, one of ``POSSIBLE_PRODUCT_TYPES``, e.g. 'AIR'.
        :type type: str or None
        :param description: (optional) Description of insurance product, e.g. 'Страховка от риска медицинских расходов'.
        :type description: str or None
        :param currency: (obsolete) Currency code of the product, ISO 4217, e.g. 'RUB'.
        :type currency: str or None
        """
        self.code = code
        self.type = type
        self.description = description
        self.currency = currency


class Amount:
    """Amount."""

    def __init__(self, value, currency=None):
        """Init.

        :param value: Value, e.g. 35000.
        :type value: Decimal
        :param currency: (optional) Currency code, ISO 4217, e.g. 'RUB'.
        :type currency: str or None
        """
        self.value = value
        self.currency = currency


class Person:
    pass


class Segment:
    """Travel segment."""

    def __init__(self, transport_operator_code=None, route_number=None, service_class=None,
                 connection_time=None, departure=None, arrival=None, place_number=None,
                 car_number=None, car_type=None, connecting_flight=None, flight_direction=None):
        """Init.
        
        :param transport_operator_code: 
        :param route_number: 
        :param service_class: 
        :param connection_time: 
        :param departure: (optional) Departure point.
        :type departure: Point or None
        :param arrival: (optional) Arrival point.
        :type arrival: Point or None
        :param place_number: (optional) Place or seat number, e.g. '56b'.
        :type place_number: str or None
        :param car_number: (optional) Train car number, e.g. '12'.
        :type car_number: str or None
        :param car_type: (optional) Train car type, e.g. 'SV'.
        :type car_type: str or None
        :param connecting_flight: (optional) True if flight is connecting.
        :type connecting_flight: bool or None
        :param flight_direction: (optional) Flight direction.
        :type flight_direction: FlightDirection or None
        """
        self.departure = departure
        self.arrival = arrival
        self.place_number = place_number
        self.car_number = car_number
        self.car_type = car_type
        self.connecting_flight = connecting_flight
        self.flight_direction = flight_direction


class Point:
    """Departure or arrival point."""

    def __init__(self, date=None, point=None, country=None):
        """Init.

        :param date: (optional) Datetime of departure/arrival.
        :type date: datetime.datetime or None
        :param point: (optional) code of departure/arrival point, e.g. 'SVO'.
        :type point: str or None
        :param country: (optional) code of country, ISO 3166-1, e.g. 'RU'.
        :type country: str or None
        """
        self.date = date
        self.point = point
        self.country = country


class FlightDirection(Enum):
    """Flight direction."""

    OW = 1  # One way
    RT = 2  # Round trip


class QuoteRequest:
    """Request for calculating one or more insurance policies."""

    def __init__(self, session_id=None, product=None, insureds=None,
                 segments=None, booking_price=None, currency=None, service_class=None,
                 country=None):
        """Init.

        :param session_id: (optional) Session id, e.g. '88c70099-8e11-4325-9239-9c027195c069'.
        :type session_id: str or None
        :param product: (optional) Insurance product.
        :type product: InsuranceProduct or None
        :param insureds: (optional) List of insured persons.
        :type insureds: list[Person] or None
        :param segments: (optional) List of travel segments, e.g. list of flights.
        :type segments: list[Segment]
        :param booking_price: (optional) Total price of flight booking.
        :type booking_price: Amount or None
        :param currency: (optional) Quote currency code, ISO 4217, e.g. 'RUB'.
        :type currency: str or None
        :param service_class: (optional) Service class of flight, one of ``SERVICE_CLASSES``, e.g. 'BUSINESS'.
        :type service_class: str or None
        :param country: (optional) Country code where the insurance policy will be paid for, ISO 3166-1, e.g. 'RU'.
        :type country: str or None
        """
        self.session_id = session_id if session_id is not None else str(uuid.uuid4())
        self.product = product
        self.insureds = insureds if insureds is not None else []
        self.segments = segments if segments is not None else []
        self.booking_price = booking_price
        self.currency = currency
        self.service_class = service_class
        self.country = country
