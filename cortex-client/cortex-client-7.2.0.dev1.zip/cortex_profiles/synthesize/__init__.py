from typing import List, Optional, Any, Mapping
from faker import Factory, Generator

from cortex_profiles.synthesize.apps import AppProvider
from cortex_profiles.synthesize.attribute_values import AttributeValueProvider
from cortex_profiles.synthesize.attributes import AttributeProvider
from cortex_profiles.synthesize.concepts import CortexConceptsProvider
from cortex_profiles.synthesize.tenant import TenantProvider
from cortex_profiles.synthesize.insights import InsightsProvider
from cortex_profiles.synthesize.interactions import InteractionsProvider
from cortex_profiles.synthesize.profiles import ProfileProvider
from cortex_profiles.synthesize.sessions import SessionsProvider
from cortex_profiles.synthesize.schema import SchemaProvider


def add_provider_with_args(fake:Generator, provider, args):
    initialized_provider = provider(fake, **args)
    fake.add_provider(initialized_provider)
    return fake


def add_provider_with_subset_of_args(fake:Generator, provider, args_to_consider:List[str], all_args:Mapping[str, Any]):
    args = {arg: all_args[arg] for arg in args_to_consider if arg in all_args}
    return add_provider_with_args(fake, provider, args)


def add_profile_providers(fake:Generator, all_provider_args) -> None:
    """
    # How do mark the order as mattering with the providers ... or at least that providers depend on each other ...!?
        # Order doesnt matter, but before a method is called , all dependent providers must be in scope!

    :param fake:
    :return:
    """

    add_provider_with_subset_of_args(fake, TenantProvider, ["profile_universe", "tenant_universe"], all_provider_args)
    add_provider_with_subset_of_args(fake, CortexConceptsProvider, ["concept_universe"], all_provider_args)
    add_provider_with_subset_of_args(fake, AppProvider, ["app_universe"], all_provider_args)
    add_provider_with_subset_of_args(fake, InsightsProvider, ["insight_types", "concept_limits_per_insight"], all_provider_args)
    add_provider_with_subset_of_args(fake, InteractionsProvider, ["interactions"], all_provider_args)

    fake.add_provider(SessionsProvider)
    fake.add_provider(AttributeValueProvider)
    fake.add_provider(AttributeProvider)
    fake.add_provider(ProfileProvider)
    fake.add_provider(SchemaProvider)

    return fake


def create_profile_synthesizer(**kwargs):
    profile_synthesizer = Factory.create()
    profile_synthesizer = add_profile_providers(profile_synthesizer, kwargs)
    return profile_synthesizer


# TODO ... make insights.tags get a set of concepts ...
# TODO ... make concept_limits_on_insights work ...

if __name__ == "__main__":

    synth = create_profile_synthesizer(
        profile_universe=[str(x) for x in range(0, 9)],
        tenant_universe=["cogscalelabs"],
        concept_universe=[
            {
                "context": "cortex/person",
                "id": "Bill Gates",
                "title": "cortex/person"
            },
            {
                "context": "cortex/person",
                "id": "Steve Jobs",
                "title": "cortex/person"
            },
            {
                "context": "cortex/person",
                "id": "Elon Musk",
                "title": "cortex/person"
            },
            {
                "context": "cortex/company",
                "id": "Apple Inc",
                "title": "cortex/company"
            },
            {
                "context": "cortex/company",
                "id": "Microsoft",
                "title": "cortex/company"
            },
            {
                "context": "cortex/company",
                "id": "Google Inc",
                "title": "cortex/company"
            },
            {
                "context": "cortex/company",
                "id": "Tesla Inc",
                "title": "cortex/company"
            }
        ],
        concept_limits_per_insight={
            "cortex/person": {
                "min": 1,
                "max": 3
            },
            "cortex/company": {
                "min": 1,
                "max": 1
            }
        },
        app_universe=["FNI"],
        insight_types={
            "FNI": [
                "NewsRecommendation"
            ]
        },
        interactions=[
            {
                "interaction": "presented",
                "durationOrientedInteraction": False,
                "subsetOf": [],
                "mutuallyExlusiveOf": []
            },
            {
                "interaction": "viewed",
                "durationOrientedInteraction": True,
                "subsetOf": [("presented", 10, 25)],
                "mutuallyExlusiveOf": []
            },
            {
                "interaction": "liked",
                "durationOrientedInteraction": False,
                "subsetOf": [("viewed", 10, 50)],
                "mutuallyExlusiveOf": ["disliked"]
            },
            {
                "interaction": "disliked",
                "durationOrientedInteraction": False,
                "subsetOf": [("viewed", 10, 35)],
                "mutuallyExlusiveOf": ["liked"]
            }
        ]
    )

    import os
    import json
    import attr
    with open(os.path.expanduser("~/Desktop/old-attributes.json"), "w") as fh:
        attributes = [
            attr.asdict(a) for x in range(0, 3) for a in synth.attributes_for_single_profile(str(x))
        ]
        json.dump(attributes, fh, indent=4)
        # for attribute in attributes:
        #     fh.write(json.dumps(attribute))
        #     fh.write("\n")

    with open(os.path.expanduser("~/Desktop/old-schema.json"), "w") as fh:
        json.dump(synth.profile_schema().dict(), fh, indent=4)

