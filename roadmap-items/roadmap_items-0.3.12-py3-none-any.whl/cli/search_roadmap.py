# search-roadmap.py - Searches for Roadmaps
import logging
import sys
from smoacks.cli_util import get_opts, get_session
from roadmap_items.Roadmap import Roadmap

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

def search():
    opts = get_opts('search_roadmap', 'Searches for Roadmaps in a roadmap_items',
                    { 'search_text': 'search_text' })

    session = get_session(opts)
    if not session:
        sys.exit('Invalid username/password.')

    success, resp_list =Roadmap.search(session, opts.search_text)

    if success:
        for resp in resp_list:
            print('{} - {}'.format(resp.get_ids(), resp.name))
    else:
        print('Search failed with code {} and message: {}'.format(resp.status_code, resp.text))