# kiwano.py
# Author: Jacob Schreiber <jmschreiber91@gmail.com>

import numpy
from apricot import FacilityLocationSelection

def kiwano(similarities, names, verbose=False, initial_subset=None):
	"""Kiwano will take in a similarity matrix and output an ordering.

	Kiwano is the implementation of a procedure that can determine the
	order that experiments should be performed based on a submodular
	optimization procedure applied to imputed versions of those
	experiments. Thus, the input to this procedure is a calculated
	similarity matrix, and the output is an ordering over those
	experiments. The similarity matrix must be symmetric and
	non-negative, with higher values indicating higher similarity.
	We anticipate that these similarities are squared correlation
	valus, but they can be any similarity metric that follows
	those properties. The ranking procedure involves optimizing a
	facility location function.

	This is an implementation of the code for the paper

	Prioritizing transcriptomic and epigenomic experiments by using 
	an optimization strategy that leverages imputed data
	Jacob Schreiber, Jeffrey Bilmes, William Noble
	"""

	if not isinstance(similarities, numpy.ndarray):
		raise ValueError("Similarities must be a 2D symmetric numpy array.")
	if numpy.any(similarities.T != similarities):
		raise ValueError("Similarities must be a 2D symmetric numpy array.")
	if similarities.ndim != 2:
		raise ValueError("Similarities must be a 2D symmetric numpy array")

	if len(similarities) != len(names):
		raise ValueError("The length of similarities must be the same as the length of names")

	n = int(initial_subset.sum()) if initial_subset is not None else 0
	selector = FacilityLocationSelection(len(names) - n, pairwise_func='precomputed', 
		verbose=verbose, initial_subset=initial_subset)
	selector.fit(similarities)
	return names[selector.ranking], selector.ranking
