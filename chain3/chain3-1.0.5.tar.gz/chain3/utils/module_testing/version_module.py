from mc_utils import (
    is_string,
)


class VersionModuleTest:
    def test_net_version(self, chain3):
        version = chain3.version.network

        assert is_string(version)
        assert version.isdigit()

    def test_mc_protocolVersion(self, chain3):
        protocol_version = chain3.version.ethereum

        assert is_string(protocol_version)
        assert protocol_version.isdigit()
