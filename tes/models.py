# -*- coding: utf-8 -*-

"""
tes.models
~~~~~~~~~~
This module contains the primary objects.
"""

PRODUCT_TYPES = ['AIR']


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

    def __init__(self, code, type, description, currency=None):
        """Init.

        :param code: Code of insurance product, e.g. 'ON_ANTICOVID_AVIA_1'.
        :type code: str
        :param type: Type of insurance product, one of ``POSSIBLE_PRODUCT_TYPES``, e.g. 'AIR'.
        :type type: str
        :param description: Description of insurance product, e.g. 'Страховка от риска медицинских расходов'.
        :type description: str
        :param currency: (obsolete) Currency code of the product, ISO 4217, e.g. 'RUB'.
        :type currency: str or None
        """
        self.code = code
        self.type = type
        self.description = description
        self.currency = currency
