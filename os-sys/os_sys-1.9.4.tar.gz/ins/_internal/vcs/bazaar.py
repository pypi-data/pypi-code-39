from __future__ import absolute_import

import logging
import os

from ins._vendor.six.moves.urllib import parse as urllib_parse

from ins._internal.download import path_to_url
from ins._internal.utils.misc import display_path, rmtree
from ins._internal.vcs import VersionControl, vcs

logger = logging.getLogger(__name__)


class Bazaar(VersionControl):
    name = 'bzr'
    dirname = '.bzr'
    repo_name = 'branch'
    schemes = (
        'bzr', 'bzr+http', 'bzr+https', 'bzr+ssh', 'bzr+sftp', 'bzr+ftp',
        'bzr+lp',
    )

    def __init__(self, url=None, *args, **kwargs):
        super(Bazaar, self).__init__(url, *args, **kwargs)
        # This is only needed for python <2.7.5
        # Register lp but do not expose as a scheme to support bzr+lp.
        if getattr(urllib_parse, 'uses_fragment', None):
            urllib_parse.uses_fragment.extend(['lp'])

    @staticmethod
    def get_base_rev_args(rev):
        return ['-r', rev]

    def export(self, location):
        """
        Export the Bazaar repository at the url to the destination location
        """
        # Remove the location to make sure Bazaar can export it correctly
        if os.path.exists(location):
            rmtree(location)

        url, rev_options = self.get_url_rev_options(self.url)
        self.run_command(
            ['export', location, url] + rev_options.to_args(),
            show_stdout=False,
        )

    @classmethod
    def fetch_new(cls, dest, url, rev_options):
        rev_display = rev_options.to_display()
        logger.info(
            'Checking out %s%s to %s',
            url,
            rev_display,
            display_path(dest),
        )
        cmd_args = ['branch', '-q'] + rev_options.to_args() + [url, dest]
        cls.run_command(cmd_args)

    def switch(self, dest, url, rev_options):
        self.run_command(['switch', url], cwd=dest)

    def update(self, dest, url, rev_options):
        cmd_args = ['pull', '-q'] + rev_options.to_args()
        self.run_command(cmd_args, cwd=dest)

    @classmethod
    def get_url_rev_and_auth(cls, url):
        # hotfix the URL scheme after removing bzr+ from bzr+ssh:// readd it
        url, rev, user_pass = super(Bazaar, cls).get_url_rev_and_auth(url)
        if url.startswith('ssh://'):
            url = 'bzr+' + url
        return url, rev, user_pass

    @classmethod
    def get_remote_url(cls, location):
        urls = cls.run_command(['info'], show_stdout=False, cwd=location)
        for line in urls.splitlines():
            line = line.strip()
            for x in ('checkout of branch: ',
                      'parent branch: '):
                if line.startswith(x):
                    repo = line.split(x)[1]
                    if cls._is_local_repository(repo):
                        return path_to_url(repo)
                    return repo
        return None

    @classmethod
    def get_revision(cls, location):
        revision = cls.run_command(
            ['revno'], show_stdout=False, cwd=location,
        )
        return revision.splitlines()[-1]

    @classmethod
    def is_commit_id_equal(cls, dest, name):
        """Always assume the versions don't match"""
        return False


vcs.register(Bazaar)
