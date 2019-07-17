import time
from .utils import request_soup

CARDKINDOM_BASE = 'https://www.cardkingdom.com/'
CARDKINGDOM_CARD_API = CARDKINDOM_BASE + 'mtg/{edition}/{card}'

CARDKINDOM_CARD_QUALITIES = ['NM', 'EX', 'VG', 'G']

def CARDKINGDOM_URI(card, edition):
    _card = card.lower().replace(' ', '-').replace(':', '')
    _edition = edition.lower().replace(' ', '-').replace(':', '')
    return CARDKINGDOM_CARD_API.format(edition=_edition, card=_card)

def prices(soup):
    card_prices = []
    price_spans = soup.find_all('span', class_="stylePrice")
    for price_span in price_spans:
        price = price_span.text.strip().rstrip('\n').replace('$', '')
        card_prices.append(float(price))
    return card_prices

def availabilities(soup):
    card_availabilities = []
    card_qualities_list = soup.find_all('li', class_='itemAddToCart')
    for card_quality in card_qualities_list:
        if 'outOfStock' in card_quality['class']:
            card_availabilities.append(False)
        else:
            card_availabilities.append(True)
    return card_availabilities

def prices_and_availbility(soup):
    _soup = soup.find('ul', class_='addToCartByType')
    card_prices = prices(_soup)
    card_availabilities = availabilities(_soup)
    zipped = list(zip(CARDKINDOM_CARD_QUALITIES, card_prices, card_availabilities))
    results = {}
    for qual, price, avail in zipped:
        results[qual] = {'availability':avail, 'price':float(price)}
    return results




def handle_edition(edition):
    if edition == 'Kaladesh Inventions':
        return 'masterpiece-series-inventions'
    if edition == 'Unlimited Edition':
        return 'unlimited'
    if 'Judge' in edition:
        return 'promotional'
    if 'Volume' in edition:
        return edition.replace('Volume', 'Vol')
    if 'Commander 2011' == edition:
        return 'commander'
    if 'Limited Edition' in edition:
        return edition.replace('Limited Edition', '').strip()
    if 'Revised Edition' == edition:
        return '3rd-edition'
    return edition

def handle_name(name, edition):
    if edition == 'masterpiece-series-inventions':
        return name + '-KLD'
    if 'promotional' == edition:
        return name + '-judge-foil'
    return name


def price_data_for_card(name, prints):
    prices = {}
    for i, edition in enumerate(prints):
        _edition = handle_edition(edition)
        _name = handle_name(name, _edition)
        url = CARDKINGDOM_URI(_name, _edition)
        try:
            soup = request_soup(url)
            prices[edition] = prices_and_availbility(soup)
            if i != len(prints) - 1:
                time.sleep(0.05)
        except AttributeError:
            pass
            # print(_name, _edition)
    return prices


def cheapest_price(prices, must_be_available=False):
    lowest = float('inf')
    edition = None
    quality = None

    for card_edition, qualities in prices.items():
        for card_quality, price_avail in qualities.items():
            price = price_avail['price']
            avail = price_avail['availability']
            if must_be_available and not avail:
                continue
            if price < lowest:
                lowest = price
                edition = card_edition
                quality = card_quality
    return edition, quality, lowest
