from context import north_c9
from north_c9.location import Location
from north_c9.grid import Grid

if __name__ == '__main__':
    deck_grid = Grid(
        rows=21,
        columns=17,
        spacing=37.5,
        location=Location(-375, -219)
    )

    source = deck_grid.generate_class('N9Deck', 'n9_deck')

    with open('../north_c9/deck.py', 'w') as f:
        f.write(source)