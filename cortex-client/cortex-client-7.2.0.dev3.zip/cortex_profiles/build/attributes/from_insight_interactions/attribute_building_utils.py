import pandas as pd

from cortex_common.constants.contexts import CONTEXTS
from cortex_common.utils.dataframe_utils import append_seconds_to_df, determine_count_of_occurrences_of_grouping
from cortex_profiles.datamodel.constants import INTERACTIONS
from cortex_profiles.datamodel.dataframes import COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL, \
    TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL, INSIGHT_COLS, INTERACTIONS_COLS
from .etl_utils import merge_interactions_with_insights, append_interaction_time_to_df_from_properties


def derive_count_of_insights_per_interactionType_per_insightType_per_profile(insight_interactions_df: pd.DataFrame, insights_df: pd.DataFrame) -> pd.DataFrame:
    """
    For every profile, what is the total count of insights relevant to the profile that the profile interacted with in
        different ways {liked, disliked, ...} per type of insight {Investmnet Insight, Retirement, ...}
    :param insight_interactions_df:
    :param insights_df:
    :return:
    """
    insight_transitions_events_with_types = pd.merge(
        insight_interactions_df,
        insights_df[[INSIGHT_COLS.ID, INSIGHT_COLS.INSIGHTTYPE]],
        left_on=INTERACTIONS_COLS.INSIGHTID, right_on=INSIGHT_COLS.ID, how="inner"
    )
    return determine_count_of_occurrences_of_grouping(
        insight_transitions_events_with_types, [INTERACTIONS_COLS.PROFILEID, INSIGHT_COLS.INSIGHTTYPE, INTERACTIONS_COLS.INTERACTIONTYPE]
    )


def derive_count_of_insights_per_interactionType_per_relatedConcepts_per_profile(
        insight_interactions_df: pd.DataFrame, insights_df: pd.DataFrame) -> pd.DataFrame:
    """
    For every profile, what is the total number count of insights relevant to the profile that transitioned
        to each of the different states {liked, disliked, ...} per related concept {Investment Insight, Retirement, ...}
    :param insight_interactions_df:
    :param insights_df:
    :return:
    """

    expanded_insight_interactions_df = merge_interactions_with_insights(insight_interactions_df, insights_df)

    filtered_interactions_with_tags = expanded_insight_interactions_df[
        expanded_insight_interactions_df[COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP] == CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP
        ]

    return filtered_interactions_with_tags.assign(total=1).groupby(
        [
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.PROFILEID,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTID,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTITLE,  # Not really an id ... but wanted to preserve it post agg ...
        ]
    ).agg({
        COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TOTAL: 'size',
        COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDON: lambda x: list(sorted(x))
    }).reset_index()


def derive_count_of_insights_per_interactionType_per_relatedConcepts(
        insight_interactions_df: pd.DataFrame, insights_df: pd.DataFrame) -> pd.DataFrame :
    """
    What is the total number of insights that transitioned to each of the different states {liked, disliked, ...}
        per related concept {Investment Insight, Retirement, ...}
    :param insight_interactions_df:
    :param insights_df:
    :return:
    """

    expanded_insight_interactions_df = merge_interactions_with_insights(insight_interactions_df, insights_df)

    filtered_interactions_with_tags = expanded_insight_interactions_df[
        expanded_insight_interactions_df[COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP] == CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP
        ]

    return filtered_interactions_with_tags.assign(total=1).groupby(
        [
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTID,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTITLE,
        ]
    ).agg({
        COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TOTAL: 'size',
        COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDON: lambda x: list(sorted(x))
    }).reset_index()


def prepare_interactions_per_tag_with_times(insight_interactions_df:pd.DataFrame, insights_df:pd.DataFrame) -> pd.DataFrame :

    expanded_insight_interactions_df = merge_interactions_with_insights(
        append_interaction_time_to_df_from_properties(insight_interactions_df),
        insights_df
    )
    if expanded_insight_interactions_df.empty:
        return pd.DataFrame(columns=TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.values())
    interactions_about_related_concepts_mask = expanded_insight_interactions_df[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP] == CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP
    interactions_about_views_mask = expanded_insight_interactions_df[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE] == INTERACTIONS.VIEWED
    filtered_interactions_with_times = expanded_insight_interactions_df[(interactions_about_related_concepts_mask) & (interactions_about_views_mask)]
    return filtered_interactions_with_times


def derive_time_spent_on_insights_with_relatedConcepts(insight_interactions_with_time_df: pd.DataFrame) -> pd.DataFrame :
    return append_seconds_to_df(
            insight_interactions_with_time_df,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TOTAL,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.ISOUTCSTARTTIME,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.ISOUTCENDTIME
        ).groupby([
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.PROFILEID,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTID,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTITLE,  # Not really an id ... but wanted to preserve it post agg ...
        ], as_index=False).agg({
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TOTAL: 'sum',
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDON: lambda x: list(sorted(x))
        }).reset_index()
