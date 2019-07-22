# -*- coding: utf-8 -*-

from missinglink.commands.cloud.backend_context import BackendContext


class GcpContext(BackendContext):

    @classmethod
    def get_kms(cls, crypto_key_path):
        from missinglink.crypto import GcpEnvelope

        return GcpEnvelope(crypto_key_path)
