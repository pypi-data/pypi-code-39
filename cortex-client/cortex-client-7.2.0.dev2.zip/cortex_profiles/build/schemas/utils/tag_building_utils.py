from typing import List, Mapping

from cortex_common.constants.contexts import ATTRIBUTES
from cortex_profiles.build.schemas.builtin_templates.groups import ImplicitGroups
from cortex_profiles.build.schemas.builtin_templates.tags import ImplicitTags, ImplicitTagTemplates
from cortex_profiles.build.schemas.builtin_templates.vocabulary import APP_ID, INSIGHT_TYPE, CONCEPT, \
    INTERACTION_TYPE


def expand_tags_for_profile_attribute(cand:Mapping[str, str], attribute_context:str, subject:str) -> List[str]:
    """
    Determines which tags are applicable to a specific attribute ... based on the candidate being expanded ...
    Subjects lead to additional tags ...

    :param cand:
    :param attribute_context:
    :param subject:
    :return:
    """
    interaction_tag = None if INTERACTION_TYPE not in cand else ImplicitTagTemplates.INTERACTION(cand).name
    insight_interaction_tag = None if interaction_tag is None else ImplicitTags.INSIGHT_INTERACTIONS.name

    app_association_tag = None if APP_ID not in cand else ImplicitTagTemplates.APP_ASSOCIATED(cand).name
    app_specific_tag = None if app_association_tag is None else ImplicitTags.APP_SPECIFIC.name

    algo_association_tag = None if INSIGHT_TYPE not in cand else ImplicitTagTemplates.ALGO_ASSOCIATED(cand).name
    concept_association_tag = None if CONCEPT not in cand else ImplicitTagTemplates.CONCEPT_ASSOCIATED(cand).name

    # These two tags should be mutually exclusive ...
    concept_specific_tag = None if concept_association_tag is None else ImplicitTags.CONCEPT_SPECIFIC.name
    concept_agnostic_tag = None if concept_specific_tag is not None else ImplicitTags.CONCEPT_AGNOSTIC.name

    classification_tag = {
        ATTRIBUTES.DECLARED_PROFILE_ATTRIBUTE: ImplicitTags.DECLARED.name,
        ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE: ImplicitTags.OBSERVED.name,
        ATTRIBUTES.INFERRED_PROFILE_ATTRIBUTE: ImplicitTags.INFERRED.name,
        ATTRIBUTES.ASSIGNED_PROFILE_ATTRIBUTE: ImplicitTags.ASSIGNED.name,
    }.get(attribute_context, None)

    subject_tag = None if not subject else "{}/{}".format(ImplicitGroups.SUBJECTS.name, subject)
    return list(filter(
        lambda x: x,
        [
            interaction_tag, app_association_tag, algo_association_tag, concept_association_tag, classification_tag, subject_tag,
            concept_specific_tag, concept_agnostic_tag, app_specific_tag, insight_interaction_tag
        ]
    ))