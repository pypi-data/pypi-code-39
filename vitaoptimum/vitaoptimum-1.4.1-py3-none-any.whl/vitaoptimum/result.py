import sys
import matplotlib.pyplot as plt
from abc import abstractmethod


##############################################################################
#                      ALGORITHMS RESULT MAIN BASE CLASS                     #
##############################################################################

class _ResultBase:

    @abstractmethod
    def to_string(self, separator):
        pass

    def __str__(self):
        return self.to_string(separator="\n")

    def print(self, device=sys.stdout):
        if device:
            device.write(self.to_string(separator="\n"))
            device.write("\n")
        else:
            print(sys.stderr, "Print device is not defined")

    @abstractmethod
    def plot_convergence(self):
        pass

    def plot_fobj(self):
        '''Plot objective function within boundaries constraints'''
        print("Not implemented")

    def plot_optimum(self):
        '''Plot found optimum (point on fobj within a small area)'''
        print("Not implemented")


##############################################################################
#                      VITA OPTIMUM RESULTS BASE CLASSES                     #
##############################################################################


class _VitaOptimumResult(_ResultBase):
    """Base result for all VitaOptimum Methods"""

    def __init__(self, best_fobj, solution, convergence):
        self._best_fobj = best_fobj
        self._solution = solution
        self._convergence = convergence

    def to_string(self, separator='\n'):
        lines = [
            f"Best objective function value: {self._best_fobj}",
            f"Found solution: {self._solution}",
            f"Convergence: {self._convergence}",
        ]
        return separator.join(lines)

    def plot_convergence(self):
        '''Plot convergence of the solution search by VitaOptimum'''
        plt.xlabel('Number of function evaluations')
        plt.ylabel('Objective function')
        plt.title('Convergence graph')
        plt.grid(True)
        plt.plot(self._convergence, 'b', label='line')
        plt.show()

    @property
    def solution(self):
        return self._solution

    @property
    def best_fobj(self):
        return self._best_fobj

    @property
    def convergence(self):
        return self._convergence


class _VitaOptimumUnconstrainedResult(_VitaOptimumResult):
    """Base result for all VitaOptimum Unconstrained Methods"""

    def to_string(self, separator='\n'):
        lines = [super().to_string(separator)]
        return separator.join(lines)


class _VitaOptimumConstrainedResult(_VitaOptimumResult):
    """Base result for all VitaOptimum Constrained Methods"""

    def __init__(self, best_fobj, solution, best_constrains, convergence):
        self._best_constrains = best_constrains
        _VitaOptimumResult.__init__(self, best_fobj, solution, convergence)

    def to_string(self, separator='\n'):
        lines = [super().to_string(separator)]
        lines.append(f"Best constraint values: {self._best_constrains}")
        return separator.join(lines)

    @property
    def constrains(self):
        return self._best_constrains



class _VitaOptimumMixedResult(_VitaOptimumResult):
    """Mixed Unonstrained Method Result"""

    def __init__(self, best_fobj, continuous_solution, integer_solution,
             binary_solution, permutations_solution, convergence):
        mixed_solution = [
            continuous_solution,
            integer_solution,
            binary_solution,
            permutations_solution
        ]
        _VitaOptimumUnconstrainedResult.__init__(self, best_fobj,
                mixed_solution, convergence)

    def to_string(self, separator='\n'):
        lines = [
            f"Best objective function value: {self._best_fobj}",
            f"Found continuous solution: {self._solution[0]}",
            f"Found integer solution: {self._solution[1]}",
            f"Found binary solution: {self._solution[2]}",
            f"Found permutations solution: {self._solution[3]}",
            f"Convergence: {self._convergence}",
        ]
        return separator.join(lines)


##############################################################################
#                            VITA OPTIMUM RESULTS                            #
##############################################################################

class VitaOptimumBcsResult(_VitaOptimumConstrainedResult):
    """Binary Constrained Method Result"""

    def to_string(self, separator='\n'):
        lines = [
            f"Binary Constrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumBusResult(_VitaOptimumUnconstrainedResult):
    """Binary Unconstrained Global Optimization Method Result"""

    def to_string(self, separator='\n'):
        lines = [
            f"Binary Unconstrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumCcsResult(_VitaOptimumConstrainedResult):
    """Continuous Constrained Method Result"""

    def to_string(self, separator='\n'):
        lines = [
            f"Continuous Constrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumCusResult(_VitaOptimumUnconstrainedResult):
    """Continuous Unconstrained Method Result"""

    def to_string(self, separator='\n'):
        lines = [
            f"Continuous Unconstrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumIcsResult(_VitaOptimumConstrainedResult):
    """Integer Constrained Method Result"""

    def to_string(self, separator='\n'):
        lines = [
            f"Integer Constrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumIusResult(_VitaOptimumUnconstrainedResult):
    """Integer Unconstrained Method Result"""

    def to_string(self, separator='\n'):
        lines = [
            f"Integer Unconstrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumMcsResult(_VitaOptimumConstrainedResult):
    """Mixed Constrained Method Result"""

    def __init__(self, best_fobj, continuous_solution, integer_solution,
                 binary_solution, permutations_solution, best_constrains,
                 convergence):
        self._best_constrains = best_constrains
        _VitaOptimumMixedResult.__init__(
            self, best_fobj, continuous_solution,
            integer_solution,  binary_solution,
            permutations_solution, convergence)

    @property
    def best_constrains(self):
        return self._best_constrains

    def to_string(self, separator='\n'):
        lines = [
            f"Mixed Constrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        lines.append(f"Best constraint values: {self._best_constrains}")
        return separator.join(lines)


class VitaOptimumMusResult(_VitaOptimumUnconstrainedResult):
    """Mixed Unconstrained Method Result"""

    def __init__(self, best_fobj, continuous_solution, integer_solution,
                 binary_solution, permutations_solution, convergence):
        _VitaOptimumMixedResult.__init__(
            self, best_fobj, continuous_solution,
            integer_solution,  binary_solution,
            permutations_solution, convergence)

    def to_string(self, separator='\n'):
        lines = [
            f"Mixed Unconstrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPcsResult(_VitaOptimumConstrainedResult):
    """Permutation Constrained Method Result"""

    def to_string(self, separator='\n'):
        lines = [
            f"Permutation Constrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPusResult(_VitaOptimumUnconstrainedResult):
    """Permutation Unconstrained Method Result"""

    def to_string(self, separator='\n'):
        lines = [
            f"Permutation Unconstrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


##############################################################################
#                            VITA OPTIMUM PLUS RESULTS                       #
##############################################################################

class _VitaOptimumPlusResult(_ResultBase):
    """Base result for all VitaOptimum Plus Global Optimization Methods"""

    def __init__(self, best_fobj, solution, is_converged, quality):
        self._best_fobj = best_fobj
        self._solution = solution
        self._is_converged = is_converged
        self._quality = quality

    def to_string(self, separator='\n'):
        lines = [
            f"Is converged: {self._is_converged[0]}",
            f"Best objective function value: {self._best_fobj}",
            f"Found solution: {self._solution}",
            f"Quality: {self._quality}",
        ]
        return separator.join(lines)

    def plot_convergence(self):
        '''Plot convergence of the solution search by VitaOptimum Plus'''
        print("Not implemented")

    @property
    def solution(self):
        return self._solution

    @property
    def quality(self):
        return self._quality

    @property
    def best_fobj(self):
        return self._best_fobj

    @property
    def is_converged(self):
        return self._is_converged


class _VitaOptimumPlusConstrainedResult(_VitaOptimumPlusResult):

    def __init__(self, best_fobj, best_constrains, solution, is_converged, quality):
        self._best_constrains = best_constrains
        _VitaOptimumPlusResult.__init__(self, best_fobj, solution, is_converged, quality)

    @property
    def best_constrains(self):
        return self._best_constrains

    def to_string(self, separator='\n'):
        lines = [super().to_string(separator)]
        lines.append(f"Best constraint values: {self._best_constrains}")
        return separator.join(lines)


class _VitaOptimumPlusUnconstrainedResult(_VitaOptimumPlusResult):

    def __init__(self, best_fobj, solution, is_converged, quality):
        _VitaOptimumPlusResult.__init__(self, best_fobj, solution, is_converged, quality)

    def to_string(self, separator='\n'):
        lines = [super().to_string(separator)]
        return separator.join(lines)


class VitaOptimumPlusBcsResult(_VitaOptimumPlusConstrainedResult):
    """Binary Constrained Method Result (VO+)"""

    def to_string(self, separator='\n'):
        lines = [
            f"Binary Constrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPlusBusResult(_VitaOptimumPlusUnconstrainedResult):
    """Binary Unconstrained Method Result (VO+)"""

    def to_string(self, separator='\n'):
        lines = [
            f"Binary Unconstrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPlusCcsResult(_VitaOptimumPlusConstrainedResult):
    """Continuous Constrained Method Result (VO+)"""

    def to_string(self, separator='\n'):
        lines = [
            f"Continuous Constrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPlusCusResult(_VitaOptimumPlusUnconstrainedResult):
    """Continuous Unconstrained Method Result (VO+)"""

    def to_string(self, separator='\n'):
        lines = [
            f"Continuous Unconstrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPlusIcsResult(_VitaOptimumPlusConstrainedResult):
    """Integer Constrained Method Result (VO+)"""

    def to_string(self, separator='\n'):
        lines = [
            f"Integer Constrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPlusIusResult(_VitaOptimumPlusUnconstrainedResult):
    """Integer Unconstrained Method Result (VO+)"""

    def to_string(self, separator='\n'):
        lines = [
            f"Integer Unconstrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPlusPcsResult(_VitaOptimumPlusConstrainedResult):
    """Permutation Constrained Method Result (VO+)"""

    def to_string(self, separator='\n'):
        lines = [
            f"Permutation Constrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPlusPusResult(_VitaOptimumPlusUnconstrainedResult):
    """Permutation Unconstrained Method Result (VO+)"""

    def to_string(self, separator='\n'):
        lines = [
            f"Permutation Unconstrained Global Optimization Method Result:",
        ]
        lines.append(super().to_string(separator))
        return separator.join(lines)


class VitaOptimumPlusMusResult(_VitaOptimumPlusUnconstrainedResult):
    def __init__(self, best_fobj, continuous_solution,
                 integer_solution, binary_solution,
                 permutations_solution, is_converged,
                 quality):
        mixed_solution = [
            continuous_solution,
            integer_solution,
            binary_solution,
            permutations_solution
        ]
        _VitaOptimumPlusUnconstrainedResult.__init__(
                self, best_fobj, mixed_solution, is_converged, quality)

    def to_string(self, separator='\n'):
        lines = [
            f"Mixed Unconstrained Global Optimization Method Result:",
            f"Best objective function value: {self._best_fobj}",
            f"Found continuous solution: {self._solution[0]}",
            f"Found integer solution: {self._solution[1]}",
            f"Found binary solution: {self._solution[2]}",
            f"Found permutations solution: {self._solution[3]}",
            f"Is converged: {self._convergence}",
            f"Quality: {self._quality}",
        ]
        return separator.join(lines)
