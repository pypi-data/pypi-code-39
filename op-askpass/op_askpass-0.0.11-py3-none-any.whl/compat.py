dataclass = None
try:
    from dataclasses import dataclass
except ImportError:
    from attr import dataclass
