from typing import List

import attr

from cortex_common.types import ProfileSchema, ProfileTaxonomySchema
from cortex_profiles.build.schemas.builtin_templates.groups import ImplicitGroups
from cortex_profiles.build.schemas.builtin_templates.hierarchy import HierarchyNameTemplates, \
    HierarchyDescriptionTemplates
from cortex_profiles.build.schemas.builtin_templates.tags import ImplicitTags, ImplicitTagTemplates
from cortex_profiles.build.schemas.utils.schema_building_utils import prepare_template_candidates_from_schema_fields
from cortex_profiles.types import SchemaConfig, RecursiveProfileHierarchyGroup, ProfileAttributeSchemaQuery


def derive_hierarchy_from_attribute_tags(schema_config:SchemaConfig, schema:ProfileSchema) -> List[ProfileTaxonomySchema]:
    """
    general
    application-usage
        {app}
    insight-interactions
        concept-specific-interactions
            apps-{app}
            algos-{algo}
        concept-agnostic-interactions
            apps-{app}
            algos-{algo}

    # TODO ... implement folders above ...
    # Todo ... implement the following as declared preferences ...

    app-preferences
        {app}
    trading-preferences

    :param attributes:
    :return:
    """

    apps = prepare_template_candidates_from_schema_fields(schema_config, [attr.fields(SchemaConfig).apps])
    algos = prepare_template_candidates_from_schema_fields(schema_config, [attr.fields(SchemaConfig).insight_types])

    hierarchy = (
        RecursiveProfileHierarchyGroup(
            name=HierarchyNameTemplates.GENERAL,
            label=HierarchyNameTemplates.GENERAL,
            description=HierarchyDescriptionTemplates.GENERAL,
            includedAttributes=ProfileAttributeSchemaQuery(attributesWithAnyTags=[ImplicitTags.ASSIGNED.name]),
            tags=[ImplicitTags.ASSIGNED.name]
        ).flatten(schema)
        +
        RecursiveProfileHierarchyGroup(
            name=HierarchyNameTemplates.INSIGHT_INTERACTION,
            label=HierarchyNameTemplates.INSIGHT_INTERACTION,
            description=HierarchyDescriptionTemplates.INSIGHT_INTERACTION,
            includedAttributes=ProfileAttributeSchemaQuery(none=True),
            tags=[ImplicitTags.INSIGHT_INTERACTIONS.name]
        ).append_child(
            RecursiveProfileHierarchyGroup(
                name=HierarchyNameTemplates.CONCEPT_SPECIFIC,
                label=HierarchyNameTemplates.CONCEPT_SPECIFIC,
                description=HierarchyDescriptionTemplates.CONCEPT_SPECIFIC,
                includedAttributes=ProfileAttributeSchemaQuery(none=True),
                tags=[ImplicitTags.CONCEPT_SPECIFIC.name]
            )
            .append_children(
                [
                    RecursiveProfileHierarchyGroup(
                        name=HierarchyNameTemplates.ALGO_SPECIFIC.format(**algo),
                        label=HierarchyNameTemplates.ALGO_SPECIFIC.format(**algo),
                        description=HierarchyDescriptionTemplates.ALGO_SPECIFIC.format(**algo),
                        includedAttributes=ProfileAttributeSchemaQuery(
                            attributesWithAllTags=[ImplicitTags.INSIGHT_INTERACTIONS.name, ImplicitTagTemplates.ALGO_ASSOCIATED(algo).name],
                            attributesInAllGroups=[ImplicitGroups.CONCEPT_ASSOCIATED.name]
                        ),
                        tags=[ImplicitTagTemplates.ALGO_ASSOCIATED(algo).name]
                    )
                    for algo in algos
                ]
            )
        ).append_child(
            RecursiveProfileHierarchyGroup(
                name=HierarchyNameTemplates.CONCEPT_AGNOSTIC,
                label=HierarchyNameTemplates.CONCEPT_AGNOSTIC,
                description=HierarchyDescriptionTemplates.CONCEPT_AGNOSTIC,
                includedAttributes=ProfileAttributeSchemaQuery(none=True),
                tags=[ImplicitTags.CONCEPT_AGNOSTIC.name]
            )
            .append_children(
                [
                    RecursiveProfileHierarchyGroup(
                        name=HierarchyNameTemplates.ALGO_SPECIFIC.format(**algo),
                        label=HierarchyNameTemplates.ALGO_SPECIFIC.format(**algo),
                        description=HierarchyDescriptionTemplates.ALGO_SPECIFIC.format(**algo),
                        includedAttributes=ProfileAttributeSchemaQuery(
                            attributesWithAllTags=[ImplicitTags.INSIGHT_INTERACTIONS.name, ImplicitTagTemplates.ALGO_ASSOCIATED(algo).name],
                            inverse=ProfileAttributeSchemaQuery(attributesInAllGroups=[ImplicitGroups.CONCEPT_ASSOCIATED.name])
                        ),
                        tags=[ImplicitTagTemplates.ALGO_ASSOCIATED(algo).name]
                    )
                    for algo in algos
                ]
            )
        ).flatten(schema)
        +
        RecursiveProfileHierarchyGroup(
            name=HierarchyNameTemplates.APPLICATION_USAGE,
            label=HierarchyNameTemplates.APPLICATION_USAGE,
            description=HierarchyDescriptionTemplates.APPLICATION_USAGE,
            includedAttributes=ProfileAttributeSchemaQuery(none=True),
            tags=[ImplicitTags.APP_USAGE.name]
        ).append_children([
            RecursiveProfileHierarchyGroup(
                name=HierarchyNameTemplates.APP_SPECIFIC.format(**app),
                label=HierarchyNameTemplates.APP_SPECIFIC.format(**app),
                description=HierarchyDescriptionTemplates.APP_SPECIFIC.format(**app),
                includedAttributes=ProfileAttributeSchemaQuery(
                    attributesWithAllTags=[ImplicitTags.APP_USAGE.name, ImplicitTagTemplates.APP_ASSOCIATED(app).name]
                ),
                tags=[ImplicitTags.APP_SPECIFIC.name, ImplicitTagTemplates.APP_ASSOCIATED(app).name]
            )
            for app in apps
        ]).flatten(schema)
        +
        RecursiveProfileHierarchyGroup(
            name=HierarchyNameTemplates.MEANINGFUL_INTERACTIONS,
            label=HierarchyNameTemplates.MEANINGFUL_INTERACTIONS,
            description=HierarchyDescriptionTemplates.MEANINGFUL_INTERACTIONS,
            includedAttributes=ProfileAttributeSchemaQuery(none=True),
            tags=[ImplicitTags.APP_INTERACTION.name]
        ).flatten(schema)
    )
    return hierarchy
