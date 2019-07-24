from typing import List, Optional

from cortex_common.types import ProfileSchema
from cortex_common.utils import split_camel_case
from cortex_profiles.build.schemas.builders import ProfileSchemaBuilder
from cortex_profiles.datamodel.constants import DOMAIN_CONCEPTS
from cortex_profiles.synthesize.apps import AppProvider
from cortex_profiles.synthesize.base import BaseProviderWithDependencies
from cortex_profiles.synthesize.concepts import CortexConceptsProvider
from cortex_profiles.synthesize.defaults import INTERACTION_CONFIG
from cortex_profiles.synthesize.insights import InsightsProvider
from cortex_profiles.synthesize.tenant import TenantProvider
from cortex_profiles.types.schema_config import SchemaConfig


class SchemaProvider(BaseProviderWithDependencies):

    def __init__(self, *args, **kwargs):
        super(SchemaProvider, self).__init__(*args, **kwargs)

    def dependencies(self) -> List[type]:
        return [
            CortexConceptsProvider,
            TenantProvider,
            AppProvider,
            InsightsProvider
        ]

    def profile_schema(self, schemaId:Optional[str]=None, additional_attributes:Optional[List]=[], additional_tags:Optional[List]=[]) -> ProfileSchema:
        # Schema Config ... per app ...
        # Change the builder to merge multiple schema configs ...
        # CLEANUP ... make sure we dont use anything from default ... and that it is comming from the fakers ...
        #   This way if someone creates their own synthesizer ... when they call profile schema ...
        #   they get a schema according to their synthesizer ... and not something else

        implicit_schema_configs = [
            SchemaConfig(
                apps = [
                    {"id": appId, "singular": appId.split(":")[0].upper(), "acronym": appId.split(":")[0].upper()}
                ],
                insight_types = [
                    {
                        "id": insightType, "singular": " ".join(split_camel_case(insightType)),
                        "plural": "{}s".format(" ".join(split_camel_case(insightType))),
                        "acronym": "".join(map(lambda x: x[0], split_camel_case(insightType)))
                    }
                    for insightType in self.fake.insightTypes(appId)
                ],
                concepts=[
                    {"id": DOMAIN_CONCEPTS.PERSON, "singular": "person", "plural": "people"},
                    {"id": DOMAIN_CONCEPTS.COMPANY, "singular": "company", "plural": "companies"},
                    {"id": DOMAIN_CONCEPTS.COUNTRY, "singular": "country", "plural": "countries"},
                    {"id": DOMAIN_CONCEPTS.CURRENCY, "singular": "currency", "plural": "currencies"},
                    {"id": DOMAIN_CONCEPTS.WEBSITE, "singular": "website", "plural": "websites"}
                ],
                interaction_types=[
                    {"id": interaction["interaction"], "verb": interaction["interaction"], "verbInitiatedBySubject": interaction["initiatedByProfile"]}
                    for interaction in INTERACTION_CONFIG if interaction["durationOrientedInteraction"] == False
                ],
                timed_interaction_types=[
                    {"id": interaction["interaction"], "verb": interaction["interaction"], "verbInitiatedBySubject": interaction["initiatedByProfile"]}
                    for interaction in INTERACTION_CONFIG if interaction["durationOrientedInteraction"] == True
                ]
            )
            for appId in self.fake.appIds()
        ]

        schema_builder = ProfileSchemaBuilder(
            "cortex/synthetic-schema",
            schemaId=schemaId
        )
        for schema_config in implicit_schema_configs:
            schema_builder.append_tag_oriented_schema_from_config(schema_config)
            schema_builder.append_hierarchical_schema_from_config(schema_config)
        schema_builder.append_attributes(additional_attributes)
        schema_builder.append_tags(additional_tags)
        return schema_builder.get_schema()
