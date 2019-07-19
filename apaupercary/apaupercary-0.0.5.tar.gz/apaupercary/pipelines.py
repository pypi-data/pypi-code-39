from apaupercary import scryfall, cardkingdom
def fetch_prices(name, vendor='cardkingdom'):
    data = scryfall.get_card_by_name(name)
    prints = scryfall.get_card_prints(data)
    prices = cardkingdom.price_data_for_card(name, prints)
    return prices

def fetch_cheapest_price(name, vendor='cardkingdom', availability=False):
    data = scryfall.get_card_by_name(name)
    prints = scryfall.get_card_prints(data)
    prices = cardkingdom.price_data_for_card(name, prints)
    edition, quality, price = cardkingdom.cheapest_price(prices, availability)
    res = {'print':edition,'quality':quality,'price':price}
    return res
