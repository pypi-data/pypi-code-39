# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

# /// A minimal version of the ball, useful when bandwidth needs to be conserved.
class TinyBall(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsTinyBall(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = TinyBall()
        x.Init(buf, n + offset)
        return x

    # TinyBall
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # TinyBall
    def Location(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from .Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # TinyBall
    def Velocity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from .Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def TinyBallStart(builder): builder.StartObject(2)
def TinyBallAddLocation(builder, location): builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(location), 0)
def TinyBallAddVelocity(builder, velocity): builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(velocity), 0)
def TinyBallEnd(builder): return builder.EndObject()
