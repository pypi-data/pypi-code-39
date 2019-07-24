from typing import cast

import arrow

from cortex_common.types import EntityEvent, DeclaredProfileAttribute, ProfileAttributeType, EntityAttributeValue
from cortex_common.utils import construct_attr_class_from_dict, utc_timestamp


__all__ = [
    "turn_attribute_into_entity_event",
    "turn_entity_event_into_attribute",
]

def turn_attribute_into_entity_event(attribute: ProfileAttributeType) -> EntityEvent:
    """
    Transforms an attribute into an entity event.
        If type(attribute) == ProfileAttribute[EntityAttributeValue] then the Entity Event captured
            within the attribute is used as is ...
        Otherwise ... the attribute is converted into an entity event where ...
            - The attributeKey is used as the event
            - The time of the attributeCreation is used as the eventTime ...
            - The attributeValue is used as the properties as is ...
    :param attribute:
    :return:
    """
    if isinstance(attribute.attributeValue, EntityAttributeValue):
        return attribute.attributeValue.value
    else:
        return EntityEvent(  # type: ignore
            event=attribute.attributeKey,
            entityId=attribute.profileId,
            entityType=attribute.profileSchema,
            eventTime=attribute.createdAt,
            properties=dict(attribute.attributeValue)
        )


def turn_entity_event_into_attribute(
        entityEvent: EntityEvent, attributeType: type = DeclaredProfileAttribute,
        attributeValueType: type = EntityAttributeValue) -> ProfileAttributeType:
    """
    Transforms an attribute into an entity event.
        If type(attribute) == ProfileAttribute[EntityAttributeValue] then the Entity Event captured
            within the attribute is used as is ...
        Otherwise ... the attribute is converted into an entity event where ...
            - The attributeKey is used as the event
            - The time of the attributeCreation is used as the eventTime ...
            - The attributeValue is used as the properties as is ...
    :param attribute:
    :return:
    """
    if attributeValueType == EntityAttributeValue:
        return attributeType(
            profileId=entityEvent.entityId,
            profileSchema=entityEvent.entityType,
            attributeKey=entityEvent.event,
            attributeValue=EntityAttributeValue(value=entityEvent),
            # type:ignore # ignore until valid mypy attr support ...
            createdAt=str(arrow.get(
                cast(int, entityEvent.eventTime) / 1000)) if entityEvent.eventTime is not None else utc_timestamp(),
        )
    else:
        return attributeType(
            profileId=entityEvent.entityId,
            profileSchema=entityEvent.entityType,
            attributeKey=entityEvent.event,
            attributeValue=construct_attr_class_from_dict(attributeValueType, entityEvent.properties),
            createdAt=str(arrow.get(
                cast(int, entityEvent.eventTime) / 1000)) if entityEvent.eventTime is not None else utc_timestamp(),
        )
