# coding: utf-8

#-------------------------------------------------------------------------------
# Copyright (C) 2017-2018 Maximilian Stahlberg
#
# This file is part of PICOS.
#
# PICOS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PICOS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This file implements the MOSEK solver through its high level Fusion API.
# The Fusion API is currently much slower than MOSEK's low level Python API.
# If this changes in the future, the Fusion API would be the prefered interface.
#-------------------------------------------------------------------------------

import sys
import cvxopt

from ..expressions import *
from ..constraints import *

from .solver import *

class MOSEKFusionSolver(Solver):
    @classmethod
    def test_availability(cls):
        import mosek.fusion

    @classmethod
    def supports_integer(cls):
        return True

    @classmethod
    def supported_objectives(cls):
        yield AffinExp

    @classmethod
    def supported_constraints(cls):
        yield AffineConstraint
        yield SOCConstraint
        yield RSOCConstraint
        yield LMIConstraint

    @classmethod
    def support_level(cls, problem):
        # MOSEK does not support mixed integer SDPs.
        if not problem.is_continuous() \
            and any([True for constraint in problem.constraints
                if constraint.__class__ is LMIConstraint]):
            return SUPPORT_LEVEL_NONE

        return super(MOSEKFusionSolver, cls).support_level(problem)

    def __init__(self, problem):
        super(MOSEKFusionSolver, self).__init__(
            problem, "MOSEK (Fusion)", "MOSEK via Fusion API")

        # Maps PICOS variables to MOSEK variables and vice versa.
        self.knownVariables = {}

        # Maps PICOS constraints to MOSEK constraints and vice versa.
        self.knownConstraints = {}

    def __del__(self):
        if self.int is not None:
            self.int.dispose()

    def reset_problem(self):
        if self.int is not None:
            self.int.dispose()
        self.int = None
        self.knownVariables.clear()
        self.knownConstraints.clear()

    @classmethod
    def _get_major_version(cls):
        if not hasattr(cls, "mosekVersion"):
            import mosek
            cls.mosekVersion = mosek.Env.getversion()

        return cls.mosekVersion[0]

    ver = property(lambda self: self.__class__._get_major_version())
    """The major version of the available MOSEK library."""

    @classmethod
    def _mosek_sparse_triple(cls, I, J, V):
        """Transforms a sparse triple (e.g. from CVXOPT) for use with MOSEK."""
        if cls._get_major_version() >= 9:
            IJV = list(IJV for IJV in zip(I, J, V) if IJV[2] != 0)
            I, J, V = (list(X) for X in zip(*IJV)) if IJV else ([], [], [])
        else:
            I = list(I) if not isinstance(I, list) else I
            J = list(J) if not isinstance(J, list) else J
            V = list(V) if not isinstance(V, list) else V

        return I, J, V

    @classmethod
    def _matrix_cvx2msk(cls, cvxoptMatrix):
        """Transforms a CVXOPT (sparse) matrix into a MOSEK (sparse) matrix."""
        import mosek.fusion as msk

        M = cvxoptMatrix
        n, m = M.size

        if type(M) is cvxopt.spmatrix:
            return msk.Matrix.sparse(
                n, m, *cls._mosek_sparse_triple(M.I, M.J, M.V))
        elif type(M) is cvxopt.matrix:
            return msk.Matrix.dense(n, m, list(M.T))
        else:
            raise ValueError("Argument must be a CVXOPT matrix.")

    @classmethod
    def _mosek_vstack(cls, *expressions):
        """
        This is a wrapper around MOSEK's :func:`vstack
        <mosek.fusion.Expr.vstack>` function that silences a FutureWarning.
        """
        import mosek.fusion as msk

        if cls._get_major_version() >= 9:
            return msk.Expr.vstack(*expressions)
        else:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", FutureWarning)
                return msk.Expr.vstack(*expressions)

    def _affinexp_pic2msk(self, picosExpression):
        """
        Transforms a PICOS affine expression into a MOSEK expression, subject to
        the requirement that all contained variables are known to MOSEK.
        """
        import mosek.fusion as msk
        if not isinstance (picosExpression, AffinExp):
            raise ValueError("Argument must be an AffinExp.")

        vectorShape = [len(picosExpression), 1]
        targetShape = list(picosExpression.size)

        if self.ver < 9:
            vectorShape = msk.Set.make(vectorShape)
            targetShape = msk.Set.make(targetShape)

        # Convert linear part of expression.
        firstSummand = True
        for picosVar, factor in picosExpression.factors.items():
            mosekVar = self.knownVariables[picosVar]

            summand = msk.Expr.mul(self._matrix_cvx2msk(factor), mosekVar)
            if firstSummand:
                mosekExpression = summand
                firstSummand = False
            else:
                mosekExpression = msk.Expr.add(mosekExpression, summand)

        # Convert constant term of expression.
        if picosExpression.constant is not None:
            mosekConstant = msk.Expr.constTerm(
                self._matrix_cvx2msk(picosExpression.constant))

            if firstSummand:
                mosekExpression = mosekConstant
            else:
                mosekExpression = msk.Expr.add(mosekExpression, mosekConstant)
        elif firstSummand:
            mosekExpression = Expr.zeros(vectorShape)

        # Restore the expression's original shape.
        # NOTE: Transposition due to differing major orders.
        mosekExpression = msk.Expr.reshape(
            msk.Expr.transpose(mosekExpression), targetShape)

        if self._debug():
            self._debug(
                "Affine expression converted: {} → {}".format(
                repr(picosExpression), mosekExpression.toString()))

        return mosekExpression

    @classmethod
    def _bounds_pic2msk(cls, picosVar, fixMOSEK9 = False):
        """
        Transforms the bounds of a PICOS variable into two MOSEK matrices (or
        scalars, for homogenous bounds).
        """
        import mosek.fusion as msk

        lowerRows, upperRows = [], []
        lowerBnds, upperBnds = [], []

        # Construct a sparse matrix representation of the bounds.
        for localIndex, (lower, upper) in picosVar.bnd.items():
            row = localIndex
            col = 0

            if lower is not None:
                lowerRows.append(localIndex)
                lowerBnds.append(lower)
            elif fixMOSEK9:
                lowerRows.append(localIndex)
                lowerBnds.append(-1e20)

            if upper is not None:
                upperRows.append(localIndex)
                upperBnds.append(upper)
            elif fixMOSEK9:
                upperRows.append(localIndex)
                upperBnds.append(1e20)

        lowerCols, upperCols = [0]*len(lowerBnds), [0]*len(upperBnds)

        # Construct MOSEK matrices from the sparse representation.
        mosekBounds = [None, None]
        for side, rows, cols, bounds in (
                (0, lowerRows, lowerCols, lowerBnds),
                (1, upperRows, upperCols, upperBnds)):
            if len(bounds) == picosVar.dim and len(set(bounds)) == 1:
                 mosekBounds[side] = bounds[0]
            elif bounds:
                # NOTE: Zero values intentionally not removed as they represent
                #       partial unboundedness.
                mosekBounds[side] = msk.Matrix.sparse(
                    picosVar.dim, 1, rows, cols, bounds)

        return mosekBounds

    def _import_variable(self, picosVar):
        import mosek.fusion as msk

        varType = picosVar.vtype
        shape   = [picosVar.dim, 1]

        # Import variable bounds.
        if varType != "binary":
            # Retrieve lower and upper bounds.
            lower, upper = self._bounds_pic2msk(picosVar)

            # Convert bounds to a domain.
            if lower is None and upper is None:
                domain = msk.Domain.unbounded()
            elif lower is not None and upper is None:
                domain = msk.Domain.greaterThan(lower)
            elif lower is None and upper is not None:
                domain = msk.Domain.lessThan(upper)
            elif lower is not None and upper is not None:
                if lower == upper:
                    domain = msk.Domain.equalsTo(lower)
                elif self.ver >= 9:
                    # HACK: MOSEK 9 does not accept sparse (partial) range
                    #       domains anymore. The workaround triggers a MOSEK
                    #       warning, but there is no other way to pass such
                    #       variable bounds directly.
                    if isinstance(lower, msk.Matrix) \
                    or isinstance(upper, msk.Matrix):
                        lower, upper = self._bounds_pic2msk(picosVar, True)
                        if isinstance(lower, msk.Matrix):
                            lower = lower.getDataAsArray()
                        if isinstance(upper, msk.Matrix):
                            upper = upper.getDataAsArray()

                    domain = msk.Domain.inRange(lower, upper, shape)
                else:
                    domain = msk.Domain.inRange(lower, upper)

        # Refine the domain with the variable's type.
        if varType == "binary":
            domain = msk.Domain.binary()
        elif varType == "integer":
            domain = msk.Domain.integral(domain)
        elif varType not in ("continuous", "symmetric"):
            raise NotImplementedError(
                "Variables of type '{}' are not supported with MOSEK."
                .format(varType))

        # Create the MOSEK variable.
        mosekVar = self.int.variable(picosVar.name, shape, domain)

        # Map the PICOS variable to the MOSEK variable and vice versa.
        self.knownVariables[picosVar] = mosekVar
        self.knownVariables[mosekVar] = picosVar

        if self._debug(): # Formatting can be expensive.
            self._debug("Variable imported: {} → {}"
                .format(picosVar, " ".join(mosekVar.toString().split())))

    # TODO: This needs a test.
    def _import_variable_values(self, integralOnly = False):
        for picosVar in self.ext.variables.values():
            if integralOnly and picosVar.vtype not in ("binary", "integer"):
                continue
            if picosVar.is_valued():
                mosekVar = self.knownVariables[picosVar]
                mosekVar.setLevel(list(picosVar.value))

    def _import_linear_constraint(self, picosCon):
        import mosek.fusion as msk
        assert isinstance(picosCon, AffineConstraint)

        # Separate constraint into a linear function and a constant.
        linear, bound = picosCon.bounded_linear_form()

        # Rewrite constraint in MOSEK types: The linear function is represented
        # as a MOSEK expression while the constant term becomes a MOSEK domain.
        linear = self._affinexp_pic2msk(linear[:])
        bound  = self._matrix_cvx2msk(bound.constant)

        if picosCon.is_increasing():
            domain = msk.Domain.lessThan(bound)
        elif picosCon.is_decreasing():
            domain = msk.Domain.greaterThan(bound)
        elif picosCon.is_equality():
            domain = msk.Domain.equalsTo(bound)
        else:
            assert False, "Unexpected constraint relation."

        # Import the constraint.
        if picosCon.name is None:
            return self.int.constraint(linear, domain)
        else:
            return self.int.constraint(picosCon.name, linear, domain)

    def _import_socone_constraint(self, picosCon):
        import mosek.fusion as msk
        assert isinstance(picosCon, SOCConstraint)

        coneElement = self._mosek_vstack(
            msk.Expr.flatten(self._affinexp_pic2msk(picosCon.ub)),
            msk.Expr.flatten(self._affinexp_pic2msk(picosCon.ne)))

        # TODO: Remove zeros from coneElement[1:].

        return self.int.constraint(coneElement, msk.Domain.inQCone())

    def _import_rscone_constraint(self, picosCon):
        import mosek.fusion as msk
        assert isinstance(picosCon, RSOCConstraint)

        # MOSEK handles the vector [x₁; x₂; x₃] as input for a constraint of the
        # form ‖x₃‖² ≤ 2x₁x₂ whereas PICOS handles the expressions e₁, e₂ and e₃
        # for a constraint of the form ‖e₁‖² ≤ e₂e₃.
        # Neutralize MOSEK's additional factor of two by scaling e₂ and e₃ by
        # sqrt(0.5) each to obtain x₁ and x₂ respectively.
        scale = 0.5**0.5
        coneElement = self._mosek_vstack(
            msk.Expr.flatten(self._affinexp_pic2msk(scale * picosCon.ub1)),
            msk.Expr.flatten(self._affinexp_pic2msk(scale * picosCon.ub2)),
            msk.Expr.flatten(self._affinexp_pic2msk(picosCon.ne)))

        # TODO: Remove zeros from coneElement[2:].

        return self.int.constraint(coneElement, msk.Domain.inRotatedQCone())

    def _import_sdp_constraint(self, picosCon):
        import mosek.fusion as msk
        assert isinstance(picosCon, LMIConstraint)

        semiDefMatrix = self._affinexp_pic2msk(picosCon.psd)

        return self.int.constraint(semiDefMatrix, msk.Domain.inPSDCone())

    def _import_constraint(self, picosCon):
        import mosek.fusion as msk

        # HACK: Work around faulty MOSEK warnings (warning 705).
        import os
        with open(os.devnull, "w") as devnull:
            self.int.setLogHandler(devnull)

            if isinstance(picosCon, AffineConstraint):
                mosekCon = self._import_linear_constraint(picosCon)
            elif isinstance(picosCon, SOCConstraint):
                mosekCon = self._import_socone_constraint(picosCon)
            elif isinstance(picosCon, RSOCConstraint):
                mosekCon = self._import_rscone_constraint(picosCon)
            elif isinstance(picosCon, LMIConstraint):
                mosekCon = self._import_sdp_constraint(picosCon)
            else:
                assert False, "Constraint type not supported."

            self.int.setLogHandler(sys.stdout)

        # Map the PICOS constraint to the MOSEK constraint and vice versa.
        self.knownConstraints[picosCon] = mosekCon
        self.knownConstraints[mosekCon] = picosCon

        if self._debug(): # Formatting can be expensive.
            self._debug("Constraint imported: {} → {}".format(picosCon,
                " ".join(mosekCon.toString().split()) if not isinstance(
                mosekCon, msk.PSDConstraint) else mosekCon))

    def _import_objective(self):
        import mosek.fusion as msk

        picosSense, picosObjective = self.ext.objective

        if picosSense == "find":
            mosekSense = msk.ObjectiveSense.Minimize
            mosekObjective = msk.Expr.constTerm(0)
        elif picosSense == "min":
            mosekSense = msk.ObjectiveSense.Minimize
            mosekObjective = self._affinexp_pic2msk(picosObjective)
        elif picosSense == "max":
            mosekSense = msk.ObjectiveSense.Maximize
            mosekObjective = self._affinexp_pic2msk(picosObjective)
        else:
            raise NotImplementedError("Objective '{0}' not supported by MOSEK."
                .format(picosSense))

        self.int.objective(mosekSense, mosekObjective)

        if self._debug(): # Formatting can be expensive.
            self._debug(
                "Objective imported: {} {} → {} {}".format(
                picosSense, picosObjective, mosekSense,
                " ".join(mosekObjective.toString().split())))

    def _import_problem(self):
        import mosek.fusion as msk

        # Create a problem instance.
        self.int = msk.Model()
        self.int.setLogHandler(sys.stdout)

        # Import variables.
        for variable in self.ext.variables.values():
            self._import_variable(variable)

        # Import constraints.
        for constraint in self.ext.constraints:
            self._import_constraint(constraint)

        # Set objective.
        self._import_objective()

    def _update_problem(self):
        for oldConstraint in self._removed_constraints():
            raise ProblemUpdateError(
                "MOSEK does not support removal of constraints.")

        for oldVariable in self._removed_variables():
            raise ProblemUpdateError(
                "MOSEK does not support removal of variables.")

        for newVariable in self._new_variables():
            self._import_variable(newVariable)

        for newConstraint in self._new_constraints():
            self._import_constraint(newConstraint)

        if self._objective_has_changed():
            self._import_objective()

    def _solve(self):
        import mosek.fusion as msk
        from mosek import objsense

        # MOSEK 8 has additional parameters and status codes.
        mosek8 = self.ver < 9

        # Reset options.
        # HACK: This is a direct access to MOSEK's internal Task object, which
        #       is necessary as the Fusion API has no call to reset options.
        # TODO: As soon as the Fusion API offers option reset, use it instead.
        self.int.getTask().setdefaults()

        # Handle "verbose" option.
        self.int.setSolverParam("log", max(0, self.verbosity()))

        # Handle "tol" option.
        # Prefixes:
        # - "" is for linear problems.
        # - "Co" is for conic problems.
        # - "Qo" is for quadratic problems (MOSEK < 9).
        # Suffixes:
        # - "PFeas" is the primal feasibility tolerance.
        # - "DFeas" is the dual feasibility tolerance.
        # - "MuRed" is the relative complementary gap feasibility tolerance.
        # - "RelGap" is the relative gap termination tolerance.
        if self.ext.options["tol"] is not None:
            for prefix in ("", "Co") + (("Qo",) if mosek8 else ()):
                for suffix in ("Pfeas", "Dfeas", "MuRed", "RelGap"):
                    option = "intpnt{}Tol{}".format(prefix, suffix)
                    self.int.setSolverParam(option, self.ext.options["tol"])

        # Handle "gaplim" option.
        if self.ext.options["gaplim"] is not None:
            self.int.setSolverParam("mioTolRelGap", self.ext.options["gaplim"])

        # Handle "maxit" option.
        # Subsolvers:
        # - "bi" is for basis identification via Simplex.
        # - "intpnt" is for the Interior Point Method.
        # - "sim" is for the Simplex algoritm.
        if self.ext.options["maxit"] is not None:
            for subsolver in ("bi", "intpnt", "sim"):
                option = "{}MaxIterations".format(subsolver)
                self.int.setSolverParam(option, self.ext.options["maxit"])

        # Handle "lp_node_method" option.
        if self.ext.options["lp_node_method"] is not None:
            if self.ext.options["lp_node_method"] == "interior":
                self.int.setSolverParam("mioNodeOptimizer", "intpnt")
            elif self.ext.options["lp_node_method"] == "psimplex":
                self.int.setSolverParam("mioNodeOptimizer", "primalSimplex")
            elif self.ext.options["lp_node_method"] == "dsimplex":
                self.int.setSolverParam("mioNodeOptimizer", "dualSimplex")
            else:
                self._handle_bad_option_value("lp_node_method")

        # Handle "lp_root_method" option.
        if self.ext.options["lp_root_method"] is not None:
            if self.ext.options["lp_root_method"] == "interior":
                self.int.setSolverParam("mioRootOptimizer", "intpnt")
            elif self.ext.options["lp_root_method"] == "psimplex":
                self.int.setSolverParam("mioRootOptimizer", "primalSimplex")
            elif self.ext.options["lp_root_method"] == "dsimplex":
                self.int.setSolverParam("mioRootOptimizer", "dualSimplex")
            else:
                self._handle_bad_option_value("lp_root_method")

        # Handle "timelimit" option.
        if self.ext.options["timelimit"] is not None:
            for prefix in ("optimizer", "mio"):
                option = "{}MaxTime".format(prefix)
                self.int.setSolverParam(option, self.ext.options["timelimit"])

        # Handle "nbsol" option.
        if self.ext.options["nbsol"] is not None:
            self.int.setSolverParam(
                "mioMaxNumSolutions", self.ext.options["nbsol"])

        # Handle "hotstart" option.
        if self.ext.options["hotstart"]:
            # TODO: Check if valued variables (i.e. a hotstart) are utilized by
            #       MOSEK beyond mioConstructSol, and whether it makes sense to
            #       (1) also value continuous variables and (2) reset variable
            #       values when hotstart gets disabled again (see Gurobi).
            self.int.setSolverParam("mioConstructSol", "on")
            self._import_variable_values(integralOnly = True)

        # Handle MOSEK-specific options.
        for option, value in self.ext.options["mosek_params"].items():
            try:
                self.int.setSolverParam(option, value)
            except msk.ParameterError:
                self._handle_bad_option_value("mosek_params",
                    "MOSEK option '{}' does not exist.".format(option))
            except ValueError as error:
                self._handle_bad_option_value("mosek_params",
                    "Invalid value '{}' for MOSEK option '{}': {}"
                    .format(value, option, str(error)))

        # Handle unsupported options.
        self._handle_unsupported_option("treememory")

        # Attempt to solve the problem.
        with self._header(), self._stopwatch():
            self.int.solve()

        # Retrieve primals.
        if self.ext.options["noprimals"]:
            primals = None
        else:
            primals = {}
            for varName, picosVar in self.ext.variables.items():
                mosekVar = self.knownVariables[picosVar]
                try:
                    primals[varName] = list(mosekVar.level())
                except msk.SolutionError:
                    primals[varName] = None

        # Retrieve duals.
        if self.ext.options["noduals"]:
            duals = None
        else:
            duals = []
            for picosCon in self.ext.constraints:
                # Retrieve corresponding MOSEK constraint.
                mosekCon = self.knownConstraints[picosCon]

                # Retrieve its dual.
                try:
                    mosekDual = mosekCon.dual()
                except msk.SolutionError:
                    duals.append(None)
                    continue

                # Devectorize the dual. Note the change from row-major to
                # column-major order.
                size = picosCon.size
                picosDual = cvxopt.matrix(mosekDual, (size[1], size[0])).T

                # Adjust the dual based on constraint type.
                if isinstance(picosCon, AffineConstraint) \
                or isinstance(picosCon, LMIConstraint):
                    if picosCon.is_decreasing():
                        picosDual = -picosDual
                elif isinstance(picosCon, SOCConstraint):
                    picosDual[0] = -picosDual[0]
                elif isinstance(picosCon, RSOCConstraint):
                    # MOSEK handles the vector [x₁; x₂; x₃] as input for a
                    # constraint of the form ‖x₃‖² ≤ 2x₁x₂ whereas PICOS handles
                    # the expressions e₁, e₂ and e₃ for a constraint of the form
                    # ‖e₁‖² ≤ e₂e₃. MOSEK's additional factor of two was
                    # neutralized on import by scaling e₂ and e₃ by sqrt(0.5)
                    # each to obtain x₁ and x₂ respectively. Scale now also the
                    # dual returned by MOSEK to make up for this.
                    scale = 0.5**0.5
                    alpha = scale * picosDual[0]
                    beta  = scale * picosDual[1]
                    z     = list(picosDual[2:])

                    # HACK: Work around a potential documentation bug in MOSEK:
                    #       The first two vector elements of the rotated
                    #       quadratic cone dual are non-positive (allowing for a
                    #       shorter notation in the linear part of their dual
                    #       representation) even though their definition of the
                    #       (self-dual) rotated quadratic cone explicitly states
                    #       that they are non-negative (as in PICOS).
                    alpha = -alpha
                    beta  = -beta

                    picosDual = cvxopt.matrix([alpha, beta] + z)
                else:
                    assert False, \
                        "Constraint type belongs to unsupported problem type."

                # Flip sign based on objective sense.
                if (self.int.getTask().getobjsense() == objsense.minimize):
                    picosDual = -picosDual

                duals.append(picosDual)

        # Retrieve objective value.
        try:
            objectiveValue = float(self.int.primalObjValue())
        except msk.SolutionError:
            objectiveValue = None

        # Retrieve solution metadata.
        meta = {}

        # Set MOSEK-specific entries "primal_status" and "dual_status".
        for key in ("primal_status", "dual_status"):
            if key == "primal_status":
                solutionStatus = self.int.getPrimalSolutionStatus()
            else:
                solutionStatus = self.int.getDualSolutionStatus()
            if solutionStatus is msk.SolutionStatus.Undefined:
                meta[key] = "undefined"
            elif solutionStatus is msk.SolutionStatus.Unknown:
                meta[key] = "unknown"
            elif solutionStatus is msk.SolutionStatus.Optimal:
                meta[key] = "optimal"
            elif mosek8 and solutionStatus is msk.SolutionStatus.NearOptimal:
                meta[key] = "near optimal"
            elif solutionStatus is msk.SolutionStatus.Feasible:
                meta[key] = "feasible"
            elif mosek8 and solutionStatus is msk.SolutionStatus.NearFeasible:
                meta[key] = "near feasible"
            elif solutionStatus is msk.SolutionStatus.Certificate:
                meta[key] = "infeasible"
            elif mosek8 and solutionStatus is \
                    msk.SolutionStatus.NearCertificate:
                meta[key] = "near infeasible"
            elif solutionStatus is msk.SolutionStatus.IllposedCert:
                meta[key] = "illposed"
            else:
                self._warn("The MOSEK solution status {} is not known to PICOS."
                    .format(solutionStatus))
                meta[key] = "unknown"

        # Set common entry "status".
        problemStatus = self.int.getProblemStatus(msk.SolutionType.Default)
        if problemStatus is msk.ProblemStatus.Unknown:
            meta["status"] = "unknown"
        elif problemStatus is msk.ProblemStatus.PrimalAndDualFeasible:
            meta["status"] = "feasible"
        elif problemStatus is msk.ProblemStatus.PrimalFeasible:
            meta["status"] = "primal feasible"
        elif problemStatus is msk.ProblemStatus.DualFeasible:
            meta["status"] = "dual feasible"
        elif problemStatus is msk.ProblemStatus.PrimalInfeasible:
            meta["status"] = "primal infeasible"
        elif problemStatus is msk.ProblemStatus.DualInfeasible:
            meta["status"] = "dual infeasible"
        elif problemStatus is msk.ProblemStatus.PrimalAndDualInfeasible:
            meta["status"] = "infeasible"
        elif problemStatus is msk.ProblemStatus.Illposed:
            meta["status"] = "illposed"
        elif problemStatus is msk.ProblemStatus.PrimalInfeasibleOrUnbounded:
            meta["status"] = "primal infeasible or unbounded"
        else:
            self._warn("The MOSEK problem status {} is not known to PICOS."
                .format(solutionStatus))
            meta["status"] = "unknown"

        # Refine common entry "status".
        primFsb = meta["status"] in ("feasible", "primal feasible")
        dualFsb = meta["status"] in ("feasible", "dual feasible")
        if primFsb or dualFsb:
            primOpt = meta["primal_status"] in ("optimal", "near optimal")
            dualOpt = meta["dual_status"] in ("optimal", "near optimal")
            if primFsb and dualFsb and primOpt and dualOpt:
                meta["status"] = "optimal"
            elif primFsb and primOpt:
                meta["status"] = "primal optimal"
            elif dualFsb and dualOpt:
                meta["status"] = "dual optimal"

        return (primals, duals, objectiveValue, meta)
