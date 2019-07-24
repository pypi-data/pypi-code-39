from typing import List, Optional

from attr import attrs

from cortex_common.constants.contexts import CONTEXTS
from cortex_common.constants.types import VERSION, DESCRIPTIONS
from cortex_common.utils.object_utils import unique_id
from cortex_common.utils.time_utils import utc_timestamp
from cortex_common.utils.attr_utils import describableAttrib

__all__ = [
    "Link",
    "InsightTag",
    "Insight",
    "InsightRelatedToConceptTag",
]


@attrs(frozen=True)
class Link(object):

    """
    Linking to a specific concept by id.
    """
    id = describableAttrib(type=str, description=DESCRIPTIONS.ID)
    title = describableAttrib(type=Optional[str], default=None, description="What is the human friendly name of this link?")
    context = describableAttrib(type=str, default=CONTEXTS.LINK, description=DESCRIPTIONS.CONTEXT, internal=True)
    version = describableAttrib(type=str, default=VERSION, description=DESCRIPTIONS.VERSION, internal=True)


@attrs(frozen=True)
class InsightTag(object):
    """
    Tags that can occur on insights.
    """
    id = describableAttrib(type=str, description=DESCRIPTIONS.ID)
    insight = describableAttrib(type=Link, description="What insight is this tag about?")
    tagged = describableAttrib(type=str, description="When was the insight tagged with this tag?")
    concept = describableAttrib(type=Link, description="What concept is being tagged by the insight?")
    relationship = describableAttrib(type=Link, description="What relationship does the tagged concept have with regards to the insight?")
    context = describableAttrib(type=str, default=CONTEXTS.INSIGHT_CONCEPT_TAG, description=DESCRIPTIONS.CONTEXT, internal=True)
    version = describableAttrib(type=str, default=VERSION, description=DESCRIPTIONS.VERSION, internal=True)


@attrs(frozen=True)
class Insight(object):
    """
    A piece of information generated for a specific profile.
    """
    id = describableAttrib(type=str, description=DESCRIPTIONS.ID)
    insightType = describableAttrib(type=str, description="What kind of insight is this?")
    profileId = describableAttrib(type=str, description="What profile was this insight generated for?")
    dateGeneratedUTCISO = describableAttrib(type=str, description="When was this insight generated?")
    appId = describableAttrib(type=str, description="Which app was this insight generated for?")
    tags = describableAttrib(type=List[InsightTag], factory=list, description="What concepts were tagged in this insight?")
    body = describableAttrib(type=Optional[dict], factory=dict, description="What is the main content captured within the insight?")
    context = describableAttrib(type=str, default=CONTEXTS.INSIGHT, description=DESCRIPTIONS.CONTEXT, internal=True)
    version = describableAttrib(type=str, default=VERSION, description=DESCRIPTIONS.VERSION, internal=True)


@attrs(frozen=True)
class InsightRelatedToConceptTag(InsightTag):
    """
    Tag relating an insight to another concept.
    """
    insightId = describableAttrib(type=str, factory=unique_id, description="What insight is this tag related to?")
    insight = describableAttrib(type=str, description="What insight is this tag related to?")
    id = describableAttrib(type=str, factory=unique_id, description=DESCRIPTIONS.ID)
    tagged = describableAttrib(type=str, factory=utc_timestamp, description="When was the insight tagged with this tag?")
    relationship = describableAttrib(
        type=Link,
        default=Link(id=CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP, context=CONTEXTS.INSIGHT_TAG_RELATIONSHIP),
        description="What relationship does the tagged concept have with regards to the insight?"
    )
    @insight.default
    def from_insight_id(self):
        return Link(
            id=self.insightId,
            context=CONTEXTS.INSIGHT,
            version=VERSION
        )

