# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
from enum import Enum
import json

import requests

from .exceptions import TESException, AuthErrorException
from .models import (
    ApiRequest, ApiProblem, InsuranceProduct,
    Person, Policy, Segment, Amount,
    ServiceClass, SportKind, FareType, Opt,
    AcquisitionChannel, CancellationType, Declaration,
)
from .models import (
    ConfirmRequest, CreateRequest, CreateResponse, QuoteRequest,
    QuoteResponse,
)

DEFAULT_CURRENCY = 'RUB'
DEFAULT_COUNTRY = 'RU'
DEFAULT_MANAGER = 'AlfaStrahTESClient'


class AlfaStrahTESClient:
    api_host = 'https://vesta.alfastrah.ru'
    base_path = '/travel-ext-services/api/v2'

    def __init__(self, api_key, verify_ssl=True):
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.req = self.resp = self.status_code = None

    def raise_for_error(self):
        """Raises stored :class:`TESException`, if one occurred."""
        if self.status_code is None or self.status_code == 200:
            return
        api_problem = ApiProblem(**self.resp) if self.resp is not None else ApiProblem()
        if self.status_code == 401:
            raise AuthErrorException(api_problem.detail or 'Unauthorized')
        else:
            raise TESException(api_problem.detail or 'Unknown problem')

    def request(self, method, path,
                params=None, data=None, resp_cls=None):
        """Constructs and sends a request to API Gateway.

        :param method: HTTP method, e.g. 'GET', 'POST', 'PUT', 'DELETE'.
        :type method: str
        :param path: API path, e.g. '/products'.
        :type path: str
        :param params: Query parameters to send in query string.
        :type params: Dict or None
        :param data: Request body.
        :type data: ApiRequest or None
        :param resp_cls: Response class.
            This class must contain a static "decode()" method
            that will be called to convert a JSON Python object (API Response) to an instance of this class.
        :type resp_cls: class or None
        :return: JSON API response.
        :rtype: class
        """
        self.req = json.dumps(data, cls=MultiJSONEncoder) if data is not None else None
        self.resp = None
        url = '{api_host}{base_path}{path}'.format(api_host=self.api_host, base_path=self.base_path, path=path)
        headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
        }
        r = requests.request(method, url,
                             headers=headers, params=params, data=self.req, verify=self.verify_ssl)
        try:
            self.resp = r.json()
        except ValueError:
            self.resp = None
        self.status_code = r.status_code
        self.raise_for_error()
        if resp_cls is not None:
            return json.loads(r.content, cls=MultiJSONDecoder, target_type=resp_cls)
        return self.resp

    def get_products(self, product_type=None):
        """Returns list of available insurance products.

        :param product_type: (optional) Returns list of insurance products of the given type only, if specified,
            e.g. 'AIR'.
        :type product_type: str or None
        :returns: List of available insurance products.
        :rtype: list[InsuranceProduct]
        """
        if product_type:
            path = '/products/{type}'.format(type=product_type)
        else:
            path = '/products'
        products = self.request('GET', path, resp_cls=InsuranceProduct)
        return products

    def quote(self, session_id=None, product=None, insureds=None,
              segments=None, booking_price=None, currency=None, service_class=None,
              country=None, sport=None, fare_type=None, luggage_type=None,
              fare_code=None, manager_name=None, manager_code=None, opt=None,
              selling_page=None, end_date=None, acquisition_channel=None):
        """Calculates the cost of one or more insurance policies.

        :param session_id: Session id, e.g. '88c70099-8e11-4325-9239-9c027195c069'.
        :type session_id: str or None
        :param product: Insurance product.
        :type product: InsuranceProduct or None
        :param insureds: List of insured persons.
        :type insureds: list[Person] or None
        :param segments: List of travel segments, e.g. list of flights.
        :type segments: list[Segment] or None
        :param booking_price: Total price of the booking.
        :type booking_price: Amount or None
        :param currency: Quote currency code, ISO 4217, e.g. 'RUB'.
        :type currency: str or None
        :param service_class: Service class.
        :type service_class: ServiceClass or None
        :param country: Country code where the insurance policy will be paid for, ISO 3166-1, e.g. 'RU'.
        :type country: str or None
        :param sport: Insured sports kind.
        :type sport: list[SportKind] or None
        :param fare_type: Refundability.
        :type fare_type: FareType or None
        :param luggage_type: Luggage type.
        :type luggage_type: LuggageType or None
        :param fare_code: Fare code (fare basis), e.g. 'BPXOWRF'.
        :type fare_code: str or None
        :param manager_name: Manager (cashier) code, e.g. 'Ivanova A.A.'.
        :type manager_name: str or None
        :param manager_code: Manager (cashier) code, e.g. '1q2w3e4r'.
        :type manager_code: str or None
        :param opt: Option state.
        :type opt: Opt or None
        :param selling_page: Policy selling page.
        :type selling_page: SellingPage or None
        :param end_date: Expiry date of the policy.
        :type end_date: datetime.datetime or None
        :param acquisition_channel: Acquisition (data collection) channel.
        :type acquisition_channel: AcquisitionChannel or None

        :return: List of quotes.
        :rtype: QuoteResponse
        """
        path = '/policies/quote'
        quote_request = QuoteRequest(
            session_id=session_id, product=product, insureds=insureds,
            segments=segments, booking_price=booking_price, currency=currency, service_class=service_class,
            country=country, sport=sport, fare_type=fare_type, luggage_type=luggage_type,
            fare_code=fare_code, manager_name=manager_name, manager_code=manager_code, opt=opt,
            selling_page=selling_page, end_date=end_date, acquisition_channel=acquisition_channel
        )
        resp = self.request('POST', path, data=quote_request, resp_cls=QuoteResponse)
        return resp

    def create(self, insureds, session_id=None, product=None,
               insurer=None, segments=None, booking_price=None, currency=None,
               discounted_rate=None, service_class=None, pnr=None, customer_email=None,
               customer_phone=None, payment_type=None, sale_session=None, country=None,
               issuance_city=None, sport=None, fare_type=None, luggage_type=None,
               fare_code=None, manager_name=None, manager_code=None, begin_date=None,
               end_date=None, external_id=None, opt=None, selling_page=None,
               acquisition_channel=None):
        """Creates one or more insurance policies.

        :param insureds: List of insured persons.
        :type insureds: list[Person]
        :param session_id: Session id, e.g. '88c70099-8e11-4325-9239-9c027195c069'.
        :type session_id: str or None
        :param product: Insurance product.
        :type product: InsuranceProduct or None
        :param insurer: Insurer.
        :type insurer: Person or None
        :param segments: Travel segments.
        :type segments: list[Segment] or None
        :param booking_price: Total price of the booking.
        :type booking_price: Amount or None
        :param currency: Quote currency code, ISO 4217, e.g. 'RUB'.
        :type currency: str or None
        :param discounted_rate: Discounted rates in different currencies.
        :type discounted_rate: list[Amount] or None
        :param service_class: Service class.
        :type service_class: ServiceClass or None
        :param pnr: Booking number, e.g. 'TR097S'.
        :type pnr: str or None
        :param customer_email: Customer contact email, e.g. 'example@mail.com'.
        :type customer_email: str or None
        :param customer_phone: Customer contact phone, e.g. '+79876543210'.
        :type customer_phone: str or None
        :param payment_type: Form of payment, e.g. 'CARD'.
        :type payment_type: str or None
        :param sale_session: Sale session, e.g. 'PQGWIXCLPY4613323570'.
        :type sale_session: str or None
        :param country: Code of the country where the document was issued, ISO 3166-1, e.g. 'RU'.
        :type country: str or None
        :param issuance_city: City where the policy was issued, e.g. 'Moscow'.
        :type issuance_city: str or None
        :param sport: Insured sports kind.
        :type sport: list[SportKind] or None
        :param fare_type: Refundability.
        :type fare_type: FareType or None
        :param luggage_type: Luggage type.
        :type luggage_type: LuggageType or None
        :param fare_code: Fare code (fare basis), e.g. 'BPXOWRF'.
        :type fare_code: str or None
        :param manager_name: Manager (cashier) code, e.g. 'Ivanova A.A.'.
        :type manager_name: str or None
        :param manager_code: Manager (cashier) code, e.g. '1q2w3e4r'.
        :type manager_code: str or None
        :param begin_date: Start date of the policy.
        :type begin_date: datetime.datetime or None
        :param end_date: Expiry date of the policy.
        :type end_date: datetime.datetime or None
        :param external_id: Policy ID in partner system, e.g. 'FQU/12324264/546546654'.
        :type external_id: str or None
        :param opt: Option state.
        :type opt: Opt or None
        :param selling_page: Policy selling page.
        :type selling_page: SellingPage or None
        :param acquisition_channel: Acquisition (data collection) channel.
        :type acquisition_channel: AcquisitionChannel or None

        :returns: List of created insurance policies.
        :rtype: CreateResponse
        """
        path = '/policies'
        create_request = CreateRequest(
            insureds, session_id=session_id, product=product, insurer=insurer,
            segments=segments, booking_price=booking_price, currency=currency, discounted_rate=discounted_rate,
            service_class=service_class, pnr=pnr, customer_email=customer_email, customer_phone=customer_phone,
            payment_type=payment_type, sale_session=sale_session, country=country, issuance_city=issuance_city,
            sport=sport, fare_type=fare_type, luggage_type=luggage_type, fare_code=fare_code,
            manager_name=manager_name, manager_code=manager_code, begin_date=begin_date, end_date=end_date,
            external_id=external_id, opt=opt, selling_page=selling_page, acquisition_channel=acquisition_channel
        )
        resp = self.request('POST', path, data=create_request, resp_cls=CreateResponse)
        return resp

    def confirm(self, policy_id, session_id=None):
        """Confirms insurance policy.

        :param policy_id: Policy Id, e.g. 21684956.
        :type policy_id: int
        :param session_id: Session id, e.g. '88c70099-8e11-4325-9239-9c027195c069'.
        :type session_id: str or None

        :return: True in case of success.
        :rtype: bool
        """
        path = '/policies/{policy_id}/confirm'.format(policy_id=policy_id)
        confirm_request = ConfirmRequest(session_id=session_id)
        _ = self.request('PUT', path, data=confirm_request)
        return True

    def cancel(self, policy_id,
               type=None, is_ext_id=None, local_date_time=None, body=None):
        """Cancel insurance policy.

        :param policy_id: Policy Id, e.g. 21684956.
        :type policy_id: int

        :param type: Cancellation type.
        :type type: CancellationType or None
        :param is_ext_id: True if the given `policy_id` is an external identifier, default: false.
        :type is_ext_id: bool or None
        :param local_date_time: Use the given datetime as operation date.
            The parameter is processed by the system only by agreement.
        :type: datetime.datetime or None
        :param body: Client's application info.
        :type body: Declaration or None

        :return: Cancellation amount.
        :rtype: Amount
        """
        params = dict()
        if type is not None:
            params['type'] = type.name
        if is_ext_id is not None:
            params['is_ext_id'] = is_ext_id
        if local_date_time is not None:
            params['local_date_time'] = local_date_time.strftime('%Y-%m-%dT%H:%M:%S')
        path = '/policies/{policy_id}'.format(policy_id=policy_id)
        resp = self.request('DELETE', path, data=body, params=params, resp_cls=Amount)
        return resp

    def get_policy(self, policy_id):
        """Retrieves insurance policy info by the given id.

        :param policy_id: Policy Id, e.g. 21684956.
        :type policy_id: int

        :return: Policy.
        :rtype: Policy
        """
        path = '/policies/{policy_id}'.format(policy_id=policy_id)
        policy = self.request('GET', path, resp_cls=Policy)
        return policy


class MultiJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, Enum):
            return o.name
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')

        if hasattr(o, 'encode') and callable(o.encode):
            return o.encode()

        # Let the base class default raise the TypeError
        return json.JSONEncoder.default(self, o)


class MultiJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        self.target_type = kwargs.pop('target_type', None)
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, **kwargs):
        obj = json.JSONDecoder.decode(self, s, **kwargs)

        if isinstance(obj, dict):
            return self.target_type.decode(obj)

        if isinstance(obj, list):
            return [self.target_type.decode(o) for o in obj]

        # None
        return obj
