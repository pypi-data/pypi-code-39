from evogen.random_sampling import nCr

def heterozygosity(r:int, pop_size: int):
    """ Returns heterozygosity of a given popualation. 
    This statistics is defined as the probability that two alleles chosen from 
    the given population are not identical by state (e.g. A1 and A2). H is often 
    used for representing this statistics.

    Parameter
    ---------
    r: int
        The number of derived alleles in a population. r has to be 
        0 <= r <= pop_size.
    pop_size: int
        The total number of chromosomes in a population.

    Return
    ------
    hetero: float
        The heterozygosity statistics of the population.
    """
    assert isinstance(r, int), f'Non integer {r} found. r, the count of '\
        'derived alleles, has to be integer.'
    assert isinstance(pop_size, int), f'Non integer {pop_size} found. pop_size,'\
        ' the total number of chromosome in a population has to be integer.'
    # The probability of case 1 where choosing the same allele in this population
    pr1 = r / pop_size # Derived as r * (1 * 1/pop_size)
    # The probability of case 2 where choosing two differenct alleles
    pr2 = nCr(r, 2) * (r-1) / pop_size
    # Because two cases are mutually exclusive, sum together
    hetero = pr1 + pr2
    assert 0 <= hetero or hetero <= 1, f'Wrong calculation of heterozygosity: '\
        '{hetero}'

    return hetero
    
def homozygosity(r:int, pop_size: int):
    """ Returns homozygosiy of a give population.
    This statistics is defined as the probability that two alleles chosen from 
    the given population are identical by state (e.g. A1 and A1). G or F is often 
    used for representing this statistics.

    Parameter
    ---------
    r: int
        The number of derived alleles in a population. r has to be 
        0 <= r <= pop_size.
    pop_size: int
        The total number of chromosomes in a population.

    Return
    ------
    homo: float
        The homozygosity statistics of the population.

    """
    homo = 1 - heterozygosity(r, pop_size)
    assert 0 <= homo or homo <= 1, f'Wrong calculation of homozygosity: '\
        '{homo}'

    return homo
