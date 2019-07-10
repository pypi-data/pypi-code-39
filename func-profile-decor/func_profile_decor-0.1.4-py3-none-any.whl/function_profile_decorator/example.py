"""Small example on how to use @profile decorator."""
from function_profile_decorator import profile


@profile(mem_prof=True)
def factoriel_loop(n: int) -> int:
    """Calculate factoriel non-recursive."""
    fac: int = 1
    for i in range(1, n + 1):
        fac = fac * i
    return fac


factoriel_loop(n=100)

