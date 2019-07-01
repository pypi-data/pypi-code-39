# automatically generated by the FlatBuffers compiler, do not modify

# namespace: class2

import flatbuffers

class ClassificationClass2Response(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsClassificationClass2Response(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ClassificationClass2Response()
        x.Init(buf, n + offset)
        return x

    # ClassificationClass2Response
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ClassificationClass2Response
    def Response(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 8
            from .Probability import Probability
            obj = Probability()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # ClassificationClass2Response
    def ResponseLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def ClassificationClass2ResponseStart(builder): builder.StartObject(1)
def ClassificationClass2ResponseAddResponse(builder, response): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(response), 0)
def ClassificationClass2ResponseStartResponseVector(builder, numElems): return builder.StartVector(8, numElems, 4)
def ClassificationClass2ResponseEnd(builder): return builder.EndObject()
