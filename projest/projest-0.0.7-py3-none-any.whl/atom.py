
class Atom:

    def __init__(self, atom_name, x_coordinate, y_coordinate, z_coordinate, occupancy, temperature_factor, element_symbol):
        self.atom_name = atom_name
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.z_coordinate = z_coordinate
        self.occupancy = occupancy
        self.temperature_factor = temperature_factor
        self.element_symbol = element_symbol
                       
    def __str__(self):
        return "%s - %.2f - %.2f - %.2f - %.2f - %.2f - %s" %(self.atom_name, self.x_coordinate, 
        self.y_coordinate, self.z_coordinate, self.occupancy, self.temperature_factor,
        self.element_symbol)