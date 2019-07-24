from typing import List, Optional

import attr

from cortex_common.types import ProfileAttributeSchema, ProfileFacetSchema, ProfileSchema, ProfileTagSchema
from cortex_common.utils import utc_timestamp, unique_id, group_objects_by, dervie_set_by_element_id
from cortex_profiles.build.schemas.utils import attribute_building_utils as implicit_attributes
from cortex_profiles.build.schemas.builtin_templates.groups import ImplicitGroups
from cortex_profiles.build.schemas.builtin_templates.tags import ImplicitTags, ImplicitTagTemplates, ImplicitTagLabels
from cortex_profiles.build.schemas.utils.hierarchy_building_utils import derive_hierarchy_from_attribute_tags
from cortex_profiles.build.schemas.utils.schema_building_utils import prepare_schema_config_variable_names
from cortex_profiles.types.schema_config import SchemaConfig


def implicitly_generate_group_schemas(schema_config:SchemaConfig, additional_tags:Optional[List[ProfileTagSchema]]=None) -> List[ProfileFacetSchema]:
    all_groups = list(ImplicitGroups.values())
    all_tags = implicitly_generate_tag_schemas(schema_config, additional_tags)
    tags_grouped_by_group = group_objects_by(all_tags, lambda t: t.group)
    groups_grouped_by_id = group_objects_by(all_groups, lambda g: g.name)
    tag_groups = [
        attr.evolve(
            group_schemas[0],
            tags=list(sorted(map(lambda x: x.name, tags_grouped_by_group.get(group_id, []))))
        )
        for group_id, group_schemas in groups_grouped_by_id.items()
    ]
    return [x for x in tag_groups if len(x.tags) > 0]


def implicitly_generate_attribute_schemas(schema_config:SchemaConfig, disabledAttributes:Optional[List[str]]=None, include_tags:bool=True, contexts_to_cast:Optional[List[str]]=None) -> List[ProfileAttributeSchema]:
    dags = [] if disabledAttributes is None else disabledAttributes
    plc = [] if contexts_to_cast is None else contexts_to_cast
    return (
          (implicit_attributes.schemas_for_universal_attributes(include_tags=include_tags, contexts_to_cast=plc) if "universal_attributes" not in dags else [])
        + (implicit_attributes.schema_for_concept_specific_interaction_attributes(schema_config, include_tags=include_tags, contexts_to_cast=plc) if "concept_specific_interaction_attributes" not in dags else [])
        + (implicit_attributes.schema_for_concept_specific_duration_attributes(schema_config, include_tags=include_tags, contexts_to_cast=plc) if "concept_specific_duration_attributes" not in dags else [])
        + (implicit_attributes.schema_for_interaction_attributes(schema_config, include_tags=include_tags, contexts_to_cast=plc) if "interaction_attributes" not in dags else [])
        + (implicit_attributes.schema_for_app_specific_attributes(schema_config, include_tags=include_tags, contexts_to_cast=plc) if "app_specific_attributes" not in dags else [])
        + (implicit_attributes.schema_for_interaction_instances(schema_config, include_tags=include_tags, contexts_to_cast=plc) if "interaction_instances" not in dags else [])
        + (implicit_attributes.schema_for_aggregated_relationships(schema_config, include_tags=include_tags, contexts_to_cast=plc) if "aggregated_relationships" not in dags else [])
        + (implicit_attributes.schema_for_aggregated_timed_relationships(schema_config, include_tags=include_tags, contexts_to_cast=plc) if "aggregated_timed_relationships" not in dags else [])
    )


def implicitly_generate_tag_schemas(schema_config:SchemaConfig, additional_tags:Optional[List[ProfileTagSchema]]=None) -> List[ProfileTagSchema]:
    additional_tags = additional_tags if additional_tags is None else []
    tags = [
        ImplicitTags.DECLARED,
        ImplicitTags.OBSERVED,
        ImplicitTags.INFERRED,
        ImplicitTags.ASSIGNED,
        ImplicitTags.INSIGHT_INTERACTIONS,
        ImplicitTags.APP_SPECIFIC,
        ImplicitTags.APP_INTERACTION,
        ImplicitTags.CONCEPT_SPECIFIC,
        ImplicitTags.CONCEPT_AGNOSTIC,
        ImplicitTags.APP_USAGE,
        ImplicitTags.GENERAL
    ]

    used_labels = list(ImplicitTagLabels.values())

    interactions = list(map(
        lambda interaction: prepare_schema_config_variable_names({attr.fields(SchemaConfig).interaction_types.name: interaction}),
        list(dervie_set_by_element_id(schema_config.interaction_types + schema_config.timed_interaction_types, lambda x: x.id))
    ))

    for interaction in interactions:
        new_tag = ImplicitTagTemplates.INTERACTION(interaction, used_labels)
        used_labels.append(new_tag.label)
        tags.append(new_tag)

    apps = list(map(
        lambda app: prepare_schema_config_variable_names({attr.fields(SchemaConfig).apps.name: app}),
        schema_config.apps
    ))

    for app in apps:
        new_tag = ImplicitTagTemplates.APP_ASSOCIATED(app, used_labels)
        used_labels.append(new_tag.label)
        tags.append(new_tag)

    algos = list(map(
        lambda algo: prepare_schema_config_variable_names({attr.fields(SchemaConfig).insight_types.name: algo}),
        schema_config.insight_types
    ))

    for algo in algos:
        new_tag = ImplicitTagTemplates.ALGO_ASSOCIATED(algo, used_labels)
        used_labels.append(new_tag.label)
        tags.append(new_tag)

    concepts = list(map(
        lambda concept: prepare_schema_config_variable_names({attr.fields(SchemaConfig).concepts.name: concept}),
        schema_config.concepts
    ))

    for concept in concepts:
        new_tag = ImplicitTagTemplates.CONCEPT_ASSOCIATED(concept, used_labels)
        used_labels.append(new_tag.label)
        tags.append(new_tag)

    return tags + additional_tags


def implicity_generate_tag_oriented_profile_schema_from_config(
        schema_config:SchemaConfig,
        disabledAttributes:Optional[List[str]]=None,
        additional_tags:Optional[List[ProfileTagSchema]]=None,
        contexts_to_cast:Optional[List[str]]=None,
        include_attributes:bool=True,
        additional_schema_init_args:dict={},
    ) -> ProfileSchema:
    additional_tags = additional_tags if additional_tags is not None else []
    return ProfileSchema(
        id=unique_id(),
        createdAt=utc_timestamp(),
        attributes=implicitly_generate_attribute_schemas(
            schema_config,
            disabledAttributes=disabledAttributes,
            include_tags=True,
            contexts_to_cast=contexts_to_cast
        ) if include_attributes else [],
        attributeTags=implicitly_generate_tag_schemas(schema_config, additional_tags),
        facets=implicitly_generate_group_schemas(schema_config, additional_tags),
        **additional_schema_init_args
    )


class ProfileSchemaBuilder(object):


    def __init__(self, name:str=None, title:Optional[str]=None, description:Optional[str]=None, schemaId:Optional[str]=None):
        self._schema: ProfileSchema = ProfileSchema(
            name=name,
            title=title if title is not None else name,
            description=description if title is not None else name,
        )
        if schemaId is not None:
            self._schema = attr.evolve(self._schema, id=schemaId)

    def craft_schema_init_args(self):
        return {
            "name": self._schema.name,
            "title": self._schema.title,
            "description": self._schema.description,
        }

    def append_hierarchical_schema_from_config(self, schema_confg:SchemaConfig, disabledAttributes:Optional[List[str]]=None):
        self._schema:ProfileSchema = attr.evolve(
            self._schema,
            taxonomy=derive_hierarchy_from_attribute_tags(
                schema_confg,
                implicity_generate_tag_oriented_profile_schema_from_config(
                    schema_confg, disabledAttributes=disabledAttributes, include_attributes=False,
                    additional_schema_init_args=self.craft_schema_init_args()
                )
            )
        )
        return self

    def append_tag_oriented_schema_from_config(self, schema_confg:SchemaConfig, disabledAttributes:Optional[List[str]]=None, additional_tags:Optional[List[ProfileTagSchema]]=None, contexts_to_cast:Optional[List[str]]=None) :
        self._schema:ProfileSchema = self._schema + (
            implicity_generate_tag_oriented_profile_schema_from_config(
                schema_confg, disabledAttributes=disabledAttributes, additional_tags=additional_tags, contexts_to_cast=contexts_to_cast,
                additional_schema_init_args=self.craft_schema_init_args()
            )
        )
        return self

    # TODO ... modify this to recreate the facets ... since there are new tags now ...
    def append_tags(self, attributeTags:List[ProfileTagSchema]):
        self._schema = attr.evolve(self._schema, attributeTags=(self._schema.attributeTags + attributeTags))
        return self

    def append_facets(self, facets: List[ProfileFacetSchema]):
        # ... need to merge the tags in each group!
        self._schema = attr.evolve(self._schema, facets=(self._schema.facets + facets))
        return self

    def append_attributes(self, attributes: List[ProfileAttributeSchema]):
        self._schema = attr.evolve(self._schema, attributes=(self._schema.attributes + attributes))
        return self

    def get_schema(self) -> ProfileSchema:
        return self._schema


# def implicity_generate_heirarchical_profile_schema_from_config(schema_config:SchemaConfig, tenantId, environmentId) -> ProfileSchema:
#     return ProfileSchema(
#         id=unique_id(),
#         tenantId=tenantId,
#         environmentId=environmentId,
#         createdAt=utc_timestamp(),
#         attributes=implicitly_generate_attribute_schemas(schema_config, include_tags=False),
#         hierarchy=derive_hierarchy_from_attribute_tags(schema_config)
#     )
#