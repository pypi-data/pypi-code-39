from typing import Any, BinaryIO, Dict, Optional, Union


class Consumer:

    def length(self, ctx: Dict[str, Any], label: str, values: Optional[Dict[str, Any]] = None):
        return None

    def read(self, ctx: Dict[str, Any], label: str, stream: BinaryIO):
        raise NotImplemented

    def write(self, ctx: Dict[str, Any], label: str, data: Union[bytes, int], values: Dict[str, Any]):
        raise NotImplemented


class ConstantConsumption(Consumer):

    def __init__(self, length: int):
        self._length = length

    def length(self, _, __, values: Optional[Dict[str, Any]] = None):
        return self._length

    def read(self, ctx: Dict[str, Any], label: str, stream: BinaryIO):
        return stream.read(self.length(ctx, label))

    def write(self, _, __, data: bytes, ___):
        return data


class SharedConsumption(Consumer):

    def __init__(self, length: int, masks: Dict[str, int]):
        self._length = length
        self.masks = masks

    @property
    def id(self):
        return "+".join(self.masks.keys())

    def length(self, _, __, values: Optional[Dict[str, Any]] = None):
        return self._length

    @staticmethod
    def shift_distance(value: int):
        return len(bin(value)) - len(bin(value).rstrip("0"))

    def read(self, ctx: Dict[str, Any], label: str, stream: BinaryIO):
        if self.id not in ctx:
            ctx[self.id] = int(stream.read(self.length(ctx, label)).hex(), 16)
        return ctx[self.id] & self.masks[label]

    def write(self, ctx: Dict[str, Any], label: str, data: int, values):
        if self.id not in ctx:
            ctx[self.id] = 0
        if data & self.masks[label] != data:
            data = data << self.shift_distance(self.masks[label])
        ctx[self.id] |= data
        if len([l for l in self.masks if l not in ctx]) == 1:
            return ctx[self.id].to_bytes(self.length(ctx, label, values), "big")


class DynamicConsumption(Consumer):

    def __init__(self, target: str):
        self.target = target

    def length(self, ctx: Dict[str, Any], _, values: Optional[Dict[str, Any]] = None):
        return ctx[self.target] if values is None else values[self.target]

    def read(self, ctx: Dict[str, Any], label: str, stream: BinaryIO):
        return stream.read(self.length(ctx, label))

    def write(self, _, __, data: bytes, ____):
        return data
