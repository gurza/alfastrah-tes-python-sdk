# -*- coding: utf-8 -*-
import datetime
import json

import pytest

from .utils import load_response
from tes import MultiJSONEncoder
from tes import (
    ApiProblem, InsuranceProduct, Risk, RiskType,
    QuoteRequest, SportKind,
)


class TestJsonSerialization:
    def test_enum_attribute(self):
        risk = Risk(type=RiskType.RISK_COVID)
        risk_dict = json.loads(json.dumps(risk, cls=MultiJSONEncoder))
        assert risk_dict['type'] == 'RISK_COVID'

    def test_enum_list(self):
        quote = QuoteRequest(sport=[SportKind.COMMON_SPORT])
        quote_dict = json.loads(json.dumps(quote, cls=MultiJSONEncoder))
        assert quote_dict['sport'] == ['COMMON_SPORT']

    def test_date(self):
        date = {
            'date': datetime.date(1970, 1, 1),
        }
        date_json = json.dumps(date, cls=MultiJSONEncoder)
        assert '1970-01-01' in date_json
        assert '1970-01-01T' not in date_json

    def test_datetime(self):
        dt = {
            'dt': datetime.datetime(1970, 1, 1, 7, 40, 0),
        }
        assert '1970-01-01T07:40:00' in json.dumps(dt, cls=MultiJSONEncoder)


class TestAPIResponseHandling:
    @pytest.mark.parametrize(
        'fn', (
            'errors/401_unauthorized.json',
            'errors/500_internal_error.json',
        ))
    def test_init_api_problem(self, fn):
        api_problem = ApiProblem(**load_response(fn))
        assert api_problem

    @pytest.mark.parametrize(
        'fn', (
            'products.json',
            'products_with_currency.json',
        ))
    def test_init_insurance_product(self, fn):
        resp = load_response(fn)
        insurance_products = [InsuranceProduct(**product) for product in resp]
        assert insurance_products
