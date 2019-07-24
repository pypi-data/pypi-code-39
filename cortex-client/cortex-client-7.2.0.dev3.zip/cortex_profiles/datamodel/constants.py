from cortex_common.constants.contexts import CONTEXTS
from cortex_common.utils.config_utils import AttrsAsDict


__all__ = [
    "TIMEFRAMES",
    "PROFILE_TYPES",
    "UNIVERSAL_ATTRIBUTES",
    "DOMAIN_CONCEPTS",
    "INTERACTIONS",
]

class TIMEFRAMES(AttrsAsDict):
    HISTORIC = "eternally"
    RECENT = "recently"


class PROFILE_TYPES(AttrsAsDict):
    END_USER = "cortex/profile-of-end-user"
    INVESTOR = "cortex/profile-of-investor"
    SHOPPER = "cortex/profile-of-dress-shopper"


class UNIVERSAL_ATTRIBUTES(AttrsAsDict):
    TYPES = "profile.types"

    @staticmethod
    def keys():
        return list(filter(lambda x: x[0] != "_", CONTEXTS.__dict__.keys()))


class DOMAIN_CONCEPTS(AttrsAsDict):
    PERSON="cortex/person"
    COUNTRY="cortex/country"
    CURRENCY="cortex/currency"
    COMPANY="cortex/company"
    WEBSITE="cortex/website"


class INTERACTIONS(AttrsAsDict):
    CONTEXT=CONTEXTS.INSIGHT_INTERACTION
    PRESENTED="presented"
    VIEWED="viewed"
    IGNORED="ignored"
