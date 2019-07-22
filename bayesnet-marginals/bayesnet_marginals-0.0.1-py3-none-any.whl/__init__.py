from importlib.util import find_spec as _find_spec

from bayesnet.core import DiscreteRandomVariable


# Verify if OpenCL is available. If it is is not, fallback to pure Python
# implementation.
if _find_spec('opencl') is not None:
    from bayesnet.opencl import ProbabilityMassFunction
    from bayesnet.opencl import ProbabilityMassFunctionMarginal
    from bayesnet.opencl import ProbabilityMassFunctionProduct

else:
    from bayesnet.pmf import ProbabilityMassFunction
    from bayesnet.pmf import ProbabilityMassFunctionMarginal
    from bayesnet.pmf import ProbabilityMassFunctionProduct

