# -*- coding: utf-8 -*-

"""
tes.models
~~~~~~~~~~
This module contains the primary objects.
"""

PRODUCT_TYPES = ['FLIGHT', 'FLIGHT_TRAVEL', 'TRAVEL', 'RAILWAY', 'PROPERTY', 'EVENT', 'BUS', 'TAXI']


class ApiProblem:
    """Description of the error that occurred while handling your request."""

    def __init__(self, title, status, detail):
        """Init.

        :param title: short error description, e.g. 'POLICY_NOT_FOUND'.
        :type title: str
        :param status: status code, e.g. 'PNF_002'.
        :type status: str
        :param detail: full error description, e.g. 'Policy with id 12345 not found or does not belong to agent'.
        :type detail: str
        """
        self.title = title
        self.status = status
        self.detail = detail


class InsuranceProduct:
    """Insurance product."""

    def __init__(self, code, product_type, description):
        """

        :param code: code of insurance product, e.g. 'TEST_FLIGHT_PRODUCT'.
        :type code: str
        :param product_type: type of insurance product, one of POSSIBLE_PRODUCT_TYPES.
        :type product_type: str
        :param description: description of insurance product, e.g. 'Страховка от риска медицинских расходов'.
        :type description: str
        """
        self.code = code
        self.product_type = product_type
        self.description = description

        self.currency = 'RUB'
