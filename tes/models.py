# -*- coding: utf-8 -*-

"""
tes.models
~~~~~~~~~~
This module contains the primary objects.
"""
import datetime
import numbers
import sys
import typing
import uuid
from enum import Enum
from decimal import Decimal

PRODUCT_TYPES = ['AIR']


class ServiceClass(Enum):
    """Service class."""

    ECONOM = 1
    COMFORT = 2
    BUSINESS = 3


class SportKind(Enum):
    """Insured sport."""

    COMMON_SPORT = 1
    DANGEROUS_SPORT = 2


class Gender(Enum):
    """Gender."""

    MALE = 1
    FEMALE = 2


class PhoneType(Enum):
    """Phone type"""

    MOBILE = 1
    HOME = 2
    OFFICE = 3
    OTHER = 4


class DocumentType(Enum):
    """Document type."""

    PASSPORT = 1
    INTERNATIONAL = 2
    IDCARD = 3
    MILITARY = 4
    FOREIGNER = 5
    JURIDICAL = 6
    ERGUL = 7
    DRIVER_LICENCE = 8
    BIRTHCERTIFICATE = 9


class RiskType(Enum):
    """Risk type."""

    RISK_MR = 1
    RISK_NSP = 2
    RISK_NS = 3
    RISK_FLIGHT_DELAYS_PERSONAL = 4
    RISK_SPORT = 5
    RISK_LOSS_LUGGAGE_PERSONAL = 6
    RISK_DELAYED_LUGGAGE_PERSONAL = 7
    RISK_GO = 8
    RISK_LUGGAGE_MASSIVE = 9
    RISK_FLIGHT_DELAYS_MASSIVE = 10
    RISK_NR = 11
    RISK_PROPERTY = 12
    RISK_EVENT = 13
    RISK_LOSS_RESTORE_DOCUMENTS = 14
    RISK_CL = 15
    RISK_LUGGAGE_DAMAGE = 16
    RISK_COVID = 17


class FareType(Enum):
    """Fare type (refundability)."""

    REFUNDABLE = 1
    NO_RETURN = 2


class LuggageType(Enum):
    """Luggage type."""

    STANDARD = 1


class Opt(Enum):
    """Option state."""

    OPT_IN = 1
    OPT_OUT = 2
    SMART_OPT_IN = 3
    SMART_OPT_OUT = 4


class SellingPage(Enum):
    """Selling page."""

    CROSS_SALE = 1
    BOOKING_EDITION = 2
    WEB_CHECK_IN = 3
    STANDALONE = 4


class FlightDirection(Enum):
    OW = 1  # One way
    RT = 2  # Round trip


class AcquisitionChannel(Enum):
    """Acquisition (data collection) channel."""

    DESKTOP = 1
    MOBILE_SITE = 2
    MOBILE_APP = 3
    CROSS_SALE = 4


class BaseModel:
    """Base class with serialization."""

    __attrs__ = []

    def to_json(self):
        json = dict()

        if not hasattr(self, '__attrs__') or not isinstance(self.__getattribute__('__attrs__'), list):
            return json

        for attr in self.__getattribute__('__attrs__'):
            if not hasattr(self, attr) or self.__getattribute__(attr) is None:
                continue
            if isinstance(self.__getattribute__(attr), Enum):
                json[attr] = self.__getattribute__(attr).name
            else:
                json[attr] = self.__getattribute__(attr)

        return json


class BaseModel2:
    __attrs__ = {}

    def __init__(self, *args, **kwargs):
        pass

    def to_json(self):
        json = dict()

        if not hasattr(self, '__attrs__') or not isinstance(self.__getattribute__('__attrs__'), dict):
            return json

        for attr in self.__attrs__.keys():
            if not hasattr(self, attr) or self.__getattribute__(attr) is None:
                continue
            if isinstance(self.__getattribute__(attr), Enum):
                json[attr] = self.__getattribute__(attr).name
            else:
                json[attr] = self.__getattribute__(attr)

        return json

    @classmethod
    def decode(cls, dct):
        def cast(json_value, target_type):
            if json_value is None:
                return None

            if isinstance(json_value, bool) or isinstance(json_value, numbers.Number):
                return json_value

            # TODO: Remove Python2 dependecy
            # isinstance(json_value, str)
            if isinstance(json_value, str if sys.version_info[0] == 3 else basestring):
                if target_type == datetime.date:
                    return datetime.datetime.strptime(json_value, '%Y-%m-%d').date()
                if target_type == datetime.datetime:
                    return datetime.datetime.strptime(json_value, '%Y-%m-%dT%H:%M:%S')
                if issubclass(target_type, Enum):
                    return target_type[json_value]
                return json_value

            if issubclass(target_type, BaseModel2):
                return target_type.decode(dct.get(attr_name)) if dct.get(attr_name) is not None else None

            raise NotImplementedError

        params = {}
        for attr_name, attr_type in cls.__attrs__.items():
            if type(attr_type) == typing.GenericMeta and attr_type.__base__[0] == list:
                params[attr_name] = [cast(o, attr_type.__args__[0]) for o in dct.get(attr_name, [])]
            else:
                params[attr_name] = cast(dct.get(attr_name), attr_type)

        return cls(**params)


class ApiRequest:
    """API request base class."""


class ApiProblem(BaseModel):
    """Description of the error that occurred while handling your request."""

    __attrs__ = [
        'title', 'status', 'detail',
    ]

    def __init__(self, title=None, status=None, detail=None):
        """Init.

        :param title: Short error description, e.g. 'POLICY_NOT_FOUND'.
        :type title: str or None
        :param status: Status code, e.g. 'PNF_002'.
        :type status: str or None
        :param detail: Full error description,
            e.g. 'Policy with id 12345 not found or does not belong to agent'.
        :type detail: str or None
        """
        self.title = title
        self.status = status
        self.detail = detail


class InsuranceProduct(BaseModel2):
    """Insurance product."""

    # __attrs__ = [
    #     'code', 'type', 'description', 'currency',
    # ]

    __attrs__ = {
        'code': str,
        'type': str,
        'description': str,
        'currency': str,
    }

    def __init__(self, code, type=None, description=None, currency=None):
        """Init.

        :param code: Code of insurance product, e.g. 'ON_ANTICOVID_AVIA_1'.
        :type code: str
        :param type: Type of insurance product, one of ``POSSIBLE_PRODUCT_TYPES``, e.g. 'AIR'.
        :type type: str or None
        :param description: Description of insurance product, e.g. 'Страховка от риска медицинских расходов'.
        :type description: str or None
        :param currency: (obsolete) Currency code of the product, ISO 4217, e.g. 'RUB'.
        :type currency: str or None
        """
        self.code = code
        self.type = type
        self.description = description
        self.currency = currency

    # @staticmethod
    # def decode(dct):
    #     """Decodes.
    #
    #     :param dct: Dictionary.
    #     :type dct: dict
    #     """
    #     return InsuranceProduct(**dct)


class Amount(BaseModel):
    """Amount."""

    __attrs__ = [
        'value', 'currency',
    ]

    def __init__(self, value, currency=None):
        """Init.

        :param value: Value, e.g. 35000.
        :type value: Decimal
        :param currency: Currency code, ISO 4217, e.g. 'RUB'.
        :type currency: str or None
        """
        self.value = value
        self.currency = currency

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Amount(**dct)


class PolicyStatus(Enum):
    """Policy status."""

    ISSUING = 1
    CONFIRMED = 2
    CANCELLED = 3
    DELETED = 4


class Operator(BaseModel):
    """Operator."""

    __attrs__ = [
        'code',
    ]

    def __init__(self, code):
        """Init.

        :param code: Operator code.
        :type code: str
        """
        self.code = code

    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Operator(**dct)


class Agent(BaseModel):
    """Agent."""

    __attrs__ = [
        'code', 'sub',
    ]

    def __init__(self, code, sub=None):
        """Init.

        :param code: Agent code, e.g. 'TestTravelFlightAgent'.
        :type code: str
        :param sub: Subagent.
            The subagent code is used to split sales across different channels or divisions within the same agent.
        :type sub: SubAgent or None
        """
        self.code = code
        self.sub = sub

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Agent(**dct)


class SubAgent(BaseModel):
    """Subagent."""

    __attrs__ = [
        'code',
    ]

    def __init__(self, code):
        """Init.

        :param code: Subagent code.
        :type code: str
        """
        self.code = code


class Cancellation(BaseModel):
    """Policy cancellation."""

    __attrs__ = [
        'reason', 'amount',
    ]

    def __init__(self, reason=None, amount=None):
        """Init.

        :param reason: Reason for cancellation of the insurance policy.
        :type reason: str or None
        :param amount: Cancellation (refund) amount.
        :type amount: Amount or None
        """
        self.reason = reason
        self.amount = amount

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Cancellation(
            reason=dct.get('reason'),
            amount=Amount.decode(dct.get('amount')) if dct.get('amount') is not None else None
        )


class ServiceCompany:
    pass


class Person(BaseModel):
    """Person."""

    __attrs__ = [
        'first_name', 'last_name', 'patronymic',
        'nick_name', 'gender', 'birth_date', 'email',
        'address', 'infant', 'nationality', 'id_card',
        'phone', 'document', 'ticket', 'risks',
    ]

    def __init__(self, first_name=None, last_name=None, patronymic=None,
                 nick_name=None, gender=None, birth_date=None, email=None,
                 address=None, infant=None, nationality=None, id_card=None,
                 phone=None, document=None, ticket=None, risks=None):
        """Init.

        :param first_name: First name, e.g. 'Федор'.
        :type first_name: str or None
        :param last_name: Last name, e.g. 'Васильев'.
        :type last_name: str or None
        :param patronymic: Patronymic, e.g. 'Иванович'.
        :type patronymic: str or None
        :param nick_name: Nick, e.g. 'Васильев Федор Иванович'.
        :type nick_name: str or None
        :param gender: Gender.
        :type gender: Gender or None
        :param birth_date: Birth date.
        :type birth_date: datetime.date
        :param email: Email, e.g. 'fedor.vasilyev@email.com'.
        :type email: str or None
        :param address: Address, e.g. 'г. Москва, ул. Иванова, д. 4, кв. 198'.
        :type address: str or None
        :param infant: True if the person is an infant.
        :type infant: bool or None
        :param nationality: Code of country, ISO 3166-1, e.g. 'RU'.
        :type nationality: str or None
        :param id_card: Number of additional document ID, e.g. '5456876321656'.
        :type id_card: str or None
        :param phone: Contact phone.
        :type phone: Phone or None
        :param document: Document ID.
        :type document: Document or None
        :param ticket: Ticket information.
        :type ticket: Ticket or None
        :param risks: Information about risks.
        :type risks: list[Risk] or None
        """
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.nick_name = nick_name
        self.gender = gender
        self.birth_date = birth_date
        self.email = email
        self.address = address
        self.infant = infant
        self.nationality = nationality
        self.id_card = id_card
        self.phone = phone
        self.document = document
        self.ticket = ticket
        self.risks = risks if risks is not None else []

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Person(
            first_name=None, last_name=None, patronymic=None,
            nick_name=None, gender=None, birth_date=None, email=None,
            address=None, infant=None, nationality=None, id_card=None,

            phone=Phone.decode(dct.get('phone')) if dct.get('phone') is not None else None,
            document=Document.decode(dct.get('document')) if dct.get('document') is not None else None,
            ticket=Ticket.decode(dct.get('ticket')) if dct.get('ticket') is not None else None,
            risks=[Risk.decode(risk) for risk in dct.get('risks', [])]
        )


class Phone(BaseModel):
    """Phone."""

    __attrs__ = [
        'number', 'type',
    ]

    def __init__(self, number=None, type=None):
        """Init.

        :param number: Phone number, e.g. '89101234567'.
        :type number: str or None
        :param type: Phone type.
        :type type: PhoneType or None
        """
        self.number = number
        self.type = type

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Phone(
            number=dct.get('number'),
            type=PhoneType[dct.get('type')] if dct.get('type') is not None else None
        )


class Document(BaseModel):
    """Document ID."""

    __attrs__ = [
        'type', 'number', 'country',
    ]

    def __init__(self, type=None, number=None, country=None):
        """Init.

        :param type: Document type.
        :type type: DocumentType or None
        :param number: Document number, e.g. '2901178356'.
        :type number: str or None
        :param country: Code of the country where the document was issued, ISO 3166-1, e.g. 'RU'.
        :type country: str or None
        """
        self.type = type
        self.number = number
        self.country = country

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Document(
            type=DocumentType[dct.get('type')] if dct.get('type') is not None else None,
            number=dct.get('number'),
            country=dct.get('country')
        )


class Ticket(BaseModel):
    """Ticket."""

    __attrs__ = [
        'number', 'price', 'issue_date',
    ]

    def __init__(self, number=None, price=None, issue_date=None):
        """Init.

        :param number: Ticket number, e.g. '5723574320584'.
        :type number: str or None
        :param price: Ticket price.
        :type price: Amount or None
        :param issue_date: Issue date.
        :type issue_date: datetime.date or None
        """
        self.number = number
        self.price = price
        self.issue_date = issue_date

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Ticket(
            number=dct.get('number'),
            price=Amount.decode(dct.get('price')) if dct.get('price') is not None else None,
            issue_date=datetime.datetime.strptime(dct.get('issue_date'), '%Y-%m-%d').date()
            if dct.get('issue_date') is not None else None,
        )


class Risk(BaseModel):
    """Risk."""

    __attrs__ = [
        'type', 'coverage', 'franchise'
    ]

    def __init__(self, type=None, coverage=None, franchise=None):
        """Init.

        :param type: Risk type.
        :type type: RiskType or None
        :param coverage: Insurance amount.
        :type coverage: Amount or None
        :param franchise: Franchise amount.
        :type franchise: Amount or None
        """
        self.type = type
        self.coverage = coverage
        self.franchise = franchise

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Risk(
            type=RiskType[dct.get('type')] if dct.get('type') is not None else None,
            coverage=Amount(dct.get('coverage')) if dct.get('coverage') is not None else None,
            franchise=Amount(dct.get('franchise')) if dct.get('franchise') is not None else None
        )


class Segment(BaseModel):
    """Travel segment."""

    __attrs__ = [
        'transport_operator_code', 'route_number', 'service_class',
        'connection_time', 'departure', 'arrival', 'place_number',
        'car_number', 'car_type', 'connecting_flight', 'flight_direction',
    ]

    def __init__(self, transport_operator_code=None, route_number=None, service_class=None,
                 connection_time=None, departure=None, arrival=None, place_number=None,
                 car_number=None, car_type=None, connecting_flight=None, flight_direction=None):
        """Init.
        
        :param transport_operator_code: Carrier code, e.g. 'SU'.
        :type transport_operator_code: str or None
        :param route_number: Route number (flight number, train number, etc), e.g. '1490'.
        :type route_number: str or None
        :param service_class: Service class.
        :type service_class: ServiceClass or None
        :param connection_time: Connection time in minutes, e.g. 120.
        :type connection_time: int or None
        :param departure: Departure point.
        :type departure: Point or None
        :param arrival: Arrival point.
        :type arrival: Point or None
        :param place_number: Place or seat number, e.g. '56b'.
        :type place_number: str or None
        :param car_number: Train car number, e.g. '12'.
        :type car_number: str or None
        :param car_type: Train car type, e.g. 'SV'.
        :type car_type: str or None
        :param connecting_flight: True if flight is connecting.
        :type connecting_flight: bool or None
        :param flight_direction: Flight direction.
        :type flight_direction: FlightDirection or None
        """
        self.transport_operator_code = transport_operator_code
        self.route_number = route_number
        self.service_class = service_class
        self.connection_time = connection_time
        self.departure = departure
        self.arrival = arrival
        self.place_number = place_number
        self.car_number = car_number
        self.car_type = car_type
        self.connecting_flight = connecting_flight
        self.flight_direction = flight_direction

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Segment(
            transport_operator_code=dct.get('transport_operator_code'),
            route_number=dct.get('route_number'),
            service_class=ServiceClass[dct.get('service_class')] if dct.get('service_class') is not None else None,
            connection_time=dct.get('connection_time'),
            departure=Point.decode(dct.get('departure')) if dct.get('departure') is not None else None,
            arrival=Point.decode(dct.get('arrival')) if dct.get('arrival') is not None else None,
            place_number=dct.get('place_number'),
            car_number=dct.get('car_number'),
            car_type=dct.get('car_type'),
            connecting_flight=dct.get('connecting_flight'),
            flight_direction=FlightDirection['flight_direction'] if dct.get('flight_direction') is not None else None
        )


class TravelType(Enum):
    """Travel type."""

    SINGLE = 1
    MULTIPLE = 2


class Point(BaseModel):
    """Departure or arrival point."""

    __attrs__ = [
        'date', 'point', 'country',
    ]

    def __init__(self, date=None, point=None, country=None):
        """Init.

        :param date: Datetime of departure/arrival.
        :type date: datetime.datetime or None
        :param point: Code of departure/arrival point, e.g. 'SVO'.
        :type point: str or None
        :param country: Code of country, ISO 3166-1, e.g. 'RU'.
        :type country: str or None
        """
        self.date = date
        self.point = point
        self.country = country

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Point(
            date=datetime.datetime.strptime(dct.get('date'), '%Y-%m-%dT%H:%M:%S')
            if dct.get('date') is not None else None,
            point=dct.get('point'),
            country=dct.get('country')
        )


class Policy(BaseModel):
    """Insurance policy."""

    __attrs__ = [
        'policy_id', 'product', 'insured',
        'insurer', 'customer_email', 'customer_phone', 'pnr',
        'series', 'payment_type', 'sale_session', 'issuance_city',
        'external_id', 'commentary', 'description', 'resources',
        'travel_type', 'sport', 'service_company', 'segments',
        'ticket', 'rate', 'discounted_rate', 'begin_date',
        'end_date', 'period_of_validity', 'risks', 'status',
        'created_at', 'update_at', 'fare_type', 'luggage_type',
        'fare_code', 'cancellation', 'operator', 'agent',
        'manager_name', 'manager_code', 'opt', 'selling_page',
        'service_class', 'age_group', 'acquisition_channel', 'error',
    ]

    def __init__(self, policy_id=None, product=None, insured=None,
                 insurer=None, customer_email=None, customer_phone=None, pnr=None,
                 series=None, payment_type=None, sale_session=None, issuance_city=None,
                 external_id=None, commentary=None, description=None, resources=None,
                 travel_type=None, sport=None, service_company=None, segments=None,
                 ticket=None, rate=None, discounted_rate=None, begin_date=None,
                 end_date=None, period_of_validity=None, risks=None, status=None,
                 created_at=None, update_at=None, fare_type=None, luggage_type=None,
                 fare_code=None, cancellation=None, operator=None, agent=None,
                 manager_name=None, manager_code=None, opt=None, selling_page=None,
                 service_class=None, age_group=None, acquisition_channel=None, error=None):
        """Init.

        :param policy_id: Policy ID, e.g. 21684956.
        :type policy_id: int or None
        :param product: Insurance product.
        :type product: InsuranceProduct or None
        :param insured: Insured person.
        :type insured: Person or None
        :param insurer: Insurer.
        :type insurer: Person or None
        :param customer_email: Customer contact email, e.g. 'example@mail.com'.
        :type customer_email: str or None
        :param customer_phone: Customer contact phone, e.g. '+79876543210'.
        :type customer_phone: str or None
        :param pnr: Booking number, e.g. 'TR097S'.
        :type pnr: str or None
        :param series: Policy series, e.g. '247.F'.
        :type series: str or None
        :param payment_type: Form of payment, e.g. 'CARD'.
        :type payment_type: str or None
        :param sale_session: Sale session, e.g. 'PQGWIXCLPY4613323570'.
        :type sale_session: str or None
        :param issuance_city: City where the policy was issued, e.g. 'Moscow'.
        :type issuance_city: str or None
        :param external_id: Policy ID in partner system, e.g. 'FQU/12324264/546546654'.
        :type external_id: str or None
        :param commentary: Comment, e.g. 'PQGWIXCLPY4613323570'.
        :type commentary: str or None
        :param description: Description: risks and insurance premium, e.g.
            'Несчастный случай - 500 000 RUBПотеря багажа - 35 000 RUBПовреждение багажа - 25 000 RUB...'.
        :type description: str or None
        :param resources: Resources, e.g. ['resource1.pdf', 'resource2.pdf'].
        :type resources: list[str] or None
        :param travel_type: Travel type.
        :type travel_type: TravelType or None
        :param sport: Insured sports kind.
        :type sport: list[SportKind] or None
        :param service_company: Service company.
        :type service_company: str or None
        :param segments: Travel segments.
        :type segments: list[Segment] or None
        :param ticket: Ticket.
        :type ticket: Ticket or None
        :param rate: Rates in different currencies.
        :type rate: list[Amount] or None
        :param discounted_rate: Discounted rates in different currencies.
        :type discounted_rate: list[Amount] or None
        :param begin_date: Start date of the policy.
        :type begin_date: datetime.datetime or None
        :param end_date: Expiry date of the policy.
        :type end_date: datetime.datetime or None
        :param period_of_validity: Policy validity period in days, e.g. 14.
        :type period_of_validity: int or None
        :param risks: Information about risks.
        :type risks: list[Risk] or None
        :param status: Policy status.
        :type status: PolicyStatus or None
        :param created_at: Policy created datetime.
        :type created_at: datetime.datetime or None
        :param update_at: Policy updated datetime.
        :type update_at: datetime.datetime or None
        :param fare_type: Refundability.
        :type fare_type: FareType or None
        :param luggage_type: Luggage type.
        :type luggage_type: LuggageType or None
        :param fare_code: Fare code (fare basis), e.g. 'BPXOWRF'.
        :type fare_code: str or None
        :param cancellation: Reason for cancellation of the insurance policy.
        :type cancellation: Cancellation or None
        :param operator: Operator who created the insurance policy.
        :type operator: Operator or None
        :param agent: Agent who owns this policy.
        :type agent: Agent or None
        :param manager_name: Manager (cashier) code, e.g. 'Ivanova A.A.'.
        :type manager_name: str or None
        :param manager_code: Manager (cashier) code, e.g. '1q2w3e4r'.
        :type manager_code: str or None
        :param opt: Option state.
        :type opt: Opt or None
        :param selling_page: Policy selling page.
        :type selling_page: SellingPage or None
        :param service_class: Service class.
        :type service_class: ServiceClass or None
        :param age_group: Age group, e.g. '0-75'.
        :type age_group: str or None
        :param acquisition_channel: Acquisition (data collection) channel.
        :type acquisition_channel: AcquisitionChannel or None
        :param error: Error message.
        :type error: str or None
        """
        self.policy_id = policy_id
        self.product = product
        self.insured = insured
        self.insurer = insurer
        self.customer_email = customer_email
        self.customer_phone = customer_phone
        self.pnr = pnr
        self.series = series
        self.payment_type = payment_type
        self.sale_session = sale_session
        self.issuance_city = issuance_city
        self.external_id = external_id
        self.commentary = commentary
        self.description = description
        self.resources = resources if resources is not None else []
        self.travel_type = travel_type
        self.sport = sport if sport is not None else []
        self.service_company = service_company
        self.segments = segments if segments is not None else []
        self.ticket = ticket
        self.rate = rate if rate is not None else []
        self.discounted_rate = discounted_rate if discounted_rate is not None else []
        self.begin_date = begin_date
        self.end_date = end_date
        self.period_of_validity = period_of_validity
        self.risks = risks if risks is not None else []
        self.status = status
        self.created_at = created_at
        self.update_at = update_at
        self.fare_type = fare_type
        self.luggage_type = luggage_type
        self.fare_code = fare_code
        self.cancellation = cancellation
        self.operator = operator
        self.agent = agent
        self.manager_name = manager_name
        self.manager_code = manager_code
        self.opt = opt
        self.selling_page = selling_page
        self.service_class = service_class
        self.age_group = age_group
        self.acquisition_channel = acquisition_channel
        self.error = error

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Policy(
            policy_id=None, product=None, insured=None,

            insurer=Person.decode(dct.get('insurer')) if dct.get('insurer') is not None else None,
            customer_email=dct.get('customer_email'),
            customer_phone=dct.get('customer_phone'),
            pnr=dct.get('pnr'),
            series=dct.get('series'),
            payment_type=dct.get('payment_type'),
            sale_session=dct.get('sale_session'),
            issuance_city=dct.get('issuance_city'),
            external_id=dct.get('external_id'),
            commentary=dct.get('commentary'),
            description=dct.get('description'),
            resources=[resource for resource in dct.get('resources', [])],
            travel_type=TravelType[dct.get('travel_type')] if dct.get('travel_type') is not None else None,
            sport=[SportKind[sport] for sport in dct.get('sport', [])],
            service_company=dct.get('service_company'),
            segments=[Segment.decode(segment) for segment in dct.get('segments', [])],
            ticket=Ticket.decode(dct.get('ticket')) if dct.get('ticket') is not None else None,
            rate=[Amount.decode(rate) for rate in dct.get('rates', [])],
            discounted_rate=Amount.decode(dct.get('discounted_rate'))
            if dct.get('discounted_rate') is not None else None,
            begin_date=datetime.datetime.strptime(dct.get('begin_date'), '%Y-%m-%dT%H:%M:%S')
            if dct.get('begin_date') is not None else None,
            end_date=datetime.datetime.strptime(dct.get('end_date'), '%Y-%m-%dT%H:%M:%S')
            if dct.get('end_date') is not None else None,
            period_of_validity=dct.get('period_of_validity'),
            risks=[Risk.decode(risk) for risk in dct.get('risks', [])],
            status=PolicyStatus[dct.get('status')] if dct.get('status') is not None else None,
            created_at=datetime.datetime.strptime(dct.get('update_at'), '%Y-%m-%dT%H:%M:%S')
            if dct.get('created_at') is not None else None,
            update_at=datetime.datetime.strptime(dct.get('update_at'), '%Y-%m-%dT%H:%M:%S')
            if dct.get('update_at') is not None else None,
            fare_type=FareType[dct.get('fare_type')] if dct.get('fare_type') is not None else None,
            luggage_type=LuggageType[dct.get('luggage_type')] if dct.get('luggage_type') is not None else None,
            fare_code=dct.get('fare_code'),
            cancellation=Cancellation.decode(dct.get('cancellation')) if dct.get('cancellation') is not None else None,
            operator=Operator.decode(dct.get('operator')) if dct.get('operator') is not None else None,
            agent=Agent.decode(dct.get('agent')) if dct.get('agent') is not None else None,
            manager_name=dct.get('manager_name'),
            manager_code=dct.get('manager_code'),
            opt=Opt[dct.get('opt')] if dct.get('opt') is not None else None,
            selling_page=SellingPage[dct.get('selling_page')] if dct.get('selling_page') is not None else None,
            service_class=ServiceClass[dct.get('service_class')] if dct.get('service_class') is not None else None,
            age_group=dct.get('age_group'),
            acquisition_channel=AcquisitionChannel[dct.get('acquisition_channel')]
            if dct.get('acquisition_channel') is not None else None,
            error=dct.get('error')
        )


class Declaration:
    pass


class QuoteRequest(BaseModel, ApiRequest):
    """Request for calculating one or more insurance policies."""

    __attrs__ = [
        'session_id', 'product', 'insureds',
        'segments', 'booking_price', 'currency', 'service_class',
        'country', 'sport', 'fare_type', 'luggage_type',
        'fare_code', 'manager_name', 'manager_code', 'opt',
        'selling_page', 'end_date', 'acquisition_channel',
    ]

    def __init__(self, session_id=None, product=None, insureds=None,
                 segments=None, booking_price=None, currency=None, service_class=None,
                 country=None, sport=None, fare_type=None, luggage_type=None,
                 fare_code=None, manager_name=None, manager_code=None, opt=None,
                 selling_page=None, end_date=None, acquisition_channel=None):
        """Init.

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
        """
        self.session_id = session_id if session_id is not None else str(uuid.uuid4())
        self.product = product
        self.insureds = insureds if insureds is not None else []
        self.segments = segments if segments is not None else []
        self.booking_price = booking_price
        self.currency = currency
        self.service_class = service_class
        self.country = country
        self.sport = sport
        self.fare_type = fare_type
        self.luggage_type = luggage_type
        self.fare_code = fare_code
        self.manager_name = manager_name
        self.manager_code = manager_code
        self.opt = opt
        self.selling_page = selling_page
        self.end_date = end_date
        self.acquisition_channel = acquisition_channel


class QuoteResponse(BaseModel):
    """Quote response."""

    __attrs__ = [
        'session_id', 'quotes',
    ]

    def __init__(self, session_id=None, quotes=None):
        """Init.

        :param session_id: Session id, e.g. '88c70099-8e11-4325-9239-9c027195c069'.
        :type session_id: str or None
        :param quotes: List of policies for each insured person.
        :type quotes: list[Quote] or None
        """
        self.session_id = session_id
        self.quotes = quotes if quotes is not None else []

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return QuoteResponse(
            session_id=dct.get('session_id'),
            quotes=[Quote.decode(quote) for quote in dct.get('quotes', [])]
        )


class Quote(BaseModel):
    """Quote/Calculating."""

    __attrs__ = [
        'policies', 'error',
    ]

    def __init__(self, policies=None, error=None):
        """Init.

        :param policies: List of policies.
        :type policies: list[Policy]
        :param error: Policy calculating error.
        :type error: str or None
        """
        self.policies = policies if policies is not None else []
        self.error = error

    @staticmethod
    def decode(dct):
        """Decodes.

        :param dct: Dictionary.
        :type dct: dict
        """
        return Quote(
            policies=[Policy.decode(policy) for policy in dct.get('policies', [])],
            error=dct.get('error', None)
        )


class CreateRequest(ApiRequest):
    pass


class CreateResponse:
    pass


class UpdateRequest(ApiRequest):
    pass


class UpdateResponse:
    pass


class ConfirmRequest(ApiRequest):
    pass


class SaleWithoutInsuranceRequest(ApiRequest):
    pass


class SaleWithoutInsuranceResponse:
    pass
