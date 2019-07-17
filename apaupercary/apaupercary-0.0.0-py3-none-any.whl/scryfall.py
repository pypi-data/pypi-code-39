from .utils import PAYLOAD_ABOUT
import requests, time

SCRYFALL_API = 'https://api.scryfall.com/'
EXACT_NAME_API = '{}cards/named'.format(SCRYFALL_API)
BASIC_LAND_TYPES = ['swamp', 'forest', 'island', 'plains', 'mountain']

def is_basic_land(name):
    return name.lower() in BASIC_LAND_TYPES

def get_card_by_name(name):
    r = requests.get(EXACT_NAME_API, params={**PAYLOAD_ABOUT, 'exact': name})
    return r.json()

def get_card_tcgplayer_id(card_data):
    return card_data['tcgplayer_id']

def get_card_prints(card_data):
    set_names = set({})
    url = card_data['prints_search_uri']
    has_more = True

    while has_more:
        r = requests.get(url, params=PAYLOAD_ABOUT)
        res = r.json()
        has_more = res['has_more']

        for card in res['data']:
            if 'paper' in card['games']:
                set_names.add(card['set_name'])

        if has_more:
            url = res['next_page']
            time.sleep(0.05)

    return list(set_names)
