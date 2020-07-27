# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
from enum import Enum
import json
import uuid

import requests

from .exceptions import TESException, AuthErrorException
from .models import (
    ApiRequest, ApiProblem, InsuranceProduct,
    Person, Segment, Amount, ServiceClass,
    SportKind, FareType, Opt, AcquisitionChannel,
    QuoteRequest, QuoteResponse,
)


class AlfaInsTESClient:
    api_host = 'https://uat-tes.alfastrah.ru'
    base_path = '/travel-ext-services/api/v2'
    default_currency = 'RUB'
    default_country = 'RU'
    default_manager = 'AlfaInsTESClient'

    def __init__(self, api_key, verify_ssl=True):
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.req = self.resp = self.status_code = None

    def raise_for_error(self):
        """Raises stored :class:`TESException`, if one occurred."""
        if self.status_code is None or self.status_code == 200:
            return
        api_problem = ApiProblem(**self.resp) if self.resp is not None else ApiProblem()
        if self.status_code == 401:
            raise AuthErrorException(api_problem.detail or 'Unauthorized')
        else:
            raise TESException(api_problem.detail or 'Unknown problem')

    def request(self, method, path, data=None, resp_cls=None):
        """Constructs and sends a request to API Gateway.

        :param method: HTTP method, e.g. 'GET', 'POST', 'PUT', 'DELETE'.
        :type method: str
        :param path: API path, e.g. '/products'.
        :type path: str
        :param data: (optional) Request body.
        :type data: ApiRequest or None
        :param resp_cls: Response class.
            This class must contain a static "decode()" method
            that will be called to convert a JSON Python object (API Response) to an instance of this class.
        :type resp_cls: class or None
        :return: JSON API response.
        :rtype: class
        """
        self.req = json.dumps(data, cls=MultiJSONEncoder) if data is not None else None
        self.resp = None
        url = '{api_host}{base_path}{path}'.format(api_host=self.api_host, base_path=self.base_path, path=path)
        headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
        }
        r = requests.request(method, url,
                             headers=headers, data=self.req, verify=self.verify_ssl)
        try:
            self.resp = r.json()
        except ValueError:
            self.resp = None
        self.status_code = r.status_code
        self.raise_for_error()
        if resp_cls is not None:
            return json.loads(r.content, cls=MultiJSONDecoder, result_cls=resp_cls)
        return self.resp

    def get_products(self, product_type=None):
        """Returns list of available insurance products.

        :param product_type: (optional) Returns list of insurance products of the given type only, if specified,
            e.g. 'AIR'.
        :type product_type: str or None
        :returns: List of available insurance products.
        :rtype: list[InsuranceProduct]
        """
        if product_type:
            path = '/products/{type}'.format(type=product_type)
        else:
            path = '/products'
        products = self.request('GET', path, resp_cls=InsuranceProduct)
        return products

    def quote(self, product_code, insureds, segments,
              booking_price, service_class, fare_type, fare_code,
              end_date,
              currency=None, country=None, sport=None, manager_name=None,
              manager_code=None, opt=None, acquisition_channel=None):
        """

        :param product_code: Insurance product code.
        :type product_code: str
        :param insureds: List of insured persons.
        :type insureds: list[Person]
        :param segments: List of travel segments, e.g. list of flights.
        :type segments: list[Segment]
        :param booking_price: Total price of the booking.
        :type booking_price: Amount
        :param service_class: Service class.
        :type service_class: ServiceClass
        :param fare_type: Refundability.
        :type fare_type: FareType
        :param fare_code: Fare code (fare basis), e.g. 'BPXOWRF'.
        :type fare_code: str
        :param end_date: Expiry date of the policy.
        :type end_date: datetime.datetime

        :param currency: Quote currency code, ISO 4217, default is ``self.default_currency``.
        :type currency: str or None
        :param country: Country code where the insurance policy will be paid for, ISO 3166-1,
            default is ``self.default_country``.
        :type country: str or None
        :param sport: Insured sports kind, default is None.
        :type sport: list[SportKind] or None
        :param manager_name: Manager (cashier) code, default is ``self.default_manager``.
        :type manager_name: str or None
        :param manager_code: Manager (cashier) code, default is ``self.default_manager``.
        :type manager_code: str or None
        :param opt: Option state, default is ``Opt.OPT_IN``.
        :type opt: Opt or None
        :param acquisition_channel: Acquisition (data collection) channel,
            default is ``AcquisitionChannel.CROSS_SALE``.
        :type acquisition_channel: AcquisitionChannel or None

        :return:
        """
        path = '/policies/quote'

        currency = currency if currency is not None else self.default_currency
        country = country if country is not None else self.default_country
        manager_name = manager_name if manager_name is not None else self.default_manager
        manager_code = manager_code if manager_code is not None else self.default_manager
        opt = opt if opt is not None else Opt.OPT_IN
        acquisition_channel = acquisition_channel if acquisition_channel is not None else AcquisitionChannel.CROSS_SALE

        product = InsuranceProduct(product_code)
        quote_request = QuoteRequest(
            session_id=str(uuid.uuid4()), product=product, insureds=insureds, segments=segments,
            booking_price=booking_price, currency=currency, service_class=service_class, country=country,
            sport=sport, fare_type=fare_type, fare_code=fare_code, manager_name=manager_name,
            manager_code=manager_code, opt=opt, end_date=end_date, acquisition_channel=acquisition_channel
        )
        resp = self.request('POST', path, data=quote_request, resp_cls=QuoteResponse)
        return resp


class MultiJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, Enum):
            return o.name
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')

        if hasattr(o, 'to_json') and callable(o.to_json):
            return o.to_json()

        # Let the base class default raise the TypeError
        return json.JSONEncoder.default(self, o)


class MultiJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        self.result_cls = kwargs.pop('result_cls', None)
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, **kwargs):
        obj = json.JSONDecoder.decode(self, s, **kwargs)

        if self.result_cls is None:
            return obj

        if isinstance(obj, dict):
            return self.result_cls.decode(obj)
        elif isinstance(obj, list):
            return [self.result_cls.decode(o) for o in obj]

        return obj
