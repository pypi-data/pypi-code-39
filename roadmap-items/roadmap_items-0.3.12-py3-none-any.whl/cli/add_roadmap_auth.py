# add-roadmap_auth.py - Adds a RoadmapAuth
import logging
import sys
from smoacks.cli_util import get_opts, get_session
from roadmap_items.RoadmapAuth import RoadmapAuth
from roadmap_items.Roadmap import Roadmap

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


def Roadmap_lookup(session, search_val):
    success, res = Roadmap.search(session, search_val)
    if success:
        for item in res:
            if item.name == search_val:
                return item.roadmap_id 

def add():
    opts = get_opts('add_roadmap_auth', 'Adds RoadmapAuth to a roadmap_items',
                    { 'Roadmap.name': 'Roadmap.name',
                    'group_id': 'group_id',
                    'role': 'role',
                     })

    session = get_session(opts)
    if not session:
        sys.exit('Invalid username/password.')

    
    opts.roadmap_id = Roadmap_lookup(session, vars(opts)['Roadmap.name'])
    add_item = RoadmapAuth(**vars(opts))
    success, resp = add_item.save_new(session)

    if success:
        print('Added RoadmapAuth with id: {}'.format(','.join(add_item.get_ids())))
    else:
        print('Add failed with code {} and message: {}'.format(resp.status_code, resp.text))