# -*- coding: utf-8 -*-
from .__version__ import (
    __title__, __description__, __url__, __version__,
    __author__, __author_email__, __license__
)

from .client import AlfaInsTESClient
from .models import (
    ApiProblem, InsuranceProduct, Amount, Person,
    Phone, Document, Ticket, Risk,
    Segment, Point, Gender, PhoneType,
    DocumentType, RiskType, SellingPage, FlightDirection,
    AcquisitionChannel, Policy, QuoteRequest, QuoteResponse,
    Quote, ServiceClass,
)
from .exceptions import TESException, AuthErrorException

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
