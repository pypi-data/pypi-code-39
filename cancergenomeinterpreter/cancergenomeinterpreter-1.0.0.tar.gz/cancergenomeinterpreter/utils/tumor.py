import csv
import logging


def grand_parents(parents, family):
    grandpas = []
    for p in parents:
        if p in family:
            grandpas += family[p]['PARENTS']
        else:
            return None

    return grandpas


class Tumor(object):
    FAMILY = {}

    @staticmethod
    def load_family(tumor_file):

        tumors_noparents = {}
        with open(tumor_file, 'rt') as fd:
            for tumor in csv.DictReader(fd, delimiter='\t'):
                tumors_noparents[tumor['ID']] = tumor

        tumors_parents = {}
        while len(tumors_noparents) > 0:

            # Fill tumor parents
            count = 0
            for key, tumor in tumors_noparents.items():
                parents = [p.strip() for p in tumor['PARENTS'].split(',')] if tumor['PARENTS'] != '' else []
                if len(parents) == 0:
                    tumor['PARENTS'] = parents
                    tumors_parents[key] = tumor
                    count += 1
                    continue

                grandpas = grand_parents(parents, tumors_parents)
                if grandpas is None:
                    continue

                tumor['PARENTS'] = parents + grandpas
                tumors_parents[key] = tumor
                count += 1

            # Remove resolved tumors
            for key in tumors_parents:
                if key in tumors_noparents:
                    del tumors_noparents[key]

            if count == 0:
                raise RuntimeError(
                    "The cancer type parents hierarchy has a loop at {}".format([t for t in tumors_noparents.keys()]))

        for pid, ptumor in tumors_parents.items():
            ptumor['OFFSPRING'] = []
            for cid, ctumor in tumors_parents.items():
                if pid in ctumor['PARENTS']:
                    ptumor['OFFSPRING'].append(cid)

        Tumor.FAMILY = tumors_parents

    def __init__(self, name):
        if name not in Tumor.FAMILY:
            logging.warning("Unknown cancer type '{}'".format(name))
        self.name = name

    def get_offspring(self):
        return Tumor.FAMILY[self.name]['OFFSPRING']

    def get_parents(self):
        return Tumor.FAMILY[self.name]['PARENTS']

    def match(self, other):

        # Checking perfect tumor match
        if self.name == other.name:
            return True

        # Checking if I'm an other's parent
        if other.name in Tumor.FAMILY:
            other_parents = Tumor.FAMILY[other.name]['PARENTS']
            if self.name in other_parents:
                return True

        # Checking if other is my parent
        if self.name in Tumor.FAMILY:
            my_parents = Tumor.FAMILY[self.name]['PARENTS']
            if other.name in my_parents:
                return True

        # We are not parents
        return False

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return "{}".format(self.name)
