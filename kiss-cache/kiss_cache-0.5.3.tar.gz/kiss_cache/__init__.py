import threading

from .cache import Cache
from .stores.django_cache import DjangoCacheStore
from .stores.in_memory import InMemoryStore

local = threading.local()
local.flush = False
