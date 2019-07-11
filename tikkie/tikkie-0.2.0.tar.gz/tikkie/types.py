from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional

from tikkie._utils import cents_to_decimal, parse_datetime


class PlatformUsage(Enum):
    PAYMENT_REQUEST_FOR_MYSELF = "Payment request for myself"
    PAYMENT_REQUEST_FOR_OTHERS = "Payment request for others"


class PlatformStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class UserStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


@dataclass
class AccessToken:
    access_token: str
    expires_in: int
    scope: str
    token_type: str


@dataclass
class Platform:
    name: str
    platform_token: str
    phone_number: str
    email: str
    notification_url: str
    status: PlatformStatus
    platform_usage: PlatformUsage
    raw_response: Optional[dict] = field(default=None, repr=False, compare=False)

    @classmethod
    def from_response(cls, r: Dict[str, str]) -> "Platform":
        return cls(
            name=r["name"],
            platform_token=r["platformToken"],
            phone_number=r["phoneNumber"],
            email=r["email"],
            notification_url=r["notificationUrl"],
            status=PlatformStatus[r["status"]],
            platform_usage=PlatformUsage[r["platformUsage"]],
            raw_response=r,
        )


@dataclass
class BankAccount:
    bank_account_token: str
    iban: str
    bank_account_label: str

    @classmethod
    def from_response(cls, r: Dict[str, str]) -> "BankAccount":
        return cls(
            bank_account_token=r["bankAccountToken"],
            iban=r["iban"],
            bank_account_label=r["bankAccountLabel"],
        )


@dataclass
class User:
    user_token: str
    name: str
    status: UserStatus
    bank_accounts: List[BankAccount]
    raw_response: Optional[dict] = field(default=None, repr=False, compare=False)

    @classmethod
    def from_response(cls, r: Dict[str, Any]) -> "User":
        return cls(
            user_token=r["userToken"],
            name=r["name"],
            status=UserStatus[r["status"]],
            bank_accounts=[BankAccount.from_response(b) for b in r["bankAccounts"]],
            raw_response=r,
        )


class OnlinePaymentStatus(Enum):
    NEW = "New"
    PENDING = "Pending"
    PAID = "Paid"
    NOT_PAID = "Not paid"


@dataclass
class Payment:
    payment_token: str
    counter_party_name: str
    amount: Decimal
    amount_currency: str
    description: str
    created: datetime
    online_payment_status: OnlinePaymentStatus
    raw_response: Optional[dict] = field(default=None, repr=False, compare=False)

    @classmethod
    def create_from_response(cls, r: Dict[str, Any]) -> "Payment":
        return cls(
            payment_token=r["paymentToken"],
            counter_party_name=r["counterPartyName"],
            amount=cents_to_decimal(r["amountInCents"]),
            amount_currency=r["amountCurrency"],
            description=r["description"],
            created=parse_datetime(r["created"]),
            online_payment_status=OnlinePaymentStatus[r["onlinePaymentStatus"]],
        )


class PaymentRequestStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    EXPIRED = "Expired"
    MAX_YIELD_REACHED = "Max yield reached"
    MAX_SUCCESSFUL_PAYMENTS_REACHED = "Max successful payments reached"


@dataclass
class PaymentRequest:
    payment_request_token: str
    amount: Optional[Decimal]
    currency: str
    description: str
    created: datetime
    expired: Optional[datetime]
    status: PaymentRequestStatus
    bank_account_yielded_too_fast: bool
    external_id: str
    payments: List[Payment]
    raw_response: Optional[dict] = field(default=None, repr=False, compare=False)

    @classmethod
    def create_from_response(cls, r: Dict[str, Any]) -> "PaymentRequest":
        return cls(
            payment_request_token=r["paymentRequestToken"],
            amount=cents_to_decimal(r["amountInCents"]),
            currency=r["currency"],
            description=r["description"],
            created=parse_datetime(r["created"]),
            expired=parse_datetime(r["expired"]) if r["expired"] else r["expired"],
            status=PaymentRequestStatus[r["status"]],
            bank_account_yielded_too_fast=r["bankAccountYieldedTooFast"],
            external_id=r["externalId"],
            payments=[Payment.create_from_response(p) for p in r["payments"]],
            raw_response=r,
        )


@dataclass
class UserPaymentRequestResponse:
    payment_requests: List[PaymentRequest]
    total_elements: int
    raw_response: Optional[dict] = field(default=None, repr=False, compare=False)

    @classmethod
    def create_from_response(cls, r: Dict[str, Any]) -> "UserPaymentRequestResponse":
        return cls(
            payment_requests=[PaymentRequest.create_from_response(p) for p in r["paymentRequests"]],
            total_elements=r["totalElements"],
            raw_response=r,
        )


@dataclass
class CreatePaymentRequestResponse:
    payment_request_url: str
    payment_request_token: str
    external_id: str
    raw_response: Optional[dict] = field(default=None, repr=False, compare=False)

    @classmethod
    def create_from_response(cls, r: Dict[str, str]) -> "CreatePaymentRequestResponse":
        return cls(
            payment_request_url=r["paymentRequestUrl"],
            payment_request_token=r["paymentRequestToken"],
            external_id=r["externalId"],
            raw_response=r,
        )
