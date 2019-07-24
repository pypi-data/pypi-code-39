from collections import Counter
from typing import List, Union

import pandas as pd
from cortex_common.types.attribute_values import ListAttributeValue
from cortex_common.types.attributes import ProfileAttribute, AssignedProfileAttribute, ObservedProfileAttribute
from cortex_common.utils.class_utils import state_modifier
from cortex_profiles.build.attributes.declared import derive_declared_attributes_from_value_only_df
from cortex_profiles.build.attributes.from_insight_interactions.builders import \
    derive_implicit_attributes_from_insight_interactions
from cortex_profiles.build.attributes.from_sessions.builders import derive_implicit_attributes_from_sessions
from cortex_profiles.datamodel.constants import UNIVERSAL_ATTRIBUTES, PROFILE_TYPES


# TODO ... move this over to the right place ...
def derive_implicit_attributes_for_counts_of_concepts_present_in_insights(insights_df: pd.DataFrame, conceptType) -> List[ProfileAttribute]:
    # Generic ...
    # Count of concepts of a specific type present in an insight ...
    df = pd.DataFrame([
        {"profileId": profileId, "count": count}
        for profileId, count in Counter([
            tag["concept"]["id"] for tags in insights_df["tags"] for tag in tags if tag["concept"]["context"] == conceptType
        ]).items()
    ])
    return derive_declared_attributes_from_value_only_df(
        df, "count", key=f"occurances.{conceptType}.inInsights"
    )


def derive_implicit_profile_type_attribute(profileId:str, profileTypes:List[str]=[PROFILE_TYPES.END_USER]) -> AssignedProfileAttribute:
    return AssignedProfileAttribute(  # type: ignore
        profileId = profileId,
        attributeKey = UNIVERSAL_ATTRIBUTES.TYPES,
        attributeValue = ListAttributeValue(profileTypes)
    )


# Todo ... should we have a builder for entities that consume insights, and another for entities mentioned in insights?
class ImplicitAttributesBuilder(object):

    def __init__(self):
        self.attributes = [ ]

    @state_modifier(derive_implicit_attributes_from_insight_interactions, (lambda self, results: self.attributes.extend(results)))
    def append_implicit_insight_interaction_attributes(self, *args, **kwargs):
        """
        See :func:`.derive_declared_attributes_from_key_value_df` for input argument instructions.
        :return: The builder itself, after its state has been modified with the appended attributes ...
        """
        return self

    @state_modifier(derive_implicit_profile_type_attribute, (lambda self, results: self.attributes.append(results)))
    def append_implicit_type_attribute(self, *args, **kwargs):
        """
        See :func:`.derive_declared_attributes_from_value_only_df` for input argument instructions.
        :return: The builder itself, after its state has been modified with the appended attributes ...
        """
        return self

    @state_modifier(derive_implicit_attributes_from_sessions, (lambda self, results: self.attributes.append(results)))
    def append_implicit_session_attributes(self, *args, **kwargs):
        """
        See :func:`.derive_implicit_attributes_from_sessions` for input argument instructions.
        :return: The builder itself, after its state has been modified with the appended attributes ...
        """
        return self

    def get(self) -> List[Union[AssignedProfileAttribute, ObservedProfileAttribute]]:
        return self.attributes
