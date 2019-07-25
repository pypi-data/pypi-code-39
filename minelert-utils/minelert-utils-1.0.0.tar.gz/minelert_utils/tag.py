__version__ = "1.0.0"
__author__ = "Niel Venter"
__copyright__ = "Copyright 2019, Minelert"

from enum import Enum


class TagType(Enum):
    INGECOM = 42
    ML_TRACK = 81
    ML_PDS = 82


BATTERY_MAP = {
    TagType.INGECOM.value: [0.7, 0.85, 1.01, 1.16, 1.31, 1.47, 1.62, 1.77, 1.93, 2.08, 2.23, 2.39, 2.54, 2.69, 2.85, 3.04],
    TagType.ML_TRACK.value: [1.86, 1.86, 2.08, 2.22, 2.30, 2.49, 2.73, 2.86, 3.00, 3.16, 3.33, 3.53, 3.74, 3.74, 3.74, 3.74]
}

INGECOM_MAP = {
    '8C1012C4F3C0': '7802',
    '8C1812C4F3C0': '7803',
    '8C8012C4BF16': 'E2D0',
    '8C6812C4BF16': 'E2CD',
    '8CB812C65AD4': '5A97',
    '8CC812C65AD4': '5A99',
    '8C084D4B3137': '26E1',
    '8C104D4B3137': '26E2',
    '8C184D4B3137': '26E3',
    '8C204D4B3137': '26E4',
    '8C284D4B3137': '26E5'
}


class Tag:
    def __init__(self):
        self.tag_id = None
        self.tag_type = None
        self.battery = 0.00
        self.rssi = None

    def set_battery_voltage(self, value):
        if self.tag_type == TagType.ML_PDS:
            pass
        else:
            self.battery = BATTERY_MAP.get(self.tag_type)[value] if value < len(BATTERY_MAP.get(self.tag_type)) else 0.00

    def __str__(self):
        return 'tag_id={}, tag_type={}, voltage={}, rssi={}'.format(self.tag_id, self.tag_type, self.battery, self.rssi)








