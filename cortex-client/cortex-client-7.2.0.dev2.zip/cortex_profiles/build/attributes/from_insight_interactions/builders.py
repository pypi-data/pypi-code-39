from typing import List

import pandas as pd
import pydash

from cortex_common.constants.contexts import CONTEXTS
from cortex_common.types.attribute_values import TotalAttributeValue, EntityAttributeValue
from cortex_common.types.attributes import ObservedProfileAttribute, ProfileAttribute
from cortex_common.types.events import EntityEvent
from cortex_common.utils.object_utils import flatten_list_recursively
from cortex_profiles.build.attributes.utils.attribute_constructing_utils import \
    simple_counter_attribute_value_constructor, simple_dimensional_attribute_value_constructor, \
    derive_attributes_from_groups_in_df, derive_attributes_from_df
from cortex_profiles.build.schemas.builtin_templates import attributes as implicit_attributes
from cortex_profiles.datamodel.constants import PROFILE_TYPES
from cortex_profiles.datamodel.dataframes import COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL, \
    TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL, INSIGHT_COLS, INTERACTIONS_COLS
from .attribute_building_utils import derive_count_of_insights_per_interactionType_per_insightType_per_profile, \
    derive_count_of_insights_per_interactionType_per_relatedConcepts_per_profile, \
    derive_time_spent_on_insights_with_relatedConcepts, prepare_interactions_per_tag_with_times


def derive_counter_attributes_for_count_of_specific_insight_interactions_per_insight_type(interactions_df:pd.DataFrame, insights_df:pd.DataFrame) -> List[ObservedProfileAttribute]:

    insight_interactions_df = derive_count_of_insights_per_interactionType_per_insightType_per_profile(interactions_df, insights_df)

    if insight_interactions_df.empty:
        return []

    attribute_value_constructor = simple_counter_attribute_value_constructor(
        "total",
        lambda x: TotalAttributeValue(value=x, unitTitle="insights")
    )

    return derive_attributes_from_groups_in_df(
        insight_interactions_df,
        [
            INTERACTIONS_COLS.PROFILEID,
            INSIGHT_COLS.INSIGHTTYPE,
            INTERACTIONS_COLS.INTERACTIONTYPE
        ],
        implicit_attributes.NameTemplates.COUNT_OF_INSIGHT_INTERACTIONS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={}
    )


def derive_dimensional_attributes_for_count_of_specific_insight_interactions_per_encountered_tag(interactions_df:pd.DataFrame, insights_df:pd.DataFrame) -> List[ObservedProfileAttribute]:

    tag_specific_interactions_df = derive_count_of_insights_per_interactionType_per_relatedConcepts_per_profile(interactions_df, insights_df)

    if tag_specific_interactions_df.empty:
        return []

    attribute_value_constructor =  simple_dimensional_attribute_value_constructor(
        f"{{{COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE}}}",  # Use the TAGGEDCONCEPTTYPE column as the context of the dimensionId
        TotalAttributeValue,
        COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTID,
        COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TOTAL,
        dimension_value_constructor=lambda x: TotalAttributeValue(value=x, unitTitle="insights"),
    )

    return derive_attributes_from_groups_in_df(
        tag_specific_interactions_df[
            tag_specific_interactions_df[COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP] == CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP
        ],
        [
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.PROFILEID,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE
        ],
        implicit_attributes.NameTemplates.COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={}
    )


def derive_dimensional_attributes_for_total_duration_of_specific_insight_interactions_per_encountered_tag(interactions_df:pd.DataFrame, insights_df:pd.DataFrame) -> List[ObservedProfileAttribute]:

    tag_specific_interactions_with_times_df = derive_time_spent_on_insights_with_relatedConcepts(
        prepare_interactions_per_tag_with_times(interactions_df, insights_df)
    )

    if tag_specific_interactions_with_times_df.empty:
        return []

    attribute_value_constructor = simple_dimensional_attribute_value_constructor(
        f"{{{TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE}}}",
        TotalAttributeValue,
        TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTID,
        TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TOTAL,
        dimension_value_constructor=lambda x: TotalAttributeValue(value=x, unitTitle="seconds"),
    )

    return derive_attributes_from_groups_in_df(
        tag_specific_interactions_with_times_df[
            tag_specific_interactions_with_times_df[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP] == CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP
        ],
        [
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.PROFILEID,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE
        ],
        implicit_attributes.NameTemplates.TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={}
    )


def derive_entity_event_attributes_for_each_interaction(interactions_df, insights_df, conceptTypesToConsider:str) -> List[ProfileAttribute]:
    tag_specific_interactions_with_times_df = prepare_interactions_per_tag_with_times(interactions_df, insights_df)

    if tag_specific_interactions_with_times_df.empty:
        return []

    attribute_value_constructor = lambda x: EntityAttributeValue(value=EntityEvent(
        event=implicit_attributes.NameTemplates.ENTITY_INTERACTION_INSTANCE.format(**pydash.merge({}, x)),
        entityId=x[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.PROFILEID],
        entityType=PROFILE_TYPES.END_USER,
        eventTime=x.get(TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.ISOUTCSTARTTIME),
        targetEntityId=x[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTID],
        targetEntityType=x[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE],
        properties={
            "interaction": x[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE],
            "started": x.get(TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.ISOUTCSTARTTIME),
            "ended": x.get(TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.ISOUTCENDTIME),
        }
    ))

    return derive_attributes_from_df(
        tag_specific_interactions_with_times_df[
            (tag_specific_interactions_with_times_df[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP] == CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP)
          & (tag_specific_interactions_with_times_df[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE] == conceptTypesToConsider)
        ],
        implicit_attributes.NameTemplates.ENTITY_INTERACTION_INSTANCE,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={}
    )


def derive_implicit_attributes_from_insight_interactions(
        insights_df: pd.DataFrame, interactions_df: pd.DataFrame, sessions_df: pd.DataFrame,
        concepts_to_create_interaction_instances_for:List[str]=[]
    ) -> List[ProfileAttribute]:
    """

    Derives all of the implicitly generated attributes for a user ...
    Recency has been pulled out ... if you want a recent profile vs a historic profile ... make a seperate schema for it ...

    This is the main method that derives most of the implicit attributes from insights, and feedback ...
    TODO ... make it so that sessions can be optionally provided ... since it can be autoderived ...
    TODO .. rip out sessions and concepts_to_create_interaction_instances_for

    :param timerange:
    :param insights_df:
    :param interactions_df:
    :param sessions_df:
    :return:
    """
    return flatten_list_recursively(
        [
            derive_counter_attributes_for_count_of_specific_insight_interactions_per_insight_type(
                interactions_df, insights_df
            ),
            derive_dimensional_attributes_for_count_of_specific_insight_interactions_per_encountered_tag(
                interactions_df, insights_df
            ),
            derive_dimensional_attributes_for_total_duration_of_specific_insight_interactions_per_encountered_tag(
                interactions_df, insights_df
            ),
        ]
        +
        [
            derive_entity_event_attributes_for_each_interaction(interactions_df, insights_df, cType)
            for cType in concepts_to_create_interaction_instances_for
        ]
    )
