#! /usr/bin/env python3
import click
import tempfile
import logging
import requests
import gzip
import sys
import json


from datetime import date, timedelta
from pathlib import Path
from mailbox import Maildir, mbox
from urllib.parse import urljoin

# Setup the logging.
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
log.addHandler(ch)


# Configuration Path to store the current state of hksync.
CONFIG_PATH = Path("~/.config/hksync/settings.json")


def prepare_mbox_url(server, mlist, start, end=None):
    """Prepare the URL download mbox archives from Hyperkitty.

    Here is a sample URL to download from:
        https://lists.mailman3.org/archives/list/mailman-users@mailman3.org
        /export/mailman-users@mailman3.org-2019-08.mbox.gz?
        start=2019-07-01&end=2019-08-01
    """
    if end is None:
        end = date.today()
    end = end.strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    filename = f'{mlist}-{start}-{end}.mbox.gz'

    # Add the trailing `/` in the server's URL to make sure that urljoin is
    # working as we intend it to.
    if not server.endswith('/'):
        server = server + '/'
    return urljoin(server,
                   f'list/{mlist}/export/{filename}?start={start}&end={end}')


def initialize(maildir_path):
    """Perform some initialization steps."""
    # Setup the directory where we'll download the archives.
    return initialize_maildir(maildir_path)


# Download archives from Hyperkitty.
def get_archives(server, mlist, download_path, start, end=None):
    """Get all the archives for the month.

    Download and extract gzipped mbox from Hyperkitty.

    :param server: Server to download archives from.
    :param mlist: MailingList to download archives for.
    :param download_path: Directory to download mbox in.
    :param start: Start date to download from.
    :param end: End date to download till, defaults to today.

    :returns: Path to the downloaded gzip mbox file.
    """
    url = prepare_mbox_url(server, mlist, start=start, end=end)
    log.debug('Downlaoding archives for %s from %s', mlist, url)
    try:
        res = requests.get(url, stream=True)
    except requests.HTTPError:
        raise ValueError
    if res.status_code != 200:
        click.secho('Unable to download the archives, either the server\'s '
                    'URL is wrong or MailingList does not exist.', fg='red')
        raise ValueError
    mbox_path = download_path / f'{mlist}_{start}_{end}.mbox.gz'
    with mbox_path.open(mode='wb') as fd:
        for chunk in res.iter_content(chunk_size=1024):
            fd.write(chunk)

    return mbox_path


# Generate Maildir from archives.
def initialize_maildir(path):
    """Initialize the Maildir for a MailingList if it doesn't exist.

    Check if there is a Maildir at the expected path.  If it does, do nothing,
    otherwise initialize the Maildir.

    :param config: The current config instance.
    :param server: The server to create maildir for.
    :param mlist: The MailingList to initialize Maildir for.

    :returns: Path to the created Maildir.
    """
    log.debug('Downloading to maildir at %s', path)
    return Maildir(path, create=True)


def add_to_maildir(maildir, mbox_path, keep_mbox=False):
    """Add emails from mbox to Maildir.

    If the mbox was unreadable or corrupt, a FailedToAddError is raised, which
    can be used by the caller to re-download the mbox file.

    :param maildir_path: Maildir instance to add emails to.
    :param mbox_path: Path to the mbox to add the emails.

    :returns: None if success.

    :raises: FailedToAddError
    """
    log.debug('Adding emails from %s', mbox_path)
    counter = 0
    for eml in mbox(mbox_path):
        maildir.add(eml)
        counter += 1
    log.debug('Removing mbox')
    mbox_path.unlink()
    return counter


def decompress_mbox(mbox_path):
    outf = str(mbox_path)[:-3]
    log.debug('Decompressing %s to %s', mbox_path, outf)
    try:
        with gzip.open(mbox_path) as fd:
            with open(outf, 'wb') as outfile:
                outfile.write(fd.read())
    except OSError:
        click.secho('Unable to download archives, please re-try', fg='red')
    log.debug('Deleting gzip mbox at %s', mbox_path)
    mbox_path.unlink()
    return Path(outf)


def sync_one_list(mlist, server, maildir, since, days):
    """Sync one MailingList from remote Hyperkitty to local Maildir. """
    mbox_tmp = Path(tempfile.mkdtemp())

    if since is not None:
        try:
            start = date.fromisoformat(since)
        except ValueError:
            click.secho('Wrong data format, it should of the type YYYY-MM-DD',
                        fg='red')
            raise
    elif days is not None:
        start = date.today() - timedelta(days=days)
    else:
        start = date.today() - timedelta(days=1)


    try:
        mbox_path = get_archives(server, mlist,
                                start=start,
                                download_path=mbox_tmp)
    except ValueError as e:
        click.secho('Failed to download archives, an error occurred...',
                    fg='red')
        logging.debug(e)
        raise

    # Decompress the gzipeed mbox file and add emails to local maildir.
    mbox_decompressed_path = decompress_mbox(mbox_path)
    total_emails = add_to_maildir(maildir, mbox_decompressed_path)
    log.info('Added %s emails for %s', total_emails, mlist)
    mbox_tmp.rmdir()


def add_list(mlist, server):
    """Add one MailingList to the list."""
    # Create the config directory, in case it doesn't exist.
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    Config = {}
    if CONFIG_PATH.exists():
        try:
            Config = json.loads(CONFIG_PATH.read_text())
        except json.decoder.JSONDecodeError:
            Config = {}
    Config[mlist] = {'server': server}
    CONFIG_PATH.write_text(json.dumps(Config))


def remove_list(mlist):
    """Remove one MailingList from the CONFIG."""
    if not CONFIG_PATH.exists():
        return None
    Config = json.loads(CONFIG_PATH.read_text())
    if mlist in Config:
        del Config[mlist]
    if Config:
        text = json.dumps(Config)
    else:
        text = ''
    CONFIG_PATH.write_text(text)


def get_lists(mlist=None):
    """Get all the MailingList we are subscribed to."""
    if not CONFIG_PATH.exists():
        return {}
    lists = json.loads(CONFIG_PATH.read_text())
    if mlist:
        if mlist in lists:
            return {mlist: lists.get(mlist)}
        raise ValueError('MailngList is not added, please run hksync add first.')
    return lists


@click.group()
@click.option('--debug', default=False)
def hksync(debug):
    """hksync: Sync archives for a Hyperkitty mailing list into local Maildir."""
    if debug:
        log.setLevel(logging.DEBUG)


@hksync.command()
@click.option('--maildir-path', '-dl',
              default="~/hksync",
              help='Path to download archives.')
@click.option('--since',
              help="""Sync emails newer than this date, YYYY-MM-DD format.
                   Defaults to last 1 week.""")
@click.option('--days',
              help="""Sync emails for past these many days.
                      Ignored if --since is provided.""")
@click.option('--mlist', '-m',
              help='MailingList to download archives for.')
def sync(maildir_path, since, days, mlist):
    """
    hksync: Sync archives for a Hyperkitty mailing list into local Maildir.

    \b
    example usage:
       # Sync emails since July 2019 for all the lists subscribed.
       $ hksync sync --since 2019-07-01

    """
    maildir = initialize(Path(maildir_path).expanduser())
    for mlist, value in get_lists(mlist).items():
        try:
            sync_one_list(mlist, value['server'], maildir, since, days)
        except ValueError as e:
            print(f'Unable to sync {mlist} due to exception: {e}')



@hksync.command()
@click.option('--server', '-s',
              required=True,
              help='Server to sync from.')
@click.option('--mlist', '-m',
              required=True,
              help='MailingList to download archives for.')
def add(server, mlist):
    """Add a new MailingList to sync regularly.

    \b
    Example usage:
        # Add a new MailingList to sync.
        $ hksync add --server https://lists.mailman3.org/archives --mlist mailman-users@mailman3.org

    """
    add_list(mlist, server)


@hksync.command()
@click.argument('mlist')
def remove(mlist):
    """Remote a MailingList from the list to sync regularly."""
    remove_list(mlist)


@hksync.command()
def list():
    """List all the MailingList subscription."""
    all_lists = get_lists()
    if not all_lists:
        click.secho('No MailingLists', fg='red')
    for mlist, value in all_lists.items():
        print('"{}" from "{}"'.format(mlist, value['server']))


if __name__ == '__main__':
    hksync()
