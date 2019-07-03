from mc_utils.curried import (
    apply_formatters_to_dict,
    apply_key_map,
)
from hexbytes import (
    HexBytes,
)

from chain3.middleware.formatting import (
    construct_formatting_middleware,
)
from chain3.utils.toolz import (
    compose,
)

remap_gmc_poa_fields = apply_key_map({
    'extraData': 'proofOfAuthorityData',
})

pythonic_gmc_poa = apply_formatters_to_dict({
    'proofOfAuthorityData': HexBytes,
})

gmc_poa_cleanup = compose(pythonic_gmc_poa, remap_gmc_poa_fields)

gmc_poa_middleware = construct_formatting_middleware(
    result_formatters={
        'mc_getBlockByHash': gmc_poa_cleanup,
        'mc_getBlockByNumber': gmc_poa_cleanup,
    },
)
