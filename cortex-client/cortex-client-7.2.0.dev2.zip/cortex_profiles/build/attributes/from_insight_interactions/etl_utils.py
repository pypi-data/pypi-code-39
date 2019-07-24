import attr
import pandas as pd

from cortex_common.utils import all_values_in_list_are_not_nones_or_nans, filter_time_column_before, explode_column, \
    filter_recent_records_on_column, unique_id
from cortex_profiles.datamodel.constants import CONTEXTS
from cortex_profiles.datamodel.dataframes import INSIGHT_COLS, INTERACTIONS_COLS, INTERACTION_DURATIONS_COLS
from cortex_profiles.types.insights import InsightTag, Link


def append_interaction_time_to_df_from_properties(df:pd.DataFrame) -> pd.DataFrame:
    return df.assign(**{
        INTERACTION_DURATIONS_COLS.STARTED_INTERACTION: df["properties"].map(
            lambda x: x.get(INTERACTION_DURATIONS_COLS.STARTED_INTERACTION)),
        INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION: df["properties"].map(
            lambda x: x.get(INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION)),
    })


def expand_tag_column(df:pd.DataFrame, tag_column_name:str) -> pd.DataFrame:
    return df.assign(
        taggedConceptType=df[tag_column_name].map(lambda x: x.get("concept").get("context")),
        taggedConceptId=df[tag_column_name].map(lambda x: x.get("concept").get("id")),
        taggedConceptTitle=df[tag_column_name].map(lambda x: x.get("concept").get("title")),
        taggedConceptRelationship=df[tag_column_name].map(lambda x: x.get("relationship").get("id")),
        taggedOn=df[tag_column_name].map(lambda x: x.get("tagged"))
    )


def merge_interactions_with_insights(insight_interactions_df:pd.DataFrame, insights_df:pd.DataFrame) -> pd.DataFrame:
    """
    This method not only does a LEFT JOIN of the interaction table with the insight table ...
    it also expands the joined result such that there is a record for each tag an insight was tagged with ...
    Essentially ... its creating a table of interactions per insight tag ...

    :param insight_interactions_df:
    :param insights_df:
    :return:
    """
    subset_of_insights = (
        insights_df[[INSIGHT_COLS.ID, INSIGHT_COLS.INSIGHTTYPE, INSIGHT_COLS.TAGS]]
            .rename(columns={INSIGHT_COLS.ID: INTERACTIONS_COLS.INSIGHTID})
    )
    merged_interactions_with_insights = pd.merge(
            insight_interactions_df, subset_of_insights, on=INTERACTIONS_COLS.INSIGHTID, how="left"
        ).drop(
            [INTERACTIONS_COLS.PROPERTIES, INTERACTIONS_COLS.CUSTOM], 
            # ^^^ These cant be in the dict when a column is exploded since they are not hashable ...
            axis=1
        )
    return expand_tag_column(
        explode_column(merged_interactions_with_insights, INSIGHT_COLS.TAGS), INSIGHT_COLS.TAGS
    )


def craft_tag_relating_insight_to_concept(insightId:str, conceptType:str, conceptId:str, conceptTitle:str, tagInsightAssociationDate:str) -> dict:
    if not all_values_in_list_are_not_nones_or_nans([insightId, conceptType, conceptId, conceptTitle]):
        return {}
    return attr.asdict(InsightTag(
        id=unique_id(),
        context=CONTEXTS.INSIGHT_CONCEPT_TAG,
        insight=Link(
            context=CONTEXTS.INSIGHT,
            id=insightId,
            title=None
        ),
        concept=Link(
            context=conceptType,
            id=conceptId,
            title=conceptTitle
        ),
        relationship=Link(
            context=CONTEXTS.INSIGHT_TAG_RELATIONSHIP,
            id=CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP,
            title=None
        ),
        tagged=tagInsightAssociationDate
        # ^^^ Knowing when this tag was associated with the insight is helpful for debuging ...!
    ))


def filter_recent_insights(insights_df:pd.DataFrame, days_considered_recent=14) -> pd.DataFrame:
    return filter_recent_records_on_column(insights_df, INSIGHT_COLS.DATEGENERATEDUTCISO, days_considered_recent)


def filter_insights_before(insights_df:pd.DataFrame, days:int) -> pd.DataFrame:
    return filter_time_column_before(insights_df, INSIGHT_COLS.DATEGENERATEDUTCISO, {"days":-1*days})


def filter_recent_interactions(interactions_df:pd.DataFrame, days_considered_recent=14) -> pd.DataFrame:
    return filter_recent_records_on_column(interactions_df, INTERACTIONS_COLS.INTERACTIONDATEISOUTC, days_considered_recent)


def filter_interactions_before(interactions_df:pd.DataFrame, days:int) -> pd.DataFrame:
    return filter_time_column_before(interactions_df, INTERACTIONS_COLS.INTERACTIONDATEISOUTC, {"days":-1*days})
