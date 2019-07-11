import numpy as np
from .random_sampling import binomial_prob_func

def simulate_prob_dens_of_allele_frequency(
    init_parent_prob_dens: list, pop_size: int, gen_num: int):
    """ Returns a table of probability densities for each generation. 
    A probability density is composed of a list of tuples of which the first item
    is a frequency of mutant allele and the second item is a probability at which 
    a population has mutant alleles at the frequency.
    
    Assumptions
    -----------
    - Population size is constant across generations.
    - No new mutation 
    - The probability of choosing an allele is independent of genotype (No selection)
        - so probability of choosing an allele only follows 
        the allele frequency in the parental generation.
    """
    
    prob_dens_table = [init_parent_prob_dens]
    parent_prob_dens = init_parent_prob_dens
    
    # Store probability densities over generations
    for _ in range(gen_num):
        child_prob_dens = prob_dens_of_children_allele_freq(
            parent_prob_dens, pop_size)
        prob_dens_table.append(child_prob_dens)
        # Children grow up to parent. 
        # If one wishes to add natural selection on survival rate, 
        # add a function here.
        parent_prob_dens = child_prob_dens
        
    return prob_dens_table

def prob_dens_of_children_allele_freq(parent_prob_dens: list, pop_size: int):
    """ Returns a list of probability densities for frequencies of mutant alleles 
    in the population of the next generation from a given probability densities in 
    a parental population.
    
    Parameters
    ----------
    parent_prob_dens: list
        a list of probabilities that a population has the "index" number of mutant alleles.
        if [0, 1, 0] is passed, this means in this generation, 1 number of mutants over
        population size 2 at probability 1. Frequencies of mutant alleles are counted 
        from 0 to population size.
    pop_size: int
        The total number of chromosomes in a population.
    """
    assert len(parent_prob_dens) == pop_size+1
    
    child_prob_dens = []

    for parent_derived_count, prob in enumerate(parent_prob_dens):
        tmp_child_prob_dens = prob_dens_of_children_allele_freq_given_parent(
            parent_derived_count, pop_size) * prob

        child_prob_dens.append(tmp_child_prob_dens)

    assert len(child_prob_dens) == pop_size+1
    
    # Sum the probability to get for each allele frequency in children 
    # population across all case of parent allele frequencies
    # Sum function in numpy array allows sum operations for column by column.
    # For example,
    # In [2]: array = np.array([[a+b for a in range(5)] for b in range(0, 40, 10)])
    # In [3]: array
    # Out[3]: 
    # array([[ 0,  1,  2,  3,  4],
    #     [10, 11, 12, 13, 14],
    #     [20, 21, 22, 23, 24],
    #     [30, 31, 32, 33, 34]])
    # In [4]: array.sum(axis=0)
    # Out[4]: array([60, 64, 68, 72, 76])
    child_prob_dens_array = np.array(child_prob_dens)
    result_child_prob_dens = child_prob_dens_array.sum(axis=0)

    # Check if the sum of probabilities is approximately equal to 1
    assert round_num(result_child_prob_dens.sum(), 4) == 1, \
        f"The sum of probabilities is not equal to 1: {result_child_prob_dens.sum()}"

    return result_child_prob_dens

def prob_dens_of_children_allele_freq_given_parent(
    parent_derived_count: int, 
    pop_size: int):
    """ Returns the probability densities of allele frequency in the next 
    (children) population given parental allele frequency. 

    Parameters
    ----------
    parent_derived_count: int
        The number of derived alleles in a parental population. 
        parent_derived_count has to be 0 <= parent_derived_count <= pop_size.
    pop_size: int
        The number of chromosomes in a parental population.

    Assumptions
    -----------
    - The population size is constant across generations from parent 
    to children populations.
    - No mutation.
    - No natural selection
    - Each trial of sampling alleles is independent. The previous result does 
    not affect the probability of sampling in the following trials. So we can
    use binomial probability function.
    """
    # The probability to choose a derived allele from a parental population 
    # at one random sampling
    p = parent_derived_count / pop_size
    child_prob_dens = binomial_prob_func(pop_size, np.arange(pop_size+1), p)
    assert len(child_prob_dens) == pop_size + 1

    return child_prob_dens

def round_num(a, ndigits=2):
    """ Returns rounded value at a given decimal point. """
    n = 10 ** ndigits
    return (a * n * 2 + 1) // 2 / n
