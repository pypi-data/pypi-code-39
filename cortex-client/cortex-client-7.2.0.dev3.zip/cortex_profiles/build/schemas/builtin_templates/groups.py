from cortex_common.types import ProfileFacetSchema
from cortex_common.utils.config_utils import AttrsAsDict


class ImplicitGroupDescriptions(AttrsAsDict):
    ATTRIBUTE_TYPE = "What tags capture of the different classifications of the attributes?"
    CLASSIFICATIONS = "What tags help classify attributes?"
    SUBJECTS = "What tags represent the conceptual essences of attributes?"
    INTERACTION = "What tags capture the different interactions attributes can be optionally related to?"
    APP_ASSOCIATED = "What tags capture the different apps attributes can be optionally related to?"
    ALGO_ASSOCIATED = "What tags capture the different algos attributes can be optionally related to?"
    CONCEPT_ASSOCIATED = "What tags capture the different concepts attributes can be optionally related to?"
    USAGE = "What tags capture how an attribute is intended to be used?"


class ImplicitGroups(AttrsAsDict):
    ATTRIBUTE_TYPE = ProfileFacetSchema(
        name="attr", label="ATTR-TYPE", description=ImplicitGroupDescriptions.ATTRIBUTE_TYPE)
    CLASSIFICATIONS = ProfileFacetSchema(
        name="info", label="INFO-TYPE", description=ImplicitGroupDescriptions.CLASSIFICATIONS)
    SUBJECTS = ProfileFacetSchema(
        name="subject", label="SUBJECTS", description=ImplicitGroupDescriptions.SUBJECTS)
    INTERACTION = ProfileFacetSchema(
        name="interaction", label="INTERACTIONS", description=ImplicitGroupDescriptions.INTERACTION)
    APP_ASSOCIATED = ProfileFacetSchema(
        name="app", label="APPS", description=ImplicitGroupDescriptions.APP_ASSOCIATED)
    ALGO_ASSOCIATED = ProfileFacetSchema(
        name="algo", label="INSIGHTS", description=ImplicitGroupDescriptions.ALGO_ASSOCIATED)
    CONCEPT_ASSOCIATED = ProfileFacetSchema(
        name="concept", label="CONCEPTS", description=ImplicitGroupDescriptions.CONCEPT_ASSOCIATED)
    USAGE = ProfileFacetSchema(
        name="usage", label="USAGE", description=ImplicitGroupDescriptions.USAGE)
