from typing import Mapping, List, Optional
from uuid import uuid4

import arrow

from cortex_common.constants.contexts import CONTEXTS
from cortex_common.utils import pick_random_time_between
from cortex_profiles.synthesize import defaults
from cortex_profiles.synthesize.apps import AppProvider
from cortex_profiles.synthesize.base import BaseProviderWithDependencies
from cortex_profiles.synthesize.concepts import CortexConceptsProvider
from cortex_profiles.synthesize.tenant import TenantProvider
from cortex_profiles.types.insights import InsightTag, Link, Insight


class InsightsProvider(BaseProviderWithDependencies):

    def __init__(self, *args,
                 insight_types:Mapping[str, List[str]]=defaults.INSIGHT_TYPES_PER_APP,
                 concept_limits_per_insight:Optional[Mapping[str, Mapping[str, int]]]=defaults.LIMITS_ON_COUNTS_CONCEPTS_OF_TYPE_PER_CONCEPT_SET,
                 **kwargs):
        super(InsightsProvider, self).__init__(*args, **kwargs)
        self.insight_types = insight_types
        self.concept_limits_per_insight = concept_limits_per_insight

    def dependencies(self) -> List[type]:
        return [
            CortexConceptsProvider,
            TenantProvider,
            AppProvider
        ]

    def insightId(self):
        return str(uuid4())

    def insightType(self, appId:str):
        return self.fake.random.choice(self.insightTypes(appId))

    def insightTypes(self, appId:str):
        return self.insight_types[appId.split(":")[0]]

    def tag(self, insightId:str, taggedOn:str, concept:Optional[Link]=None) -> InsightTag:
        concept = concept if concept else self.fake.concept()
        return InsightTag(
            id=str(uuid4()),
            insight=Link(
                id=insightId,
                context=CONTEXTS.INSIGHT
            ),
            tagged=taggedOn,
            concept=concept,
            relationship=Link(
                id=CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP,
                context=CONTEXTS.INSIGHT_TAG_RELATIONSHIP,
            )
        )

    def tags(self, insightId:str, taggedOn:str, tagged_concepts:Optional[List[Link]]=None) -> List[InsightTag]:
        tagged_concepts = tagged_concepts if tagged_concepts is not None else [None]*10
        return [self.tag(insightId, taggedOn, concept=tagged_concept) for tagged_concept in tagged_concepts]

    def concepts_relevant_to_insight(self) -> List[Link]:
        return list(self.fake.set_of_concepts(self.concept_limits_per_insight))

    def insight(self, profileId) -> Insight:
        insightId = self.insightId()
        appId = self.fake.appId()
        dateGenerated = str(pick_random_time_between(self.fake, arrow.utcnow().shift(days=-30), arrow.utcnow()))
        return Insight(
            id=insightId,
            tags=self.tags(insightId, dateGenerated, tagged_concepts=self.concepts_relevant_to_insight()),
            insightType=self.insightType(appId=appId),
            profileId=profileId,
            dateGeneratedUTCISO=dateGenerated,
            appId=appId
        )

    def insights(self, profileId:str=None, min_insights:int=50, max_insights:int=250) -> List[Insight]:
        profileId = profileId if profileId else self.fake.profileId()
        return [
            self.insight(profileId=profileId)
            for x in range(0, self.fake.random.randint(min_insights, max_insights))
        ]

