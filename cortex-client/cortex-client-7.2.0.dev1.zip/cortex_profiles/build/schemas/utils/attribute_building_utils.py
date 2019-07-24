from typing import List, Optional, Union

import attr

from cortex_common.constants.contexts import ATTRIBUTES
from cortex_common.types import ListAttributeValue, StatisticalSummaryAttributeValue, ProfileLink, \
    ProfileValueTypeSummary, ProfileAttributeSchema, DimensionalAttributeValue, TotalAttributeValue, \
    EntityAttributeValue
from cortex_profiles.build.schemas.builtin_templates.attributes import Patterns, NameTemplates, TitleTemplates, \
    DescriptionTemplates, QuestionTemplates
from cortex_profiles.build.schemas.builtin_templates.tags import ImplicitTags
from cortex_profiles.build.schemas.builtin_templates.vocabulary import CONCEPT, attr_template
from cortex_profiles.build.schemas.utils.schema_building_utils import prepare_template_candidates_from_schema_fields
from cortex_profiles.datamodel.constants import UNIVERSAL_ATTRIBUTES
from cortex_profiles.types.schema_config import SchemaConfig, CONCEPT_SPECIFIC_INTERACTION_FIELDS, \
    CONCEPT_SPECIFIC_DURATION_FIELDS, APP_SPECIFIC_FIELDS, INTERACTION_FIELDS, APP_INTERACTION_FIELDS, \
    TIMED_APP_INTERACTION_FIELDS
from .tag_building_utils import expand_tags_for_profile_attribute


def all_attribute_names_for_candidates(pattern: Patterns, candidates: list) -> List[str]:
    return [
        NameTemplates[pattern.name].format(**{k: v.id for k, v in cand.items()})
        for cand in candidates
    ]


def optionally_cast_to_profile_link(context:str, contexts_to_cast:Optional[List[str]]=None) -> Union[str, type]:
    plc = [] if contexts_to_cast is None else contexts_to_cast
    return context if context not in plc else ProfileLink


def expand_profile_attribute_schema(
            attribute_pattern: Patterns,
            attribute_filers:dict,
            valueType:ProfileValueTypeSummary,
            custom_subject:str=None,
            attributeContext:str=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags:bool=True,
            additional_tags:Optional[List[str]]=None
        ) -> ProfileAttributeSchema:
    tags_to_add = additional_tags if additional_tags is not None else []
    return ProfileAttributeSchema(
        name=NameTemplates[attribute_pattern.name].format(**{k: v.id for k, v in attribute_filers.items()}),
        type=attributeContext,
        valueType=valueType,
        label=TitleTemplates[attribute_pattern.name].format(**attribute_filers),
        description=DescriptionTemplates[attribute_pattern.name].format(**attribute_filers),
        questions=[QuestionTemplates[attribute_pattern.name].format(**attribute_filers)],
        tags=list(sorted((expand_tags_for_profile_attribute(attribute_filers, attributeContext, custom_subject) + tags_to_add) if include_tags else []))
    )


def schema_for_interaction_instances(schema_config:SchemaConfig, include_tags:bool=True, contexts_to_cast:Optional[List[str]]=None) -> List[ProfileAttributeSchema]:
    return [
        expand_profile_attribute_schema(
            Patterns.ENTITY_INTERACTION_INSTANCE, {},
            EntityAttributeValue.detailed_schema_type(),
            custom_subject=None,
            attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags=include_tags,
            additional_tags=[ImplicitTags.APP_INTERACTION.name]
        )
    ]


def schema_for_aggregated_relationships(schema_config:SchemaConfig, include_tags:bool=True, contexts_to_cast:Optional[List[str]]=None) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, APP_INTERACTION_FIELDS)
    return (
        [
            expand_profile_attribute_schema(
                Patterns.TOTAL_ENTITY_RELATIONSHIPS, cand,
                TotalAttributeValue.detailed_schema_type(),
                custom_subject=None,
                attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_SPECIFIC.name, ImplicitTags.APP_INTERACTION.name]
            )
            for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                Patterns.TALLY_ENTITY_RELATIONSHIPS, cand,
                DimensionalAttributeValue.detailed_schema_type(
                    optionally_cast_to_profile_link(attr_template("{{{relationship_type}}}").format(**cand), contexts_to_cast),
                    TotalAttributeValue
                ),
                custom_subject=None,
                attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_SPECIFIC.name, ImplicitTags.APP_INTERACTION.name]
            )
            for cand in candidates
        ]
    )


def schema_for_aggregated_timed_relationships(schema_config:SchemaConfig, include_tags:bool=True, contexts_to_cast:Optional[List[str]]=None) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, TIMED_APP_INTERACTION_FIELDS)
    return (
        [
            expand_profile_attribute_schema(
                Patterns.TOTAL_DURATION_ON_ENTITY_INTERACTION, cand,
                DimensionalAttributeValue.detailed_schema_type(
                    optionally_cast_to_profile_link(attr_template("{{{relationship_type}}}").format(**cand), contexts_to_cast),
                    TotalAttributeValue
                ),
                custom_subject=None,
                attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_SPECIFIC.name, ImplicitTags.APP_INTERACTION.name]
            )
            for cand in candidates
        ]
        +
        schema_for_aggregated_relationships(
            attr.evolve(schema_config, timed_application_events=[], application_events=schema_config.timed_application_events),
            include_tags=include_tags, contexts_to_cast=contexts_to_cast
        )
    )


def schema_for_concept_specific_interaction_attributes(schema_config:SchemaConfig, include_tags:bool=True, contexts_to_cast:Optional[List[str]]=None) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, CONCEPT_SPECIFIC_INTERACTION_FIELDS)
    return [
        expand_profile_attribute_schema(
            Patterns.COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS, cand,
            DimensionalAttributeValue.detailed_schema_type(
                optionally_cast_to_profile_link(cand[CONCEPT].id, contexts_to_cast),
                TotalAttributeValue
            ),
            custom_subject=None,
            attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags=include_tags,
            additional_tags=[],
        )
        for cand in candidates
    ]


def schema_for_concept_specific_duration_attributes(schema_config: SchemaConfig, include_tags:bool=True, contexts_to_cast:Optional[List[str]]=None) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, CONCEPT_SPECIFIC_DURATION_FIELDS)
    return [
        expand_profile_attribute_schema(
            Patterns.TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT, cand,
            DimensionalAttributeValue.detailed_schema_type(
                optionally_cast_to_profile_link(cand[CONCEPT].id, contexts_to_cast),
                TotalAttributeValue
            ),
            custom_subject=None,
            attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags=include_tags,
            additional_tags=[],
        )
        for cand in candidates
    ]


def schema_for_interaction_attributes(schema_config: SchemaConfig, include_tags:bool=True, contexts_to_cast:Optional[List[str]]=None) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, INTERACTION_FIELDS)
    return [
        expand_profile_attribute_schema(
            Patterns.COUNT_OF_INSIGHT_INTERACTIONS, cand,
            TotalAttributeValue.detailed_schema_type(),
            custom_subject=None,
            attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags=include_tags,
            additional_tags=[],
        )
        for cand in candidates
    ]


def schema_for_app_specific_attributes(schema_config:SchemaConfig, include_tags:bool=True, contexts_to_cast:Optional[List[str]]=None) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, APP_SPECIFIC_FIELDS)
    return (
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                TotalAttributeValue.detailed_schema_type(),
                custom_subject=None,
                attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.name,]
            )
            for attribute_pattern in [Patterns.COUNT_OF_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                DimensionalAttributeValue.detailed_schema_type(
                    optionally_cast_to_profile_link("cortex/day", contexts_to_cast),
                    TotalAttributeValue
                ),
                custom_subject=None,
                attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.name,]
            )
            for attribute_pattern in [Patterns.COUNT_OF_DAILY_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                TotalAttributeValue.detailed_schema_type(),
                custom_subject=None,
                attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.name,]
            )
            for attribute_pattern in [Patterns.TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                DimensionalAttributeValue.detailed_schema_type(
                    optionally_cast_to_profile_link("cortex/day", contexts_to_cast),
                    TotalAttributeValue
                ),
                custom_subject=None,
                attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.name,]
            )
            for attribute_pattern in [Patterns.TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                StatisticalSummaryAttributeValue.detailed_schema_type(),
                custom_subject=None,
                attributeContext=ATTRIBUTES.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.name,]
            )
            for attribute_pattern in [Patterns.STAT_SUMMARY_DAILY_APP_SPECIFIC_LOGINS, Patterns.STAT_SUMMARY_DAILY_APP_SPECIFIC_DURATIONS] for cand in candidates
        ]
    )


def schemas_for_universal_attributes(include_tags:bool=True, contexts_to_cast:Optional[List[str]]=None) -> List[ProfileAttributeSchema]:
    return [
        ProfileAttributeSchema(
            name=UNIVERSAL_ATTRIBUTES.TYPES,
            type=ATTRIBUTES.ASSIGNED_PROFILE_ATTRIBUTE,
            valueType=ListAttributeValue.detailed_schema_type("str"),
            label=TitleTemplates.TYPE,
            description=DescriptionTemplates.TYPE,
            questions=[QuestionTemplates.TYPE],
            tags=[ImplicitTags.ASSIGNED.name, ImplicitTags.GENERAL.name] if include_tags else []
        )
    ]
