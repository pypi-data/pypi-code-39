class DetectConfigs:
    def __init__(self, w, h, resize_out_ratio=4.0, threshold_distance=100.0, redzone_threshold_distance=100.0, max_fps=10,
                 delay_detected=0.5, max_miss=3.0):
        self.w = w
        self.h = h
        self.resize_out_ratio = resize_out_ratio
        self.threshold_distance = threshold_distance
        self.redzone_threshold_distance = redzone_threshold_distance
        self.max_fps = max_fps
        self.max_miss = max_miss
        self.delay_detected = delay_detected


class VisionDetectorHuman:
    class FaceBox:
        def __init__(self, left, top, right, bottom):
            self.left = left
            self.top = top
            self.right = right
            self.bottom = bottom

    def __init__(self, id, name, distance, face_box: FaceBox, portrait=None):
        self.id = id
        self.name = name
        self.distance = distance
        self.face_box = face_box
        self.portrait = portrait
        self.fresh = True
        self.timestamp_in_range = None

    def get(self, key, default=None):
        return getattr(self, key, default=default)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        setattr(self, key, value)
