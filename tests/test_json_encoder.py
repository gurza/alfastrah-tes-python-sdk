# -*- coding: utf-8 -*-
import datetime
import json
from decimal import Decimal

import pytest

from tes import MultiJSONEncoder
from tes import (
    Amount, Risk, RiskType, QuoteRequest,
    SportKind,
)


class TestMultiJSONEncoder:
    def test_decimal(self):
        value = 95000
        price = Amount(Decimal(value), currency='RUB')
        price_dict = json.loads(json.dumps(price, cls=MultiJSONEncoder))
        assert abs(price_dict['value'] - value) < 1e-08

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
