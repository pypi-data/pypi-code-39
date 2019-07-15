"""Class for centralizing Datastore operations"""

import logging
from typing import List

from google.cloud import datastore
from google.cloud.datastore.entity import Entity

__all__ = ("Datastore",)


_LOG_PREFIX_ = "[DATASTORE]%s"


class Datastore(object):
    """
    Class for abstracting the access of the Datastore
    """

    client: datastore.Client = None

    def __init__(self):
        """Constructor"""
        self.client = datastore.Client()

    def update_entity(
        self, kind: str, namespace: str, entity_id: int, fields_to_update: dict
    ) -> None:
        """Update an entity in Datastore"""

        # Fetch the entity
        entity = self._get_entity_by_id(kind, namespace, entity_id)

        # Update the entity
        entity.update(fields_to_update)
        self.client.put(entity)

        logging.info(
            _LOG_PREFIX_, f"[WRITE] Entity {entity_id} saved in Datastore"
        )

    def _get_entity_by_id(
        self, kind: str, namespace: str, entity_id: int
    ) -> Entity:
        """Fetch entity by id"""

        if not entity_id:
            raise ValueError("Missing the entity id")

        key = self.client.key(kind, entity_id, namespace=namespace)
        entity = self.client.get(key)

        if not entity:
            raise Exception(
                f"Entity on Datastore not found by ID: {entity_id}"
            )

        logging.info(
            _LOG_PREFIX_, f"[READ] Entity {entity_id} read from Datastore"
        )

        return entity

    def get_entity(self, kind: str, namespace: str, entity_id: int) -> dict:
        """Obtain an entity from Datastore by its id"""

        entity = self._get_entity_by_id(kind, namespace, entity_id)
        return self._entity_to_dict(entity)

    def query_entity_with_filters(
        self, kind: str, namespace: str, filter_list: List
    ) -> List[Entity]:
        """Search in Datastore using custom query"""

        logging.debug(
            _LOG_PREFIX_,
            f"[QUERY] Will query entities using the filters: {filter_list}",
        )

        query = self.client.query(kind=kind, namespace=namespace)
        for filter_item in filter_list:
            query.add_filter(filter_item[0], filter_item[1], filter_item[2])

        results = list(query.fetch())

        logging.info(
            _LOG_PREFIX_,
            f"[QUERY] Total number of entities returned: {len(results)}",
        )

        return [self._entity_to_dict(entity) for entity in results]

    @staticmethod
    def _entity_to_dict(entity: Entity) -> dict:
        """Convert from entity to dict"""

        _dict = entity.__dict__
        _dict["id"] = entity.id

        for field_name in entity.keys():
            _dict[field_name] = entity[field_name]

        return _dict
