from typing import Any

from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.training_data import Message

__all__ = ['NegatedEntityMapper']


class NegatedEntityMapper(EntityExtractor):
    name = 'NegatedEntityMapper'
    requires = ['entities']
    provides = ['entities']

    def process(self, message: Message, **kwargs: Any) -> None:
        entities = message.data.get('entities')
        if not entities:
            return

        last_negation = None
        new_entities = []

        for entity in entities:
            if entity['entity'] == 'negation':
                last_negation = entity
                continue

            if last_negation:
                if entity['start'] - last_negation['end'] <= 1:
                    entity['is_negated'] = True

            entity.setdefault('is_negated', False)
            self.add_processor_name(entity)
            new_entities.append(entity)

        message.set('entities', new_entities, add_to_output=True)
