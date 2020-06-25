# -*- coding: utf-8 -*-

"""
tes.models
~~~~~~~~~~
This module contains the primary objects.
"""

import uuid

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


class Person:
    pass


class QuoteRequest:
    """Request for calculating one or more insurance policies."""

    def __init__(self, session_id=None, product=None, insureds=None):
        """Init.

        :param session_id: (optional) Session id, e.g. '88c70099-8e11-4325-9239-9c027195c069'.
        :type session_id: str or None
        :param product: (optional) Insurance product.
        :type product: InsuranceProduct or None
        :param insureds: (optional) List of insured persons.
        :type insureds: list[Person] or None
        """
        self.session_id = session_id if session_id is not None else str(uuid.uuid4())
        self.product = product
        self.insureds = insureds if insureds is not None else []
