from enum import Enum


class SubtitleMode(Enum):
    NOTHING = 0
    ANCILLARY = 1
    DTVCC = 2
    EMBEDDED = 3

    STATUS_TO_STR = [
        "nothing",
        "Ancillary data / CDP",
        "A/53 / DTVCC Transport",
        "Embedded"
    ]

    def to_string(self):
        return SubtitleMode.STATUS_TO_STR.value[self.value]


    @staticmethod
    def from_string(string):
        try:
            return SubtitleMode(SubtitleMode.STATUS_TO_STR.value.index(string))
        except:
            return SubtitleMode.NOTHING