from cortex_profiles.build.schemas.builtin_templates.tags import ImplicitAttributeSubjects
from cortex_profiles.build.schemas.builtin_templates.vocabulary import tag_template, attr_template


class HierarchyDescriptionTemplates(object):
    GENERAL = "Group of general attributes that are applicable across use cases."
    INSIGHT_INTERACTION = "Group of attributes related to the profile's interactions on insights."
    APPLICATION_USAGE = "Group of attributes related to information on the profile's application usage."
    MEANINGFUL_INTERACTIONS = "Group of attributes related to a profile's meaingful interactions with the system."
    APP_SPECIFIC = attr_template("Group of attributes related to the {{{app_title}}} app.")
    ALGO_SPECIFIC = attr_template("Group of attributes related to the {{{insight_type}}} algo.")
    CONCEPT_SPECIFIC = "Group of attributes related to different concepts in the system."
    CONCEPT_AGNOSTIC = "Group of attributes that are independent of the different concepts in the system."


class HierarchyNameTemplates(object):
    GENERAL = "general"
    INSIGHT_INTERACTION = ImplicitAttributeSubjects.INSIGHT_INTERACTIONS
    APPLICATION_USAGE = ImplicitAttributeSubjects.APP_USAGE
    MEANINGFUL_INTERACTIONS = ImplicitAttributeSubjects.INTERACTIONS
    APP_SPECIFIC = tag_template("app::{{{app_id}}}")
    ALGO_SPECIFIC = tag_template("algo::{{{insight_type_id}}}")
    CONCEPT_SPECIFIC = "concept-specific"
    CONCEPT_AGNOSTIC = "concept-agnostic"
