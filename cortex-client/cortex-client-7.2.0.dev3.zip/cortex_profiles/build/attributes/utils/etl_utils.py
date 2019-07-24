from typing import List

import pandas as pd

from cortex_common.types import EntityEvent
from cortex_profiles.datamodel.dataframes import INSIGHT_COLS, INTERACTIONS_COLS, SESSIONS_COLS, \
    INTERACTION_DURATIONS_COLS

__all__ = [
    "filter_insights_for_profile",
    "filter_interactions_for_profile",
    "filter_sessions_for_profile",
    "filter_events_for_profile",
    "filter_timed_events_for_profile",
    "expand_tag_column",
]

def filter_insights_for_profile(insights_df:pd.DataFrame, profileId:str) -> pd.DataFrame:
    return insights_df[insights_df[INSIGHT_COLS.PROFILEID] == profileId]


def filter_interactions_for_profile(interactions_df:pd.DataFrame, profileId:str) -> pd.DataFrame:
    return interactions_df[interactions_df[INTERACTIONS_COLS.PROFILEID] == profileId]


def filter_sessions_for_profile(sessions_df:pd.DataFrame, profileId:str) -> pd.DataFrame:
    return sessions_df[sessions_df[SESSIONS_COLS.PROFILEID] == profileId]


def filter_events_for_profile(events:List[EntityEvent], profileId:str) -> List[EntityEvent]:
    return list(filter(lambda e: e.entityId == profileId, events))


def filter_timed_events_for_profile(events:List[EntityEvent], profileId:str) -> List[EntityEvent]:
    return list(filter(
        lambda e: INTERACTION_DURATIONS_COLS.STARTED_INTERACTION in e.properties and INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION in e.properties,
        filter_events_for_profile(events, profileId)
    ))


def expand_tag_column(df:pd.DataFrame, tag_column_name:str) -> pd.DataFrame:
    return df.assign(
        taggedConceptType=df[tag_column_name].map(lambda x: x.get("concept").get("context")),
        taggedConceptId=df[tag_column_name].map(lambda x: x.get("concept").get("id")),
        taggedConceptTitle=df[tag_column_name].map(lambda x: x.get("concept").get("title")),
        taggedConceptRelationship=df[tag_column_name].map(lambda x: x.get("relationship").get("id")),
        taggedOn=df[tag_column_name].map(lambda x: x.get("tagged"))
    )

