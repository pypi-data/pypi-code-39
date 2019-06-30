# add-roadmap.py - Adds a Roadmap
import logging
import sys
from smoacks.cli_util import get_opts, get_session
from roadmap_items.Roadmap import Roadmap


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()



def add():
    opts = get_opts('add_roadmap', 'Adds Roadmap to a roadmap_items',
                    { 'name': 'name',
                     })

    session = get_session(opts)
    if not session:
        sys.exit('Invalid username/password.')

    
    add_item = Roadmap(**vars(opts))
    success, resp = add_item.save_new(session)

    if success:
        print('Added Roadmap with id: {}'.format(','.join(add_item.get_ids())))
    else:
        print('Add failed with code {} and message: {}'.format(resp.status_code, resp.text))