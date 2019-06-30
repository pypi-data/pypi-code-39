# search-roadmap_item.py - Searches for RoadmapItems
import logging
import sys
from smoacks.cli_util import get_opts, get_session
from roadmap_items.RoadmapItem import RoadmapItem

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

def search():
    opts = get_opts('search_roadmap_item', 'Searches for RoadmapItems in a roadmap_items',
                    { 'search_text': 'search_text' })

    session = get_session(opts)
    if not session:
        sys.exit('Invalid username/password.')

    success, resp_list =RoadmapItem.search(session, opts.search_text)

    if success:
        for resp in resp_list:
            print('{} - {}'.format(resp.get_ids(), resp.name))
    else:
        print('Search failed with code {} and message: {}'.format(resp.status_code, resp.text))