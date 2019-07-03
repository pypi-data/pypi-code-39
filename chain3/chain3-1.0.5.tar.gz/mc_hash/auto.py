from mc_hash.backends.auto import (
    AutoBackend,
)
from mc_hash.main import (
    Keccak256,
)

keccak = Keccak256(AutoBackend())
