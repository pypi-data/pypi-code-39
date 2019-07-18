from utils import Sensitive


class Settings(dict):
    """Holder object for settings."""

    def masked(self):
        return dict(zip(self.keys(), (v.mask() if isinstance(v, Sensitive) else v for v in self.values())))

    def __getitem__(self, key):
        val = super().__getitem__(key)
        if isinstance(val, Sensitive):
            return val.obj
        return val
