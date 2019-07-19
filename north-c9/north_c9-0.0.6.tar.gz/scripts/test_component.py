from north_c9.location import Location, Rotation, Component, Grid, n9_deck


class Link(Component):
    pass


upper_arm = Link('Link1', Location())
lower_arm = Link('Link2', Location(10), Rotation(z=90), parent=upper_arm)
effector = Link('Effector', Location(10), parent=lower_arm)
print(effector.location.root_location)
print()