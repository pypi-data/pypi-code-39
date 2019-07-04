"""Exposes a class object to query the cluster `/allocations` via the REST API.
"""
from ipfshttpclient.client import base

class Section(base.SectionBase):
    def ls(self, cid=None, **kwargs):
        """Queries the `/allocations` endpoint of the IPFS cluster to list
        all the pins and their allocation metadata.

        Args:
            cid (str): CID of a specific allocation to check; otherwise, list
                *all* allocations.

        Examples:
            Query the IPFS cluster client for pin allocations list.

            >>> client.allocations.ls()
            [{
                "replication_factor_min":-1,
                "replication_factor_max":-1,
                "name":"",
                "shard_size":104857600,
                "user_allocations":null,
                "metadata":null,
                "cid":{"/":"QmZfF..."},
                "type":2,
                "allocations":[],
                "max_depth":-1,
                "reference":null},
             {...}]
        """
        path = '/allocations'
        if cid is not None:
            path = '/allocations/{0}'.format(cid)

        return self._client.request(path, decoder='json', **kwargs)[0]
