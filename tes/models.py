# -*- coding: utf-8 -*-

"""
tes.models
~~~~~~~~~~
This module contains the primary objects.
"""

PRODUCT_TYPES = ['FLIGHT', 'FLIGHT_TRAVEL', 'TRAVEL', 'RAILWAY', 'PROPERTY', 'EVENT', 'BUS', 'TAXI']


class ApiProblem:
    """Description of the error that occurred while handling your request."""

    def __init__(self, title=None, status=None, detail=None):
        """Init.

        :param title: (optional) short error description, e.g. 'POLICY_NOT_FOUND'.
        :type title: str or None
        :param status: (optional) status code, e.g. 'PNF_002'.
        :type status: str or None
        :param detail: (optional) full error description,
            e.g. 'Policy with id 12345 not found or does not belong to agent'.
        :type detail: str or None
        """
        self.title = title
        self.status = status
        self.detail = detail


class InsuranceProduct:
    """Insurance product."""

    def __init__(self, code, type, description, currency):
        """

        :param code: Code of insurance product, e.g. 'TEST_FLIGHT_PRODUCT'.
        :type code: str
        :param type: Type of insurance product, one of POSSIBLE_PRODUCT_TYPES.
        :type type: str
        :param description: Description of insurance product, e.g. 'Страховка от риска медицинских расходов'.
        :type description: str
        :param currency:
        :type currency: str
        """
        self.code = code
        self.type = type
        self.description = description
        self.currency = currency
