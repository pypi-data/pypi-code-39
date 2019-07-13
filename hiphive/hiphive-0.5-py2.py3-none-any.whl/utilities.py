"""
This module contains various support/utility functions.
"""

from typing import List
import numpy as np

from ase import Atoms
from ase.calculators.calculator import Calculator
from ase.geometry import find_mic
from ase.geometry import get_distances
from hiphive import ClusterSpace, ForceConstants
from hiphive.force_constant_model import ForceConstantModel
from .io.logging import logger


logger = logger.getChild('utilities')


def get_displacements(atoms: Atoms, atoms_ideal: Atoms) -> np.ndarray:
    """Returns the the smallest possible displacements between a
    displaced configuration relative to an ideal (reference)
    configuration.

    Notes
    -----
    * uses :func:`ase.geometry.find_mic`
    * assumes periodic boundary conditions in all directions

    Parameters
    ----------
    atoms
        configuration with displaced atoms
    atoms_ideal
        ideal configuration relative to which displacements are computed
    """
    if not np.array_equal(atoms.numbers, atoms_ideal.numbers):
        raise ValueError('Atomic numbers do not match.')

    displacements = []
    for pos, ideal_pos in zip(atoms.positions, atoms_ideal.positions):
        v_ij = np.array([pos - ideal_pos])
        displacements.append(find_mic(v_ij, atoms_ideal.cell, pbc=True)[0][0])
    return np.array(displacements)


def prepare_structures(structures: List[Atoms], atoms_ideal: Atoms,
                       calc: Calculator) -> None:
    """Prepares a set of structures in the format suitable for a
    :class:`StructureContainer <hiphive.StructureContainer>`.  This
    includes retrieving the forces using the provided calculator,
    resetting the positions to the ideal configuration, and adding
    arrays with forces and displacements.

    Notes
    -----
    Changes the structures in place.

    Parameters
    ----------
    structures
        list of input configurations
    atoms_ideal
        reference configuration relative to which displacements
        are computed
    calc
        ASE calculator used for computing forces
    """
    for atoms in structures:
        atoms.set_calculator(calc)
        forces = atoms.get_forces()
        displacements = get_displacements(atoms, atoms_ideal)
        atoms.positions = atoms_ideal.get_positions()
        atoms.new_array('forces', forces)
        atoms.new_array('displacements', displacements)


def find_permutation(atoms: Atoms, atoms_ref: Atoms) -> List[int]:
    """ Returns the best permutation of atoms for mapping one
    configuration onto another.

    Parameters
    ----------
    atoms
        configuration to be permuted
    atoms_ref
        configuration onto which to map

    Examples
    --------
    After obtaining the permutation via
    ```
    p = find_permutation(atoms1, atoms2)
    ```
    the reordered structure ``atoms1[p]`` will give the closest match
    to ``atoms2``.
    """
    assert np.linalg.norm(atoms.cell - atoms_ref.cell) < 1e-6
    dist_matrix = get_distances(
        atoms.positions, atoms_ref.positions, cell=atoms_ref.cell, pbc=True)[1]
    permutation = []
    for i in range(len(atoms_ref)):
        dist_row = dist_matrix[:, i]
        permutation.append(np.argmin(dist_row))

    if len(set(permutation)) != len(permutation):
        raise Exception('Duplicates in permutation')
    for i, p in enumerate(permutation):
        if atoms[p].symbol != atoms_ref[i].symbol:
            raise Exception('Matching lattice sites have different occupation')
    return permutation


class Shell:
    """
    Neighbor Shell class

    Parameters
    ----------
    types : list or tuple
        atomic types for neighbor shell
    distance : float
        interatomic distance for neighbor shell
    count : int
        number of pairs in the neighbor shell
    """

    def __init__(self, types, distance, count=0):
        self.types = types
        self.distance = distance
        self.count = count

    def __str__(self):
        s = '{}-{}   distance: {:10.6f}    count: {}'.format(*self.types, self.distance, self.count)
        return s

    __repr__ = __str__


def get_neighbor_shells(atoms: Atoms, cutoff: float, dist_tol: float = 1e-5) -> List[Shell]:
    """ Returns a list of neighbor shells.

    Distances are grouped into shells via the following algorithm:

    1. Find smallest atomic distance `d_min`

    2. Find all pair distances in the range `d_min + 1 * dist_tol`

    3. Construct a shell from these and pop them from distance list

    4. Go to 1.

    Parameters
    ----------
    atoms
        configuration used for finding shells
    cutoff
        exclude neighbor shells which have a distance larger than this value
    dist_tol
        distance tolerance
    """

    # TODO: Remove this once this feature have been in ASE long enough
    try:
        from ase.neighborlist import neighbor_list
    except ImportError:
        raise ImportError('get_neighbor_shells uses new functionality from ASE'
                          ', please update ASE in order to use this function.')

    # get distances
    ijd = neighbor_list('ijd', atoms, cutoff)
    ijd = list(zip(*ijd))
    ijd.sort(key=lambda x: x[2])

    # sort into shells
    symbols = atoms.get_chemical_symbols()
    shells = []
    for i, j, d in ijd:
        types = tuple(sorted([symbols[i], symbols[j]]))
        for shell in shells:
            if abs(d - shell.distance) < dist_tol and types == shell.types:
                shell.count += 1
                break
        else:
            shell = Shell(types, d, 1)
            shells.append(shell)
    shells.sort(key=lambda x: (x.distance, x.types, x.count))

    # warning if two shells are within 2 * tol
    for i, s1 in enumerate(shells):
        for j, s2 in enumerate(shells[i+1:]):
            if s1.types != s2.types:
                continue
            if not s1.distance < s2.distance - 2 * dist_tol:
                logger.warning('Found two shells within 2 * dist_tol')

    return shells


def extract_parameters(fcs: ForceConstants, cs: ClusterSpace):
    """ Extracts parameters from force constants.

    This function can be used to extract parameters to create a
    ForceConstantPotential from a known set of force constants.
    The return values come from NumPy's `lstsq function
    <https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html>`_.

    Parameters
    ----------
    fcs
        force constants
    cs
        cluster space
    """
    fcm = ForceConstantModel(fcs.supercell, cs)
    return np.linalg.lstsq(*fcm.get_fcs_sensing(fcs), rcond=None)[0]
