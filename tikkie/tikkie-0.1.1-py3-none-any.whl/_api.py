from datetime import datetime
from decimal import Decimal
from time import time
from typing import Any, Dict, List, Optional

import jwt

from tikkie import session
from tikkie._utils import decimal_to_cents, format_datetime
from tikkie.types import (
    AccessToken,
    CreatePaymentRequestResponse,
    PaymentRequest,
    Platform,
    PlatformUsage,
    User,
    UserPaymentRequestResponse,
)


def authenticate() -> None:
    s = session()
    s.access_token = get_access_token()


def get_access_token() -> AccessToken:
    s = session()
    payload = {
        "nbf": int(time()) - 60,
        "exp": int(time()) + 60,
        "sub": s.api_key,
        "iss": "Python Tikkie",
        "aud": s.aud_url,
    }

    token = jwt.encode(payload, s.private_key, algorithm="RS256")

    headers = {"API-Key": s.api_key}

    data: Dict[str, Any] = {
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "grant_type": "client_credentials",
        "client_assertion": token,
    }

    response = s.post(f"v1/oauth/token", is_auth=True, data=data, headers=headers)
    r = response.json()
    return AccessToken(
        access_token=r["access_token"],
        expires_in=int(r["expires_in"]),
        scope=r["scope"],
        token_type=r["token_type"],
    )


def create_user(
    *,
    name: str,
    phone_number: str,
    iban: str,
    bank_account_label: str,
    platform_token: Optional[str] = None,
) -> User:
    """
    This operation will enroll a new user into an existing platform payment.
    """
    s = session()
    pt = s.get_platform_token(platform_token)
    payload = {
        "name": name,
        "phoneNumber": phone_number,
        "iban": iban,
        "bankAccountLabel": bank_account_label,
    }
    response = s.post(f"v1/tikkie/platforms/{pt}/users", json=payload)

    return User.from_response(response.json())


def get_users(platform_token: Optional[str] = None) -> List[User]:
    """
    This operation will fetch all users for an existing platform of a certain API consumer.
    """
    s = session()
    pt = s.get_platform_token(platform_token)
    response = s.get(f"v1/tikkie/platforms/{pt}/users")
    return [User.from_response(u) for u in response.json()]


def get_platforms() -> List[Platform]:
    """
    This operation will fetch all platforms created for a certain API consumer.
    """
    s = session()
    response = s.get(f"v1/tikkie/platforms")
    return [Platform.from_response(p) for p in response.json()]


def create_platform(
    *,
    name: str,
    phone_number: str,
    email: Optional[str] = None,
    notification_url: Optional[str] = None,
    usage: PlatformUsage = PlatformUsage.PAYMENT_REQUEST_FOR_MYSELF,
) -> Platform:
    """
    This operation will enroll a new platform.
    """
    s = session()
    payload = {"name": name, "phoneNumber": phone_number, "platformUsage": usage.name}

    if email is not None:
        payload["email"] = email
    if notification_url is not None:
        payload["notificationUrl"] = notification_url

    response = s.post(f"v1/tikkie/platforms", json=payload)

    return Platform.from_response(response.json())


def get_user_payment_requests(
    user_token: str,
    platform_token: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> UserPaymentRequestResponse:
    """
    Returns all the payment requests for an existing user.

    The results are paginated and the desired offset and limit must be
    specified. Filtering is possible based on the date. When the platform
    has been created with the platformUsage field set to PAYMENT_REQUEST_FOR_OTHERS
    then the payments will be empty.

    :param user_token: Identifies from which user the payment requests are accessed
    :param platform_token: Identifies to which platform the user is enrolled
    :param offset: Pagination: zero based index of the records range to return
    :param limit: Pagination: the number of records to return
    :param from_date: Filtering: only include payment requests created after this date/time
    :param to_date: Filtering: only include payment requests created before this date/time
    """
    s = session()
    pt = s.get_platform_token(platform_token)
    params: Dict[str, Any] = {"offset": offset, "limit": limit}
    if from_date is not None:
        params["fromDate"] = format_datetime(from_date)
    if to_date is not None:
        params["toDate"] = format_datetime(to_date)
    response = s.get(f"v1/tikkie/platforms/{pt}/users/{user_token}/paymentrequests", params=params)
    return UserPaymentRequestResponse.create_from_response(response.json())


def get_payment_request(
    user_token: str, payment_request_token: str, platform_token: Optional[str] = None
) -> PaymentRequest:
    s = session()
    pt = s.get_platform_token(platform_token)
    response = s.get(
        f"v1/tikkie/platforms/{pt}/users/{user_token}/paymentrequests/{payment_request_token}"
    )
    return PaymentRequest.create_from_response(response.json())


def create_payment_request(
    user_token: str,
    bank_account_token: str,
    amount: Decimal,
    currency: str,
    description: str,
    external_id: str,
    platform_token: Optional[str] = None,
) -> CreatePaymentRequestResponse:
    s = session()
    pt = s.get_platform_token(platform_token)

    if not isinstance(amount, Decimal):
        raise TypeError("amount must be a Decimal")

    payload = {
        "amountInCents": decimal_to_cents(amount),
        "currency": currency,
        "description": description,
        "externalId": external_id,
    }
    response = s.post(
        f"v1/tikkie/platforms/{pt}/users/{user_token}/bankaccounts/{bank_account_token}/paymentrequests",
        json=payload,
    )
    return CreatePaymentRequestResponse.create_from_response(response.json())
