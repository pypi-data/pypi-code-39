class StreetError(Exception):
    pass


class DistilIdentificationBlocked(StreetError):
    pass


class EarningsTableEmpty(StreetError):
    pass


class EarningsTableNotFound(StreetError):
    pass


class RequestBlocked(StreetError):
    pass


class ResourceMovedTemporarily(StreetError):
    pass


class UnforeseenResponseStatusCode(StreetError):
    pass