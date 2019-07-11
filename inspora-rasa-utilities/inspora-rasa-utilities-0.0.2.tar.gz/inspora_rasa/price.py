import re
from typing import Any

from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.training_data import Message

__all__ = ['PriceEntityMapper']


class PriceEntityMapper(EntityExtractor):
    name = 'PriceEntityMapper'
    requires = ['entities']
    provides = ['entities']

    def process(self, message: Message, **kwargs: Any) -> None:
        entities = message.data.get('entities', [])[:]
        if not entities:
            return

        for entity in entities:
            if entity['entity'] == 'price':
                value = str(entity['value'])

                # price entity includes currency, e.g. "123 euro"
                price_number = re.findall(r'([0-9]+([.,][0-9]{2})?)', value)
                if price_number:
                    price = float(price_number[0][0].replace(',', '.'))
                    entity['value'] = price
                    self.add_processor_name(entity)

            if entity['entity'] == 'price-modifier':
                if entity.get('is_negated'):
                    self.add_processor_name(entity)
                    if entity['value'] == 'gt':
                        entity['value'] = 'lt'
                        entity['is_negated'] = False
                    elif entity['value'] == 'lt':
                        entity['value'] = 'gt'
                        entity['is_negated'] = False

        message.set('entities', entities, add_to_output=True)
