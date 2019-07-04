"""Exposes a class object to query the cluster `/health` via the REST API.
"""
from ipfshttpclient.client import base

class Section(base.SectionBase):
    def graph(self, **kwargs):
        """Queries the `/health/graph` endpoint of the IPFS cluster.

        Examples:
            Query the IPFS cluster client for cluster health graph.

            >>> client.health.graph()
            {
                "ClusterID":"12D3...",
                "ipfs_links":
                    {"QmSU...": [...]},
                "cluster_links":
                    {"12D3...": [...]},
                "cluster_to_ipfs":
                    {"12D3...": "QmSU...""}
            }
        """
        r = self._client.request('/health/graph', decoder='json', **kwargs)
        if isinstance(r, list) and len(r) == 1:
            return r[0]
        else: # pragma: no cover
            return r
