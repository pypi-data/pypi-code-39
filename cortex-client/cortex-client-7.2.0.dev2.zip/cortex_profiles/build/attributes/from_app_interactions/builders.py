from typing import List

import attr
import pandas as pd

from cortex_common.types.attribute_values import EntityEvent, TotalAttributeValue
from cortex_common.types.attributes import ProfileAttribute, ObservedProfileAttribute
from cortex_common.utils.dataframe_utils import append_seconds_to_df
from cortex_profiles.build.attributes.utils.attribute_constructing_utils import \
    simple_counter_attribute_value_constructor, derive_attributes_from_grouped_df, \
    simple_dimensional_attribute_value_constructor, derive_attributes_from_groups_in_df
from cortex_profiles.build.schemas.builtin_templates import attributes as implicit_attributes
from cortex_profiles.datamodel.dataframes import INTERACTION_DURATIONS_COLS


def derive_attributes_on_total_application_events(events:List[EntityEvent], vocabulary_of_plural_types:dict) -> List[ProfileAttribute]:
    events_df = pd.DataFrame([attr.asdict(x) for x in events]).rename(columns={"entityId": "profileId"})

    if events_df.empty:
        return []

    cols_to_agg_events_by = ["profileId", "entityType", "event", "targetEntityType"]
    aggregated_events_df = events_df[cols_to_agg_events_by + ["triggerId"]].groupby(cols_to_agg_events_by)
        # .aggregate({"triggerId": lambda x: len(list(set(x)))}).reset_index()

    attribute_value_constructor = simple_counter_attribute_value_constructor(
        "triggerId",
        lambda sum: TotalAttributeValue(value=sum),
        counter_deriver=lambda triggerIds: len(list(set(triggerIds)))
    )

    return derive_attributes_from_grouped_df(
        aggregated_events_df,
        cols_to_agg_events_by,
        implicit_attributes.NameTemplates.TOTAL_ENTITY_RELATIONSHIPS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={}
    )


def derive_attributes_on_tallies_of_application_events(events:List[EntityEvent], vocabulary_of_plural_types:dict) -> List[ProfileAttribute]:
    events_df = pd.DataFrame([attr.asdict(x) for x in events]).rename(columns={"entityId": "profileId"})

    if events_df.empty:
        return []

    cols_to_agg_events_by = ["profileId", "entityType", "event", "targetEntityType"]
    aggregated_events_df = events_df[cols_to_agg_events_by + ["targetEntityId", "triggerId"] ].groupby(cols_to_agg_events_by + ["targetEntityId"]).agg({"triggerId": "size"}).reset_index()

    attribute_value_constructor = simple_dimensional_attribute_value_constructor(
        "{targetEntityType}",
        TotalAttributeValue,
        "targetEntityId",
        "triggerId",
        dimension_value_constructor=lambda x: TotalAttributeValue(value=x)
    )

    return derive_attributes_from_groups_in_df(
        aggregated_events_df,
        cols_to_agg_events_by,
        implicit_attributes.NameTemplates.TALLY_ENTITY_RELATIONSHIPS,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={}
        # TODO ... add vocab mapping for additional identifiers ...
    )


def derive_attributes_on_durations_of_application_events(events: List[EntityEvent], vocabulary_of_plural_types: dict) -> List[ProfileAttribute]:
    """
    A timed interaction can not come in parts ... i.e triggerId does not work for it ...
    Cant say viewed google for 30 sec and msft for same 30 sec ...
    :param events:
    :param vocabulary_of_plural_types:
    :return:
    """

    events_df = pd.DataFrame([attr.asdict(x) for x in events]).rename(columns={"entityId": "profileId"})

    if events_df.empty:
        return []

    events_df = events_df.assign(**{
        INTERACTION_DURATIONS_COLS.STARTED_INTERACTION: events_df["properties"].map(lambda x: x[INTERACTION_DURATIONS_COLS.STARTED_INTERACTION]),
        INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION: events_df["properties"].map(lambda x: x[INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION])
    })

    events_df = append_seconds_to_df(
        events_df,
        "duration",
        INTERACTION_DURATIONS_COLS.STARTED_INTERACTION,
        INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION
    )

    cols_to_agg_events_by = ["profileId", "entityType", "event", "targetEntityType"]
    aggregated_events_df = events_df[cols_to_agg_events_by + ["targetEntityId", "duration"]].groupby(
        cols_to_agg_events_by + ["targetEntityId"]).agg({"duration": sum}).reset_index()

    attribute_value_constructor = simple_dimensional_attribute_value_constructor(
        "{targetEntityType}",
        TotalAttributeValue,
        "targetEntityId",
        "duration",
        dimension_value_constructor=lambda x: TotalAttributeValue(value=x)
    )

    return derive_attributes_from_groups_in_df(
        aggregated_events_df,
        cols_to_agg_events_by,
        implicit_attributes.NameTemplates.TOTAL_DURATION_ON_ENTITY_INTERACTION,
        ObservedProfileAttribute,
        attribute_value_constructor,
        additional_identifiers={}
        # TODO ... add vocab mapping for additional identifiers ...
    )


def derive_implicit_attributes_from_application_interactions(events:List[EntityEvent], vocabulary_of_plural_types:dict) -> List[ProfileAttribute]:
    return (
          derive_attributes_on_total_application_events(events, vocabulary_of_plural_types)
        + derive_attributes_on_tallies_of_application_events(events, vocabulary_of_plural_types)
    )


def derive_implicit_attributes_from_timed_application_interactions(events:List[EntityEvent], vocabulary_of_plural_types:dict) -> List[ProfileAttribute]:
    return (
            derive_implicit_attributes_from_application_interactions(events, vocabulary_of_plural_types)
            + derive_attributes_on_durations_of_application_events(events, vocabulary_of_plural_types)
    )