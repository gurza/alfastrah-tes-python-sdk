# -*- coding: utf-8 -*-
import pytest

from .utils import load_response
from tes import (
    ApiProblem, InsuranceProduct,
)


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
            'products/products.json',
            'products/products_with_currency.json',
        ))
    def test_init_insurance_product(self, fn):
        resp = load_response(fn)
        insurance_products = [InsuranceProduct(**product) for product in resp]
        assert insurance_products
