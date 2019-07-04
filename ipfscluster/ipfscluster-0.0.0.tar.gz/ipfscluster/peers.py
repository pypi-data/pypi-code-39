"""Exposes a class object to query the cluster `/peers` via the REST API.
"""
from ipfshttpclient.client import base

class Section(base.SectionBase):
    def ls(self, **kwargs):
        """Queries the `/peers` endpoint of the IPFS cluster to list a node's
        peers.

        Examples:
            Query the IPFS cluster client for peer list.

            >>> client.peers.ls()

        """
        plist = self._client.request('/peers', decoder='json', **kwargs)[0]
        return plist

    def rm(self, peerid, **kwargs):
        """Attempts to remove the specified peer from the cluster.

        Args:
            peerid (str): `id` of the peer to remove from the cluster.
        """
        r = self._client.request('/peers/{0}'.format(peerid),
                                decoder='json', method='delete', **kwargs)
        return r
