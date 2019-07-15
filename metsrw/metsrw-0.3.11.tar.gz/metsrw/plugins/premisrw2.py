from __future__ import absolute_import, unicode_literals

import abc

import six


class PREMISElement(six.with_metaclass(abc.ABCMeta, object)):
    pass


PREMISObjectIdentifier = NamedTuple('type', 'value')
PREMISObjectIdentifier

class PREMISObject(PREMISElement):
            xsi_type=old_premis_object.xsi_type,
            identifier_value=old_premis_object.identifier_value,
            message_digest_algorithm=old_premis_object.message_digest_algorithm,
            message_digest=old_premis_object.message_digest,
            size=old_premis_object.size,
            format_name=old_premis_object.format_name,
            format_registry_key=old_premis_object.format_registry_key,
            creating_application_name=old_premis_object.creating_application_name,
            creating_application_version=old_premis_object.creating_application_version,
            date_created_by_application=old_premis_object.date_created_by_application,
            relationship=old_premis_object.relationship,
            # New attributes:
            inhibitors=new_inhibitors,
            composition_level=new_composition_level,
    def __init__(self, object_identifiers=):
        object_identifier="Special ID",
