from typing import List

import attr

from cortex_common.utils.attr_utils import dicts_to_classes, dict_to_attr_class
from .vocabulary import Subject, Verb


__all__ = [
    "RelationshipConfig",
    "SchemaConfig",
    "CONCEPT_SPECIFIC_INTERACTION_FIELDS",
    "CONCEPT_SPECIFIC_DURATION_FIELDS",
    "INTERACTION_FIELDS",
    "APP_SPECIFIC_FIELDS",
    "APP_INTERACTION_FIELDS",
    "TIMED_APP_INTERACTION_FIELDS",
]


@attr.s(frozen=True)
class RelationshipConfig(object):
    relationship = attr.ib(type=Verb, converter=lambda x: dict_to_attr_class(x, Verb))
    relatedType = attr.ib(type=Subject, converter=lambda x: dict_to_attr_class(x, Subject))


@attr.s(frozen=True)
class SchemaConfig(object):
    apps = attr.ib(type=List[Subject], converter=lambda l: dicts_to_classes(l, Subject))
    insight_types = attr.ib(type=List[Subject], converter=lambda l: dicts_to_classes(l, Subject))
    concepts = attr.ib(type=List[Subject], converter=lambda l: dicts_to_classes(l, Subject))
    interaction_types = attr.ib(type=List[Verb], converter=lambda l: dicts_to_classes(l, Verb))
    timed_interaction_types = attr.ib(type=List[Verb], converter=lambda l: dicts_to_classes(l, Verb))
    application_events = attr.ib(type=List[RelationshipConfig], converter=lambda l: dicts_to_classes(l, RelationshipConfig), factory=list)
    timed_application_events = attr.ib(type=List[RelationshipConfig], converter=lambda l: dicts_to_classes(l, RelationshipConfig), factory=list)


CONCEPT_SPECIFIC_INTERACTION_FIELDS = [attr.fields(SchemaConfig).insight_types, attr.fields(SchemaConfig).concepts, attr.fields(SchemaConfig).interaction_types]
CONCEPT_SPECIFIC_DURATION_FIELDS = [attr.fields(SchemaConfig).insight_types, attr.fields(SchemaConfig).concepts, attr.fields(SchemaConfig).timed_interaction_types]
INTERACTION_FIELDS = [attr.fields(SchemaConfig).insight_types, attr.fields(SchemaConfig).interaction_types, attr.fields(SchemaConfig).apps]
# Should interactions be app specific???
APP_SPECIFIC_FIELDS = [attr.fields(SchemaConfig).apps]
APP_INTERACTION_FIELDS = [attr.fields(SchemaConfig).apps, attr.fields(SchemaConfig).application_events]
TIMED_APP_INTERACTION_FIELDS = [attr.fields(SchemaConfig).apps, attr.fields(SchemaConfig).timed_application_events]
