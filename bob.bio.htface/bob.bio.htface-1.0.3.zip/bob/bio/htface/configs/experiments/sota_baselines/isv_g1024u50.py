#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>

import bob.bio.gmm


algorithm = bob.bio.gmm.algorithm.ISV(subspace_dimension_of_u=160, \
                                      number_of_gaussians = 1024, \
                                      gmm_training_iterations = 10,\
                                      update_weights = False,update_variances = False)
