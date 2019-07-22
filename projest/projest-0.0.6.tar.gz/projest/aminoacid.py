
class Aminoacid:

    def __init__(self, residue_name, residue_sequence_number):
        self.residue_name = residue_name
        self.residue_sequence_number = residue_sequence_number
                
    def __str__(self):
        return "%s - %.2s" %(self.residue_name, self.residue_sequence_number)
