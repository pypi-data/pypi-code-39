from mc_utils import (
    is_boolean,
    is_integer,
    is_string,
)


class NetModuleTest:
    def test_net_version(self, chain3):
        version = chain3.net.version

        assert is_string(version)
        assert version.isdigit()

    def test_net_listening(self, chain3):
        listening = chain3.net.listening

        assert is_boolean(listening)

    def test_net_peerCount(self, chain3):
        peer_count = chain3.net.peerCount

        assert is_integer(peer_count)
