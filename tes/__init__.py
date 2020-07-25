# -*- coding: utf-8 -*-
from .__version__ import (
    __title__, __description__, __url__, __version__,
    __author__, __author_email__, __license__
)

from .client import AlfaInsTESClient, MultiJSONEncoder
from .models import (
    BaseModel, ApiRequest, ApiProblem,
    InsuranceProduct, Amount, PolicyStatus, Operator,
    Agent, SubAgent, Cancellation, ServiceCompany,
    Person, Phone, Document, Ticket,
    Risk, Segment, TravelType, Point,
    Gender, PhoneType, DocumentType, RiskType,
    FareType, LuggageType, Opt, SellingPage,
    FlightDirection, AcquisitionChannel, Policy, Declaration,
    QuoteRequest, QuoteResponse, Quote, CreateRequest,
    CreateResponse, UpdateRequest, UpdateResponse, ConfirmRequest,
    SaleWithoutInsuranceRequest, SaleWithoutInsuranceResponse, ServiceClass, SportKind,
)
from .exceptions import TESException, AuthErrorException

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
