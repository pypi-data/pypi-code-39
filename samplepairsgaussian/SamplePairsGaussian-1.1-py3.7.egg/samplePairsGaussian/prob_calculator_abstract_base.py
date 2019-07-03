from abc import ABC, abstractmethod

import numpy as np
import logging
import sys

class ProbCalculatorAbstractBase(ABC):
    """Calculates distances and probabilities for a set of particles.

    Attributes:
    posns (np.array([[float]])): particle positions. First axis are particles, seconds are coordinates in n-dimensional space
    n (int): number of particles

    idxs_possible_first_particle (np.array([int])): idx of the first particle. Only unique combinations together with idxs_2.
    idxs_possible_second_particle (np.array([int])): idx of the second particle. Only unique combinations together with idxs_1.
    probs (np.array([float])): probs of each pair of particles.
    no_idx_pairs_possible (int): # idx pairs possible
    are_probs_normalized (bool): whether the probabilities are normalized.
    max_prob (float): the maximum probability value, useful for rejection sampling

    Private attributes:
    _logger (logger): logging
    """



    def __init__(self, posns, std_dev, std_dev_clip_mult=3.0):
        """Constructor.

        Args:
        posns (np.array([[float]])): particle positions. First axis are particles, seconds are coordinates in n-dimensional space
        std_dev (float): standard deviation
        std_dev_clip_mult (float): multiplier for the standard deviation cutoff, else None
        """

        # Setup the logger
        self._logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

        # Level of logging to display
        self._logger.setLevel(logging.ERROR)

        # vars
        self._posns = posns
        self._n = len(self._posns)
        self._std_dev = std_dev
        self._std_dev_clip_mult = std_dev_clip_mult

        # Initialize all manner of other properties for possible later use
        self._idxs_possible_first_particle = np.array([]).astype(int)
        self._idxs_possible_second_particle = np.array([]).astype(int)
        self._probs = np.array([]).astype(float)
        self._max_prob = None
        self._norm = None
        self._no_idx_pairs_possible = 0



    def set_logging_level(self, level):
        """Sets the logging level

        Args:
        level (logging): logging level
        """
        self._logger.setLevel(level)



    # Various getters
    @property
    def posns(self):
        return self._posns

    @property
    def n(self):
        return self._n

    @property
    def idxs_possible_first_particle(self):
        return self._idxs_possible_first_particle

    @property
    def idxs_possible_second_particle(self):
        return self._idxs_possible_second_particle

    @property
    def probs(self):
        return self._probs

    @property
    def are_probs_normalized(self):
        return self._are_probs_normalized

    @property
    def max_prob(self):
        return self._max_prob

    @property
    def norm(self):
        return self._norm

    @property
    def no_idx_pairs_possible(self):
        return self._no_idx_pairs_possible

    @property
    def std_dev(self):
        return self._std_dev

    @property
    def std_dev_clip_mult(self):
        return self._std_dev_clip_mult
