# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class BallInfo(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsBallInfo(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = BallInfo()
        x.Init(buf, n + offset)
        return x

    # BallInfo
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # BallInfo
    def Physics(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .Physics import Physics
            obj = Physics()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # BallInfo
    def LatestTouch(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .Touch import Touch
            obj = Touch()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # BallInfo
    def DropShotInfo(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .DropShotBallInfo import DropShotBallInfo
            obj = DropShotBallInfo()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def BallInfoStart(builder): builder.StartObject(3)
def BallInfoAddPhysics(builder, physics): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(physics), 0)
def BallInfoAddLatestTouch(builder, latestTouch): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(latestTouch), 0)
def BallInfoAddDropShotInfo(builder, dropShotInfo): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(dropShotInfo), 0)
def BallInfoEnd(builder): return builder.EndObject()
