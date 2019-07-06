"""
-------------------------------------------------------------------------------

Implementation of the theory of consistently oriented eigenvectors.

This is a reference implementation against which performant implementations
can be compared.

-------------------------------------------------------------------------------
"""


import numpy as np

# define API exposure
__all__ = ['orient_eigenvectors', 'generate_oriented_eigenvectors']


"""
-------------------------------------------------------------------------------
Orientation code
-------------------------------------------------------------------------------
"""


# noinspection SpellCheckingInspection,PyPep8Naming
def orient_eigenvectors(V: np.ndarray, E: np.ndarray):
    """
    Finds vector `s` such that `Vor = V diag(s)`, where Vor is an oriented
    basis.

    Parameters
    ----------
    V: np.ndarray
        Eigenvector matrix with columns vectors
    E: np.ndarray
        Eigenvalue matrix conformant to V

    Returns
    -------
    Vor: np.ndarray
        Eigenvector matrix cast into an oriented basis, see Note 1.

    Eor: np.ndarray
        Eigenvalue matrix conformant to Vor, see Note 2.

    sign_flip_vector: np.ndarray
        Vector of signs that was applied to (sorted) `V` such that `Vor` is
        oriented.

    theta_matrix: np.ndarray
        upper-trianglar matrix of angles embedded in `Vor` with respect to the
        constituent basis in which (sorted) `V` is matrialized.

    sort_indices: np.ndarray
        Permutation vector such that Vsort = V[:, sort_indices].

    Notes
    -----

    1. The columns of `Vor` are ordered such that their associated eigenvalues
       are sorted in descending order of absolute value. That the absolute
       value is taken on the eigenvalues is to treat the general case of an
       input Hermitian matrix. For data analysis, SVD will generally yield a
       positive (semi)definite eigensystem, so negative eigenvalues are not
       attained.

    2. The diagonal entries of `Eor` are ordered in descending absolute value
       of the input eigenvalue matrix `E`.

    """

    # To begin, sort (V, E) by descending absolute-value of eigenvalues in E.
    # Note that Vsort and Esort are copies of V, E.
    Vsort, Esort, sort_indices = sort_eigenvectors(V, E)

    # make a copy for local work
    Vwork = Vsort.copy()

    # pick off full dimension
    full_dim = Vwork.shape[0]

    # initialize storage matrix for angles
    angles_matrix = np.zeros(Vwork.shape)

    # initialize sign-flip vectory
    sign_flip_vector = np.zeros(full_dim)

    # create scan array of cursors as they range [0: full-dim)
    cursors = np.arange(full_dim)

    # iterate from the full dimension down to R^1
    for cursor in cursors:

        # eval sign flip
        sign_flip_vector[cursor] = 1. if Vwork[cursor, cursor] >= 0. else -1.

        # apply the flip to the cursor column in Vsort
        Vwork[:, cursor] *= sign_flip_vector[cursor]

        # reduce the sub-space dimension by 1 using a rotation matrix
        Vwork, angles_col = reduce_dimension_by_one(full_dim, cursor, Vwork)

        # persist the angles in an upper triangular matrix
        angles_matrix[cursor, :] = angles_col.T

    # calculate Vor, the right-handed basis for Vsort
    Vor = Vsort.dot(np.diag(sign_flip_vector))

    # return work performed by this function
    return Vor, Esort, sign_flip_vector, angles_matrix, sort_indices


# noinspection SpellCheckingInspection,PyPep8Naming
def reduce_dimension_by_one(full_dim: int,
                            cursor: int,
                            Vwork: np.ndarray):
    """
    Transforms `Vwork` such that a 1 appears on the cursor pivot and the lower-
    right sub-space is, consequently, rotated.

    Parameters
    ----------
    full_dim: int
        The dimension of the full space, quoted in base(1) style.
    cursor: int
        Pointer to the lower right subspace embedded in R^full_dim, quoted in
        base(0) style.
    Vwork: np.ndarray
        Current workspace matrix such that the upper-left pivots outside of
        the current subspace are 1 while the lower-right subspace itself remains
        (almost surely) unaligned to the constituent basis.

    Returns
    -------
    Vwork: np.ndarray
        Updated Vwork matrix.
    angles_col: np.ndarray
        Givens rotation angles applied to input Vwork.

    Notes
    -----
    The goal is to apply rotation matrix R.T such that the current sub-space
    dimension of Vwork is reduced by one. In block form,

            -            -     -            -
            | 1          |     | 1          |
     R.T x  |    *  *  * |  =  |    1       |
            |    *  *  * |     |       *  * |
            |    *  *  * |     |       *  * |
            -            -     -            -
    """

    # solve for rotation angles
    angles_col = solve_rotation_angles_in_subdimension(
        full_dim, cursor, Vwork[:, cursor])

    # construct subspace rotation matrix via a cascade of Givens rotations
    R = construct_subspace_rotation_matrix(
        full_dim, cursor, angles_col)

    # Apply R.T to reduce the non-identity subspace by one dimension.
    Vwork = R.T.dot(Vwork)

    # return
    return Vwork, angles_col


# noinspection SpellCheckingInspection,PyPep8Naming
def solve_rotation_angles_in_subdimension(full_dim: int,
                                          cursor: int,
                                          Vcol: np.ndarray) -> np.ndarray:
    """
    Solves for embedded angles necessary to rotate a unit vector pointing
    along the `cursor` axis, within `full_dim`, into the input `Vcol` vector.

    Recursive solution strategy to calculate rotation angles required to
    rotate the principal axis of a sub dimension onto an axis of its
    corresponding constituent basis.

    Parameters
    ----------
    full_dim: int
        The dimension of the full space, quoted in base(1) style.
    cursor: int
        Pointer to the lower right subspace embedded in R^full_dim, quoted in
        base(0) style.
    Vcol: np.ndarray
        Column in `full_dim` whose elements at and above `cursor` will be
        matched by the rotation sequence.

    Returns
    -------
    np.ndarray
        Returns `angles_col` sized to the full dimension.

    Notes
    -----
    The recursion in this function solves for angles theta_2, theta_3, ...
    such that

        -          -     -    -
        | c2 c3 c4 |     | v1 |
        | s2 c3 c4 |  =  | v2 |,  {s|c}k = {sin|cos}(theta_k)
        |   s3 c4  |     | v3 |
        |    s4    |     | v4 |
        -          -     -    -

    In particular, the arcsin recursion equations are implemented because
    they have better edge-case properties than the arctan recursion.
    """

    # create scan array of sub-cursors as they range [cursor + 1: full-dim)
    sub_cursors = np.arange(cursor + 1, full_dim)

    # prepare for the recursion
    angles_work = np.zeros(full_dim + 1)
    r = 1.

    # iterate over rows in subspace to calculate full 2-pi angles
    for sub_cursor in sub_cursors[::-1]:

        y = Vcol[sub_cursor]
        r *= np.cos(angles_work[sub_cursor + 1])

        angles_work[sub_cursor] = np.arcsin(y / r) if r != 0.0 else 0.

    # return work angles sized to full_dim
    return angles_work[:full_dim]


# noinspection SpellCheckingInspection,PyPep8Naming
def construct_subspace_rotation_matrix(full_dim: int,
                                       cursor: int,
                                       angles_col: np.ndarray) -> np.ndarray:
    """
    Constructs a rotation matrix that spans the subspace indicated by the
    `cursor` by cascading a sequence of Givens rotations.

    Parameters
    ----------
    full_dim: int
        The dimension of the full space, quoted in base(1) style.
    cursor: int
        Pointer to the lower right subspace embedded in R^full_dim, quoted in
        base(0) style.
    angles_col: np.ndarray
        Rotation angles in current subspace. This is a view on `angles_matrix`
        from the outer scope.

    Returns
    -------
    R: np.ndarray
        Rotation matrix `R` being a cascade of Givens rotations.

    Notes
    -----
    This function constructs a cascade of Givens rotations in the following way:

    `full_dim` = 4, `cursor` = 1

    -            --            -     -            -
    | 1          || 1          |     | 1          |
    |   c  -s    ||   c     -s |  =  |    *  *  * |
    |   s   c    ||      1     |     |    *  *  * |
    |          1 ||   s      c |     |    *  *  * |
    -            --            -     -            -
          ^              ^
      theta_2,3     theta_2,4               R

    """

    # initialize R
    R = np.eye(full_dim)

    # create scan array of sub-cursors as they range [cursor + 1: full-dim)
    sub_cursors = np.arange(cursor + 1, full_dim)

    # iterate over angles (reverse order), build a Givens matrix, and apply
    for sub_cursor in sub_cursors[::-1]:

        # noinspection PyUnresolvedReferences
        R = make_givens_rotation_matrix_in_subspace(full_dim,
                                                    cursor,
                                                    sub_cursor,
                                                    angles_col[sub_cursor]) \
            .dot(R)

    # return the rotation matrix
    return R


# noinspection SpellCheckingInspection,PyPep8Naming
def make_givens_rotation_matrix_in_subspace(full_dim: int,
                                            cursor: int,
                                            sub_cursor: int,
                                            theta: float) -> np.ndarray:
    """
    Makes a Givens rotation matrix.

    Parameters
    ----------
    full_dim: int
        The dimension of the full space, quoted in base(1) style.
    cursor: int
        Pointer to the lower right subspace embedded in R^full_dim, quoted in
        base(0) style.
    sub_cursor: int
        Pointer to the pivot position of the lower cos(.) entry.
    theta: float
        Rotation angle.

    Returns
    -------
    A Givens matrix, such as

            -          -
            | 1        |
        R = |   c   -s |
            |     1    |
            |   s    c |
            -          -
                ^    ^
                |    |
             cursor  |
                sub-cursor

    where, in this example, full_dim = 4.

    Notes
    -----
    It is up to the caller to validate the `cursor` and `sub_cursor` indexing
    into R.
    """

    # eval trig
    c = np.cos(theta)
    s = np.sin(theta)

    # construct Givens rotation matrix
    R = np.eye(full_dim)

    R[cursor, cursor] = c
    R[cursor, sub_cursor] = -s
    R[sub_cursor, cursor] = s
    R[sub_cursor, sub_cursor] = c

    # return
    return R


# noinspection SpellCheckingInspection,PyPep8Naming
def sort_eigenvectors(V, E):
    """
    Sorts the columns of `V` such that their corresponding eigenvalues appear
    in decreasing order of absolute values.

    Parameters
    ----------
    V: ndarray
        Original (n x n) eigenvector matrix.
    E: ndarray
        Original (n x n) eigenvalue matrix.

    Returns
    -------
    sort_indices: ndarray
        result of argsort on abs(diag(E)), (n x 1).
    Vsort: ndarray
        V[:, sort_indices] (n x n) -- note: a copy.
    Esort: ndarray
        E[:, sort_indices] (n x n) -- note: a copy.

    """

    # extract diagonal of E
    e_vector = np.diag(E)

    # argsort the absolute values of e_vector in descending order
    sort_indices = np.argsort(np.fabs(e_vector))[::-1]

    # sort V and E based on sort_indices
    Vsort = V[:, sort_indices]
    Esort = np.diag(e_vector[sort_indices])

    # return
    return Vsort, Esort, sort_indices


"""
-------------------------------------------------------------------------------
Rotation generator code
-------------------------------------------------------------------------------
"""


# noinspection SpellCheckingInspection,PyPep8Naming
def generate_oriented_eigenvectors(angles_matrix: np.ndarray,
                                   kth_eigenvector=None) -> np.ndarray:
    """
    The call `orient_eigenvectors` consumes an eigenvector matrix `V` that is
    not necessarily oriented and returns `Vor`, its oriented counterpart.
    The `orient_eigenvectors` call also returns `angles_matrix`.

    This function consumes `angles_matrix` (instead of `V`) to produce `Vor`,
    the oriented eigenvector matrix.

    Recall that

    (1)    Vor = V S = R

    where `S` is a diagonal matrix with +/- 1 entries, and `R` is a rotation
    matrix. `orient_eigenvectors` computes `V S` while this function computes
    `R`.

    For a constituent basis I(n), the identity matrix, `R` rotates `I` into
    `Vor`,

    (2)    Vor = R I.

    In this way we identify `R` with the rotation that brings `I` into align-
    ment with `Vor`.

    Rotation matrix `R` itself is a cascade of rotations, one for each eigen-
    vector,

    (3)    R = R_1 R_2 ... R_n .

    Moreover, rotation R_k is itself a cascade of elemental Givens rotations.
    In R^4, the R_1 rotation is

    (4)    R_1(theta_(1,2), theta_(1,3), theta_(1,4)) =
                R_(1,2)(theta_(1,2))
                    x R_(1,3)(theta_(1,3))
                        x R_(1,4)(theta_(1,4)).

    The angles are read from `angles_matrix` such that

              -                  -
              | 0  t12  t13  t14 |  <-- row for R_1
    ang_mtx = |    0    t23  t24 |  <-- row for R_2
              |    *    0    t34 |   ..
              |    *    *    0   |
              -                  -

    Parameters
    ----------
    angles_matrix: ndarray
        Upper-triangular (n x n) matrix of angles.
    kth_eigenvector: int
        Default value is None, otherwise a base(1) indicator of the eigenvector
        to rotate into its constituent axis.

    Returns
    -------
    R: ndarray
        Resultant rotation matrix.

    Notes
    -----
    The full dimension of the space is inferred from the dimension of
    `angles_matrix`. Given a `full_dim`, the rotation matrix that corresponds
    to the kth eigenvector is constructed from elementary Givens rotations.
    In R^4, the rotation matrix for the 1st eigenvector is

    (1) R_1(theta_(1,2), theta_(1,3), theta_(1,4)) =
            R_(1,2)(theta_(1,2)) x R_(1,3)(theta_(1,3)) x R_(1,4)(theta_(1,4)).

    The rotation matrix for the full eigenbasis in R^4 is

    (2) R = R_1 R_2 R_3 R_4.

    """

    # initialize
    full_dim = angles_matrix.shape[0]

    # evaluate (3) from the notes above
    if kth_eigenvector is not None:

        # conform to function interface
        cursor = kth_eigenvector - 1
        angles_col = angles_matrix[cursor, :].T

        R = construct_subspace_rotation_matrix(full_dim, cursor, angles_col)

    # evaluate (4) from the notes above
    else:

        # initialize
        R = np.eye(full_dim)

        # create scan array across all dimensions
        cursors = np.arange(full_dim)

        # iterate over cursors
        for cursor in cursors:

            # conform to function interface
            angles_col = angles_matrix[cursor, :].T

            # build R_k.dot(R_(k+1))
            R = R.dot(
                construct_subspace_rotation_matrix(full_dim,
                                                   cursor,
                                                   angles_col)
            )

    # return
    return R
