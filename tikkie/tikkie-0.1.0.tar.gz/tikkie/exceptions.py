from typing import Dict, Type

from requests import Response


class BaseError(Exception):
    category: str
    code: str
    message: str
    reference: str
    status: str
    trace_id: str

    def __init__(
        self,
        message: str,
        *,
        response: Response,
        category: str,
        code: str,
        reference: str,
        status: str,
        trace_id: str
    ):
        super().__init__(message)
        self.response = response

        self.category = category
        self.code = code
        self.message = message
        self.reference = reference
        self.status = status
        self.trace_id = trace_id

    @classmethod
    def from_response(cls, response: Response) -> "BaseError":
        payload = response.json()

        # The response schema supports returning multiple errors, but
        # that doesn't make much if you are trying to raise a single exception
        # from the error. Instead, let's just be pragmatic and one parse
        # the first error.
        error: Dict[str, str] = payload["errors"][0]

        category = error["category"]
        code = error["code"]
        message = error["message"]
        reference = error["reference"]
        status = error["status"]
        trace_id = error["traceId"]

        if code.startswith("ERR_8"):
            error_class: Type["BaseError"] = UnknownError
        else:
            for ErrorClass in BaseError.__subclasses__():
                if code == ErrorClass.code:
                    error_class = ErrorClass
                    break
            else:
                # Not implemented exception found, just raise the base class
                error_class = cls

        return error_class(
            message,
            response=response,
            category=category,
            code=code,
            reference=reference,
            status=status,
            trace_id=trace_id,
        )


class UserCouldNotBeCreated(BaseError):
    code = "ERR_1100_001"


class PaymentRequestNotFound(BaseError):
    code = "ERR_1100_002"


class CouldNotSearchForPaymentRequests(BaseError):
    code = "ERR_1100_003"


class InvalidParameters(BaseError):
    code = "ERR_1100_004"


class MissingParameters(BaseError):
    code = "ERR_1100_005"


class OtherErrors(BaseError):
    code = "ERR_1100_006"


class OperationWasNotFound(BaseError):
    code = "ERR_1100_007"


class MaximumNumberOfPlatformsPerClientReached(BaseError):
    code = "ERR_3100_001"


class MaximumNumberOfUsersHasBeenReachedForThisPlatform(BaseError):
    code = "ERR_3100_002"


class ClientNotFound(BaseError):
    code = "ERR_4100_001"


class PlatformNotFound(BaseError):
    code = "ERR_4100_002"


class UserNotFound(BaseError):
    code = "ERR_4100_003"


class UnknownError(BaseError):
    code = "ERR_8XXX_XXX"


class ServiceUnavailable(BaseError):
    code = "ERR_9100_011"


# Common errors


class MalformedAuthorizationHeader(BaseError):
    code = "ERR_1001_001"


class BasicAuthenticationHeaderMissing(BaseError):
    code = "ERR_1002_001"


class AccessTokenHeaderMissing(BaseError):
    code = "ERR_1002_002"


class ApiKeyHeaderMissing(BaseError):
    code = "ERR_1002_003"


class ContainerDepthExceeded(BaseError):
    code = "ERR_1003_001"


class ObjectPropertiesLimitExceeded(BaseError):
    code = "ERR_1003_002"


class ArrayElementsLimitExceed(BaseError):
    code = "ERR_1003_003"


class PropertyNameTooLong(BaseError):
    code = "ERR_1003_004"


class PropertyValueTooLong(BaseError):
    code = "ERR_1003_005"


class RequestMessageMalformed(BaseError):
    code = "ERR_1003_006"


class SoapRequestMessageMalformed(BaseError):
    code = "ERR_1003_007"


class IncorrectOrMissingValue(BaseError):
    code = "ERR_1004_001"


class IncorrectValueOfGrantType(BaseError):
    code = "ERR_1004_002"


class TokenPassedIsNotAValidTokenType(BaseError):
    code = "ERR_1004_003"


class IncorrectValueForClientAssertionType(BaseError):
    code = "ERR_1004_004"


class JwtLifespanTooLong(BaseError):
    code = "ERR_1005_001"


class JwtAttributeIsIncorrect(BaseError):
    code = "ERR_1006_001"


class JwtMissingAttribute(BaseError):
    code = "ERR_1007_001"


class JwtExpired(BaseError):
    code = "ERR_1008_001"


class JwtNotActive(BaseError):
    code = "ERR_1009_001"


class JwtSignatureNotValid(BaseError):
    code = "ERR_1010_001"


class JwtAlgorithmNotSupported(BaseError):
    code = "ERR_1010_002"


class JwtMalformed(BaseError):
    code = "ERR_1011_001"


class InvalidClientIdentifier(BaseError):
    code = "ERR_2001_001"


class InvalidAccessToken(BaseError):
    code = "ERR_2002_001"


class AccessTokenExpired(BaseError):
    code = "ERR_2003_001"


class DeveloperInactiveStatus(BaseError):
    code = "ERR_2004_002"


class RevokedApiKey(BaseError):
    code = "ERR_2004_003"


class InvalidApiKey(BaseError):
    code = "ERR_2005_001"


class ApiKeyCannotBeUsed(BaseError):
    code = "ERR_2005_002"


class IpAddressAcccessDenied(BaseError):
    code = "ERR_3001_001"


class InsufficientScope1(BaseError):
    code = "ERR_3002_001"


class InsufficientScope2(BaseError):
    code = "ERR_3002_002"


class QuotaForTheCallExceeded(BaseError):
    code = "ERR_7001_001"


class TooManyRequests(BaseError):
    code = "ERR_7002_001"


class ServiceIsCurrentlyUnavailable(BaseError):
    code = "ERR_9001_001"
