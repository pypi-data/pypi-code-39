"""A utility module."""
from equilibrator_api import ccache
from equilibrator_api.phased_reaction import PhasedReaction


def parse_reaction_formula(formula: str) -> PhasedReaction:
    """Parse reaction text using exact match.

    :param formula: a string containing the reaction formula
    :return: a Reaction object
    """
    return PhasedReaction.parse_formula(ccache.get_compound, formula)
