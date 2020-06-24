# -*- coding: utf-8 -*-
import pytest

from .utils import load_response
from tes import (
    ApiProblem,
)


class TestAPIResponseHandling:
    @pytest.mark.parametrize(
        'fn', (
            'errors/500_transport_error.json',
        ))
    def test_init_apiproblem(self, fn):
        api_problem = ApiProblem(**load_response(fn))
        assert api_problem
