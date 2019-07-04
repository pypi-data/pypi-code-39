"""Exposes a class object to query the cluster `/pins` via the REST API.
"""
from ipfshttpclient.client import base

class Section(base.SectionBase):
    def ls(self, cid=None, **kwargs):
        """Queries the `/pins` endpoint of the IPFS cluster to list a node's
        peers.

        Args:
            cid (str): CID of a specific pin to list; otherwise, list
                *all* pins.

        Examples:
            Query the IPFS cluster client for pins list.

            >>> client.pins.ls()

        """
        path = '/pins'
        if cid is not None:
            path = '/pins/{0}'.format(cid)

        return self._client.request(path, decoder='json', **kwargs)[0]

    def sync(self, cid=None, **kwargs):
        """Synchronizes the local status of pins with IPFS using the
        `/pins/sync` endpoint of the IPFS cluster.

        Args:
            cid (str): CID of a specific pin to sync; otherwise, sync
                *all* pins.

        Examples:
            Sync the IPFS cluster client for all pins.

            >>> client.pins.sync()
            []
        """
        path = '/pins/sync'
        if cid is not None:
            path = '/pins/{0}/sync'.format(cid)

        return self._client.request(path, decoder='json', method='post', **kwargs)[0]

    def recover(self, cid=None, **kwargs):
        """Recovers a pin from IPFS using the `/pins/recover` endpoint of the
        IPFS cluster.

        Args:
            cid (str): CID of a specific file to recover; otherwise, recover
                *all* pins.

        Examples:
            Sync the IPFS cluster client for all pins.

            >>> client.pins.recover()

        """
        path = '/pins/recover'
        if cid is not None:
            path = '/pins/{0}/recover'.format(cid)

        return self._client.request(path, decoder='json', method='post',
                                    offline=True, **kwargs)[0]

    @base.returns_no_item
    def add(self, cid, **kwargs):
        """Pins a single CID to the node.

        Args:
            cid (str): CID of a specific pin to add.

        .. note:: The `cid` can also be a valid path that begins with
            `ipfs/<path>`, `ipns/<path>` or `ipld/<path>`.

        Examples:
            Add a pin to the IPFS cluster client.

            >>> client.pins.add(QmZfF6C9j4VtoCsTp4KSrhYH47QMd3DNXVZBKaxJdhaPab')

        """
        path = '/pins/{0}'.format(cid)
        return self._client.request(path, decoder='json', method='post', **kwargs)

    @base.returns_no_item
    def rm(self, cid, **kwargs):
        """Removes pin for a single CID to the node.

        Args:
            cid (str): CID of a specific pin to remove.

        .. note:: The `cid` can also be a valid path that begins with
            `ipfs/<path>`, `ipns/<path>` or `ipld/<path>`.

        Examples:
            Remove a pin to the IPFS cluster client.

            >>> client.pins.rm(QmZfF6C9j4VtoCsTp4KSrhYH47QMd3DNXVZBKaxJdhaPab')

        """
        path = '/pins/{0}'.format(cid)
        return self._client.request(path, decoder='json', method='delete', **kwargs)
