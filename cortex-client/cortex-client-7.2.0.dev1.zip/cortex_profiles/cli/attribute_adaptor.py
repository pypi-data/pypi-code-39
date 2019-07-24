import json
import pydash


def upgrade_old_attributes_into_new_ones(attributes, schema="cortex/end-user:1"):
    keysToRemove = ["tenantId", "environmentId", "onLatestProfile", "commits", "attributeValue.summary"]
    upgraded_attributes = list(map(
        lambda x: pydash.set_(
            pydash.set_(
                pydash.omit(x, *keysToRemove),
                "profileSchema",
                schema
            ),
            "profileId",
            "{}".format(x["profileId"])
        ),
        attributes if isinstance(attributes, list) else [attributes]
    ))
    return upgraded_attributes if isinstance(attributes, list) else upgraded_attributes[0]


if __name__ == '__main__':

    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--profile-schema', action='store', default="cortex/end-user:1")
    parser.add_argument('-s', '-i', '--old-attributes', '--old-attributes-file', action='store', required=True)
    parser.add_argument('-o', '--output-file', '--new-attributes', action='store', required=True)
    args = parser.parse_args()

    old_attrs = args.old_attributes
    new_attrs = args.output_file
    profile_schema = args.profile_schema

    with open(new_attrs, "w") as fhw:
        with open(old_attrs, "r") as fhr:
            attributes = json.load(fhr)
        json.dump(upgrade_old_attributes_into_new_ones(attributes, schema=profile_schema), fhw, indent=4)
