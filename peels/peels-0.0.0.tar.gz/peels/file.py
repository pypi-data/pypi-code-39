from collections import OrderedDict
from typing import Any, BinaryIO, Dict, Union

from peels.conditions import Condition
from peels.convert import Converter, convert_map
from peels.stream import Consumer, ConstantConsumption, DynamicConsumption


class Segment:

    def __init__(self, label: Union[str, None], consumer: Union[Consumer, int], converter: Union[str, Converter],
                 enabled_condition: Union[Condition, None] = None):
        self.label = label
        if isinstance(consumer, int):
            self.consumer = ConstantConsumption(consumer)
        elif isinstance(consumer, str):
            self.consumer = DynamicConsumption(consumer)
        else:
            self.consumer = consumer
        self.converter = convert_map[converter] if isinstance(converter, str) else converter
        self.enabled_condition = enabled_condition

    def consume(self, ctx: Dict[str, Any], stream: BinaryIO):
        data = self.consumer.read(ctx, self.label, stream)
        return self.converter.load(data)

    def digest(self, ctx: Dict[str, bytes], values: Dict[str, Any]):
        data = self.converter.dump(values[self.label], self.consumer.length(ctx, self.label, values))
        return self.consumer.write(ctx, self.label, data, values)


class Peel:

    def __init__(self, *segments):
        self.segments = segments

    def parse_stream(self, stream: BinaryIO) -> OrderedDict:
        ctx = OrderedDict()
        for segment in self.segments:
            if not segment.enabled_condition or segment.enabled_condition(ctx, segment.label):
                value = segment.consume(ctx, stream)
                ctx[segment.label] = value
        return ctx

    def generate(self, **values) -> bytearray:
        ctx = OrderedDict()
        for segment in self.segments:
            if not segment.enabled_condition or segment.enabled_condition(values, segment.label):
                value = segment.digest(ctx, values)
                ctx[segment.label] = value
        payload = bytearray()
        for value in ctx.values():
            if value is not None and isinstance(value, bytes):
                payload.extend(value)
        return payload
