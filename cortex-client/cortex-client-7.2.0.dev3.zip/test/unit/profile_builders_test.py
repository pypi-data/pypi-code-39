import json
import unittest

import attr
import pandas as pd

from cortex_profiles.build.attributes.declared import DeclaredAttributesBuilder
from cortex_profiles.build.schemas.builders import ProfileSchemaBuilder
from cortex_profiles.cli.schema_builder import build_custom_schema
from cortex_profiles.types import SchemaConfig


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.schema_config = SchemaConfig(**{
            "apps": [
                {"id": "insights-app-1", "singular": "IA1", "acronym": "IA1"}
            ],
            "insight_types": [
                {"id": "type-1-insight", "singular": "Type 1 Insight", "plural": "Type 1 Insights", "acronym": "T1I"},
                {"id": "type-2-insight", "singular": "Type 2 Insight", "plural": "Type 2 Insights", "acronym": "T2I"}
            ],
            "concepts": [
                {"id": "cortex/company", "singular": "company", "plural": "companies"},
                {"id": "cortex/sector", "singular": "sector", "plural": "sectors"},
                {"id": "cortex/market_index", "singular": "market index", "plural": "market indices"},
                {"id": "cortex/country", "singular": "country", "plural": "countries"},
                {"id": "cortex/market_cap_buckets", "singular": "market cap", "plural": "market caps"}
            ],
            "interaction_types": [
                {"id": "presented", "verb": "presented", "verbInitiatedBySubject": False},
                {"id": "viewed", "verb": "viewed"},
                {"id": "ignored", "verb": "ignored"},
                {"id": "liked", "verb": "liked"},
                {"id": "disliked", "verb": "disliked"}
            ],
            "timed_interaction_types": [
                {"id": "viewed", "verb": "viewed"}
            ],
            "application_events": [
                {
                    "relationship": {
                        "id": "searched", "verb": "searched", "past": "searched"
                    },
                    "relatedType": {
                        "id": "cortex/company", "singular": "company", "plural": "companies"
                    }
                }
            ]
        })
        self.schema = (
            ProfileSchemaBuilder("test/schema")
                .append_tag_oriented_schema_from_config(self.schema_config)
                .append_hierarchical_schema_from_config(self.schema_config).get_schema()
        )

    def test_01_building_schemas(self):
        """
        Tests getting schemas from a mocked endpoint ...
        :return:
        """
        print(json.dumps(attr.asdict(self.schema), indent=4))

    def test_02_building_declared_attributes(self):
        kv_df = pd.DataFrame([
           {"profileId": "p1", "key": "profile.name", "value": "Jack"},
           {"profileId": "p1", "key": "profile.age", "value": 25},
           {"profileId": "p2", "key": "profile.name", "value": "Jill"},
           {"profileId": "p2", "key": "profile.age", "value": 26},
        ])

        value_only_df = pd.DataFrame([
            {"profileId": "p3", "name": "Adam", "age": 45},
            {"profileId": "p4", "name": "Eve", "age": 46},
        ])

        attributes = (
            DeclaredAttributesBuilder()
                .append_attributes_from_kv_df(kv_df)
                .append_attributes_from_column_in_df(value_only_df, key="profile.name", value_column="name")
                .append_attributes_from_column_in_df(value_only_df, key="profile.age", value_column="age")
                .get()
        )

        print("{} total attributes generated.".format(len(attributes)))
        for attribute in attributes:
            print(attribute)

    def test_03_profile_schema_equality(self):
        from cortex_common.types import ProfileAttributeSchema, ProfileValueTypeSummary
        self.assertEqual(
            ProfileAttributeSchema(
                name="n",
                type="t",
                valueType=ProfileValueTypeSummary(outerType="t", innerTypes=[]),
                label="l",
                description="d",
                questions=["q"],
                tags=["a", "b"],
            ),
            ProfileAttributeSchema(
                name="n",
                type="t",
                valueType=ProfileValueTypeSummary(outerType="t", innerTypes=[]),
                label="l",
                description="d",
                questions=["q"],
                tags=["a", "b"],
            )
        )

    def test_04_querying_attributes_in_schema(self):
        from cortex_profiles.build.schemas.utils.attribute_query_utils import query_attributes
        from cortex_profiles.types import ProfileAttributeSchemaQuery

        def print_res(q, r):
            print("---")
            print("{} results for Query -> {}".format(len(r), attr.asdict(q, filter=lambda k, v: v is not None)))
            print(json.dumps(r, indent=4))
            print("---")

        queries = [
            ProfileAttributeSchemaQuery(all=True),
            ProfileAttributeSchemaQuery(attributesWithNames=[]),
            ProfileAttributeSchemaQuery(attributesWithAnyTags=["interaction/followed"]),
            ProfileAttributeSchemaQuery(attributesWithAnyTags=["interaction/followed", "interaction/ignored"]),
            ProfileAttributeSchemaQuery(
                inverse=ProfileAttributeSchemaQuery(attributesWithAnyTags=["interaction/followed"])),
            ProfileAttributeSchemaQuery(inverse=ProfileAttributeSchemaQuery(
                inverse=ProfileAttributeSchemaQuery(attributesWithAnyTags=["interaction/followed"]))),
            ProfileAttributeSchemaQuery(attributesInAnyGroups=["data-limits"]),
            ProfileAttributeSchemaQuery(attributesInAllGroups=["data-limits", "app-association"]),
            ProfileAttributeSchemaQuery(
                inverse=ProfileAttributeSchemaQuery(attributesInAllGroups=["data-limits", "app-association"])
            ),
        ]

        results = {
            k: list(query_attributes(v, self.schema))
            for k, v in enumerate(queries)
        }

        for k, v in results.items():
            print_res(queries[k], v)

    # @unittest.skip("skipping")
    def test_05_schema_building_tools(self):
        config = {
            "additional_fields": {
                "name": "cortex/user",
                "title": "cortex/user",
                "description": "Schema modeling the attributes for users that consume insights."
            },
            "schema_configs": [
                {
                    "fill_implicit_schema_template_with": {
                        "apps": [
                            {
                                "id": "IAI-v0",
                                "singular": "Insight AI",
                                "acronym": "IAI"
                            }
                        ],
                        "insight_types": [
                            {
                                "id": "news-insights",
                                "singular": "News Insight",
                                "plural": "News Insights",
                                "acronym": "news-insights"
                            }
                        ],
                        "concepts": [
                            {
                                "id": "cortex/company",
                                "singular": "company",
                                "plural": "companies"
                            },
                            {
                                "id": "cortex/product",
                                "singular": "product",
                                "plural": "products"
                            },
                        ],
                        "interaction_types": [
                            {
                                "id": "presented",
                                "verb": "presented",
                                "verbInitiatedBySubject": False
                            },
                            {
                                "id": "viewed",
                                "verb": "viewed"
                            },
                            {
                                "id": "ignored",
                                "verb": "ignored"
                            },
                            {
                                "id": "actedOn",
                                "verb": "actedOn"
                            },
                        ],
                        "timed_interaction_types": [
                            {
                                "id": "viewed",
                                "verb": "viewed"
                            }
                        ],
                        "application_events": [],
                        "timed_application_events": []
                    },
                    "additional_attribute_tags": [
                        {
                            "name": "subject/app-preferences",
                            "label": "SAP",
                            "description": "What attributes capture a profile's application preferences?",
                            "group": "subject",
                            "context": "cortex/profile-attribute-tag"
                        },
                        {
                            "name": "subject/insight-preferences",
                            "label": "SIP",
                            "description": "What attributes capture a profile's insight preferences?",
                            "group": "subject",
                            "context": "cortex/profile-attribute-tag"
                        }
                    ],
                    "additional_groups_of_attributes": [
                        {
                            "attributes": [
                                {
                                    "name": "appPreferences[{appId.id}].favoriteInsights",
                                    "label": "Favorite Insights",
                                    "description": "Favorite Insights in App",
                                    "question": "What are the profile's most favorite insights in the {appId.id} App?"
                                },
                            ],
                            "tags": [
                                "info/declared",
                                "subject/app-preferences",
                                "app/{appId.id}"
                            ],
                            "valueType": {
                                "outerType": "cortex/attribute-value-list",
                                "innerTypes": [
                                    {
                                        "outerType": "cortex/attribute-value-string",
                                        "innerTypes": []
                                    }
                                ]
                            }
                        },
                        {
                            "attributes": [
                                {
                                    "name": "newspaper.reading.frequency",
                                    "label": "Newspaper Addiction",
                                    "description": "Frequency Profile reads the news paper.",
                                    "question": "How often does the profile read news in the news paper?"
                                },
                            ],
                            "tags": [
                                "info/declared",
                            ],
                            "valueType": {
                                "outerType": "cortex/attribute-value-string",
                                "innerTypes": []
                            }
                        },
                        {
                            "attributes": [
                                {
                                    "name": "name",
                                    "label": "Name",
                                    "description": "Name of Profile",
                                    "question": "What is the profile's name?"
                                }
                            ],
                            "tags": [
                                "attr/declared",
                                "usage/general"
                            ],
                            "valueType": {
                                "outerType": "cortex/attribute-value-string",
                                "innerTypes": []
                            }
                        }
                    ],
                    "profile_link_contexts": [
                        "cortex/user",
                        "cortex/company",
                        "cortex/product"
                    ]
                },
                {
                    "fill_implicit_schema_template_with": {
                        "apps": [
                            {
                                "id": "IAI-v0",
                                "singular": "Insight AI",
                                "acronym": "IAI"
                            }
                        ],
                        "insight_types": [],
                        "concepts": [],
                        "interaction_types": [],
                        "timed_interaction_types": [],
                        "application_events": [
                            {
                                "relationship": {
                                    "id": "searched",
                                    "verb": "searched",
                                    "past": "searched"
                                },
                                "relatedType": {
                                    "id": "cortex/product",
                                    "singular": "product",
                                    "plural": "products"
                                }
                            },
                            {
                                "relationship": {
                                    "id": "compared",
                                    "verb": "compared",
                                    "past": "compared"
                                },
                                "relatedType": {
                                    "id": "cortex/company",
                                    "singular": "company",
                                    "plural": "companies"
                                }
                            }
                        ],
                        "timed_application_events": [
                            {
                                "relationship": {
                                    "id": "searched",
                                    "verb": "searched",
                                    "past": "searched"
                                },
                                "relatedType": {
                                    "id": "cortex/company",
                                    "singular": "company",
                                    "plural": "companies"
                                }
                            }
                        ]
                    },
                    "additional_attribute_tags": [],
                    "additional_groups_of_attributes": [],
                    "disabled_attributes": [
                        "universal_attributes",
                        "concept_specific_interaction_attributes",
                        "concept_specific_duration_attributes",
                        "interaction_attributes",
                        "app_specific_attributes",
                        "interaction_instances"
                    ],
                    "profile_link_contexts": [
                        "cortex/user",
                        "cortex/company",
                        "cortex/product"
                    ]
                }
            ]
        }
        schema = build_custom_schema(config)
        print(json.dumps(schema, indent=4))
