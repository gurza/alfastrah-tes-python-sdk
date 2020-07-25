# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
from enum import Enum
import json

import requests

from .exceptions import TESException, AuthErrorException
from .models import (
    ApiRequest, ApiResponse, ApiProblem, InsuranceProduct,
    Person, Segment, Amount, ServiceClass,
    SportKind, FareType, Opt, AcquisitionChannel,
    QuoteRequest, QuoteResponse,
)


class AlfaInsTESClient:
    api_host = 'https://uat-tes.alfastrah.ru'
    base_path = '/travel-ext-services/api/v2'

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
        :type resp_cls: ApiResponse
        :return: JSON API response.
        :rtype: object
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
        json_obj = json.JSONDecoder.decode(self, s, **kwargs)

        if self.result_cls is None:
            return json_obj

        if isinstance(json_obj, dict):
            return self.result_cls.decode(json_obj)
        elif isinstance(json_obj, list):
            return [self.result_cls.decode(o) for o in json_obj]
        return json_obj
