import logging
import re

from cancergenomeinterpreter.prescription.entities.alteration import Alteration

MATCH_LEVEL_NONE = 0
MATCH_LEVEL_GENE = 1
MATCH_LEVEL_GENE_AND_TYPE = 2
MATCH_LEVEL_COMPLETE = 3


class GeneMark(object):

    def __init__(self, gene, mark_types):
        self.gene = gene
        self.mark_types = mark_types

    def match(self, observed_alterations):

        # Check gene only level match
        gene_alterations = [alt for alt in observed_alterations if self.gene in alt.gene and alt.pam_no_polymorphism]
        if len(gene_alterations) == 0:
            return MATCH_LEVEL_NONE, []

        # Check gene and type level match
        gene_and_type_alterations = [alt for alt in gene_alterations if alt.mark_type in self.mark_types]
        if len(gene_and_type_alterations) == 0:
            return MATCH_LEVEL_GENE, gene_alterations

        return MATCH_LEVEL_GENE_AND_TYPE, gene_and_type_alterations


class ProteinChange(object):
    __PROTEIN_CHANGE = re.compile(r"([^0-9]*)([0-9]+)([^0-9]*)")

    def __init__(self, protein_change):

        if '|' in protein_change:
            consequence, protein_change = protein_change.split('|')
            self.consequence = consequence
            self.protein_change = protein_change
        else:
            self.consequence = None
            self.protein_change = protein_change

    def match(self, alteration: Alteration):

        # Check consequence if needed
        if self.consequence is not None and self.consequence != alteration.consequence:
            return False

        # Check if condition is 'everything' and return true only if it's a PAM or NO POLYMORPHISM alteration
        if self.protein_change == '.':
            return alteration.pam_no_polymorphism

        # Check range condition
        if '-' in self.protein_change:
            pos_ini, pos_end = [int(i) for i in self.protein_change.split('-')]
            m = self.__PROTEIN_CHANGE.match(alteration.alteration)
            if m is None:
                if re.search('-', alteration.alteration):
                    alteration_ranged = [int(p) for p in alteration.alteration.split('-')]
                    if alteration_ranged[0] >= pos_ini and alteration_ranged[1] <= pos_end:  # Is a range
                        return True
                    else:
                        return False
                else:
                    logging.error("Malformated alteration '{}'".format(alteration.row))
                    return False

            obs_ref, obs_pos, obs_alt = m.groups()
            return pos_ini <= int(obs_pos) <= pos_end

        # Check protein change
        m = self.__PROTEIN_CHANGE.match(self.protein_change)
        if m is None:
            logging.error("Malformated biomarker condition '{}'".format(self.protein_change))
            return False
        rule_ref, rule_pos, rule_alt = m.groups()

        m = self.__PROTEIN_CHANGE.match(alteration.alteration)
        if m is None:
            return False
        obs_ref, obs_pos, obs_alt = m.groups()

        if rule_ref != '.' and rule_ref != obs_ref:
            return False

        if rule_pos != obs_pos:
            return False

        if rule_alt == '.':
            return True

        if rule_alt == obs_alt:
            alteration.perfect_match = True
            return True

        return False

    def __str__(self):

        if self.consequence is not None:
            return "{}|{}".format(self.consequence, self.protein_change)

        return "{}".format(self.protein_change)

    def __repr__(self):
        return self.__str__()


class MutMark(GeneMark):
    MARK_TYPE = 'MUT'

    @staticmethod
    def parse(gene, alteration):

        # Extract gene from alteration
        if ':' not in alteration:
            logging.error(alteration)

        colon = alteration.index(':')
        if alteration[:colon] != gene:
            raise RuntimeError("Mismatch gene and alteration column order")
        alteration = alteration[colon:]

        wild_type = alteration.startswith('::wildtype:')
        if wild_type:
            alteration = alteration[len('::wildtype:'):]
        else:
            # Remove colon prefix
            alteration = alteration[1:]

        # Split alterations list
        protein_changes = [ProteinChange(i.strip()) for i in alteration.split(',')]

        return MutMark(gene, wild_type, protein_changes)

    def __init__(self, gene, wild_type, protein_changes):
        super().__init__(gene, [self.MARK_TYPE])
        self.wild_type = wild_type
        self.protein_changes = protein_changes

    def match_protein_change(self, alteration):
        """
         Check if the given alteration has a valid mark protein change

        :param alteration: Alteration to check the protein change
        :return: True if this alteration has one valid protein change in this marker.
        """

        # Check wild type
        return_value = True if not self.wild_type else False

        # Check protein chage match
        for protein_change in self.protein_changes:
            if protein_change.match(alteration):
                return return_value

        return not return_value

    def match(self, observed_alterations):

        # Check gene and type levels
        level, match_alterations = super().match(observed_alterations)

        if level < MATCH_LEVEL_GENE_AND_TYPE:
            return level, match_alterations

        # Check that at least one position has a mutation
        complete_match_alterations = [alt for alt in match_alterations if self.match_protein_change(alt)]

        if len(complete_match_alterations) == 0:
            return level, match_alterations

        return MATCH_LEVEL_COMPLETE, complete_match_alterations

    def __str__(self):
        return "MUT:{}:{}".format(self.gene, self.protein_changes)


class ExprMark(GeneMark):
    MARK_TYPE = 'EXPR'

    @staticmethod
    def parse(gene, alteration):
        return ExprMark(gene, alteration)

    def __init__(self, gene, expression):
        super().__init__(gene, [self.MARK_TYPE])
        self.expression = expression

    def match(self, observed_alterations):
        # Check gene and type levels
        level, match_alterations = super().match(observed_alterations)

        if level < MATCH_LEVEL_GENE_AND_TYPE:
            return level, match_alterations

        # TODO Check alteration expression
        return level, match_alterations


class CnaMark(GeneMark):
    MARK_TYPE = 'CNA'

    @staticmethod
    def parse(gene, alteration):
        return CnaMark(gene, alteration)

    def __init__(self, gene, expression):
        super().__init__(gene, [self.MARK_TYPE])
        self.expression = expression.upper()

    def match(self, observed_alterations):

        # Check gene and type levels
        level, match_alterations = super().match(observed_alterations)

        if level < MATCH_LEVEL_GENE_AND_TYPE:
            return level, match_alterations

        # Check complete match
        complete_match_alterations = [alt for alt in match_alterations if alt.alteration.upper() == self.expression]

        if len(complete_match_alterations) == 0:
            return level, match_alterations

        return MATCH_LEVEL_COMPLETE, complete_match_alterations


class FusMark(object):
    MARK_TYPE = 'FUS'

    @staticmethod
    def parse(gene, alteration):
        return FusMark(gene, alteration)

    def __init__(self, gene, expression):
        self.oncogenic_partner = gene
        fusion_separator = '-' if '-' in expression else '__'
        partners = [g.strip() for g in expression.split(fusion_separator) if g != self.oncogenic_partner and g != '.']
        if len(partners) > 1:
            raise RuntimeError("Invalid fusion expression '{}'.".format(expression))
        self.other_partner = None if len(partners) == 0 else partners[0]

    def match(self, observed_alterations):

        # Check if the oncogenic partner has any alteration of any type
        any_type_alterations = [alt for alt in observed_alterations if self.oncogenic_partner in alt.gene]
        if len(any_type_alterations) == 0:
            return MATCH_LEVEL_NONE, []

        # Check if there is any alteration with both partners
        if self.other_partner is None:
            complete_match_alterations = [alt for alt in observed_alterations if
                                          alt.mark_type == self.MARK_TYPE and
                                          self.oncogenic_partner in alt.gene]
        else:
            complete_match_alterations = [alt for alt in observed_alterations if
                                          alt.mark_type == self.MARK_TYPE and
                                          self.oncogenic_partner in alt.gene and
                                          self.other_partner in alt.gene]

        if len(complete_match_alterations) > 0:
            return MATCH_LEVEL_COMPLETE, complete_match_alterations

        # Check if only the oncogenic partner has a fusion with a different partner
        different_fusion_alterations = [alt for alt in observed_alterations if
                                        alt.mark_type == self.MARK_TYPE and
                                        self.oncogenic_partner in alt.gene]

        if len(different_fusion_alterations) > 0:
            return MATCH_LEVEL_GENE_AND_TYPE, different_fusion_alterations

        # If we are here this means that the oncogenic partner has an alteration that is not a fusion.
        return MATCH_LEVEL_GENE, any_type_alterations


class BiaMark(GeneMark):
    MARK_TYPE = 'BIA'

    @staticmethod
    def parse(gene, alteration):
        return BiaMark(gene, alteration)

    def __init__(self, gene, expression):
        super().__init__(gene, [MutMark.MARK_TYPE, CnaMark.MARK_TYPE])
        self.expression = expression

    def match(self, observed_alterations):

        # Check gene and type levels
        level, match_alterations = super().match(observed_alterations)

        if level < MATCH_LEVEL_GENE_AND_TYPE:
            return level, match_alterations

        # Don't count the passanger mutations to consider it a complete match
        match_alterations_no_passanger = [a for a in match_alterations if a.mark_type != MutMark.MARK_TYPE or a.driver]

        if len(match_alterations_no_passanger) < 2:
            return level, match_alterations

        return MATCH_LEVEL_COMPLETE, match_alterations
