"""Searching for seeds in input metabolic network.

"""


import predator

NAME = 'Predator plugin'
INPUTS = {'reaction/3', 'reversible/1'}
OUTPUTS = {'seed/1'}
TAGS = 'metabolic network',

ASP_EXPAND_NETWORK = r"""
reactant(X,R) :- reaction(X,R,_).
product(Y,R) :- reaction(_,R,Y).
reaction(R) :- reaction(_,R,_).
"""


def run_on(context:str, *, pareto:bool=False, targets:str='', optimal:bool=False, targets_are_forbidden:bool=True):
    """
    pareto -- if set, explore the pareto front
    targets -- if given, targets that seeds must activate (instead of all)
    optimal -- if set, only output optimal solution (in number of seeds)
    """

    targets = {f'"{t}"' for t in targets.split(',') if t}
    context = predator.quoted_data(context + ASP_EXPAND_NETWORK)
    forbidden_seeds = targets if targets_are_forbidden else set()
    solutions = predator.search_seeds(context, explore_pareto=pareto, forbidden_seeds=forbidden_seeds, targets=targets,
                                      compute_optimal_solutions=optimal)
    solutions = tuple(solutions)
    repr_solutions = ('seed(' + ';'.join(seeds) + ')' for seeds in solutions)
    repr_solutions = ' ; '.join(repr_solutions)
    return repr_solutions + '.' if repr_solutions else ''
