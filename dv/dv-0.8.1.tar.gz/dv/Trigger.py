import dv.fb.Trigger


class Trigger(dv.fb.Trigger.Trigger):

    def __init__(self, fb_trigger):
        self._fb_trigger = fb_trigger

    @property
    def timestamp(self):
        return self.Timestamp()

    @property
    def type(self):
        return self.Type()

    @classmethod
    def from_fb(cls, obj):
        obj.__class__ = Trigger
        return obj
