from .queries import *
from .utilities import *
from .diffusion import PureText
from .diffusion.power_iteration import *
import itertools

text_models = [PureText]
lazy_models = [KatzPowerIteration, PagerankPowerIteration, PersonalisedPagerankPowerIteration]
heat_lazy_models = [HeatPagerankPowerIteration, HeatPersonalisedPagerankPowerIteration]

def execute_model(transition, query_response_set, reindex, diffusion, diffusion_args, prefix, base_path):
    """Given a model, we exectued and write the output to a file in
    treck format. The transition matrix is obtained in do_execution function.
    Args:
        diffusion: the diffusion model
        diffusion_args: additional arguments for diffusion constructor
        prefix: the prefix of the output file
        base_path: the base path of the output file
    """
    # Create model
    model = diffusion(transition, *diffusion_args)
    # Index is already build. Resolve queries
    ranks = reindex.ranking_for_queries(model, query_response_set)
    # Generate output file path
    out_file = "{}/{}_{}.run".format(base_path, prefix, str(model))
    write_trec_ranking_file(ranks, out_file)
    return out_file

def executable_text_models(models, prefix, base_path):
    """Generate text models calls
    Args:
        prefix: the prefix of the output file
        base_path: the base path of the output file
    Response:
        A list of executable functions, each of them with its parameters
    """
    executables = []
    for diffusion in models:
        executables.append( (execute_model, (diffusion, (),
                                             prefix, base_path)) )
    return executables

def executable_lazy_power_iteration_models(models, n, betas,
        prefix, base_path):
    """Generate lazy random walk models for each beta
    Args:
        models: the list of the diffusion models
        n: number of iterations
        betas: list of betas
        prefix: the prefix of the output file
        base_path: the base path of the output file
    Response:
        A list of executable functions, each of them with its parameters
    """
    executables = []
    for diffusion in models:
        for beta in betas:
            executables.append( (execute_model, (diffusion,
                                                 (n, beta), prefix, base_path)) )
    return executables

def executable_heat_lazy_power_iteration_models(models,
        n, betas, gammas, prefix, base_path):
    """Generate heat-kernel lazy random walk models for each beta
    and gamma.
    Args:
        models: the list of the diffusion models
        n: number of iterations
        betas: list of betas
        gammas: list of gammas
        prefix: the prefix of the output file
        base_path: the base path of the output file
    Response:
        A list of executable functions, each of them with its parameters
    """
    executables = []
    for diffusion in models:
        for beta, gamma in itertools.product(betas, gammas):
            executables.append( (execute_model, (diffusion,
                                                 (n, beta, gamma), prefix,
                                                 base_path)) )
    return executables

def execute_text_models(query_response_set, transition, re_index, prefix,
        base_path, num_processors = 1):
    """ Execute text models:
    Args:
        query_response_set: the response of the text index.
        transition: the transition matrix for diffusion
        re_index: ReIndex object to re-index input objects
        prefix: the prefix of the output file
        base_path: the base path of the output file
        num_processors: number of processors to execute in parallel.
    Response:
        A list with the output file paths
    """
    return do_execution(transition, query_response_set, re_index,
            executable_text_models(text_models, prefix, base_path)
            )

def execute_lazy_models(query_response_set, transition, re_index, n, betas,
        prefix, base_path, num_processors = 1):
    """ Execute lazy models:
    Args:
        query_response_set: the response of the text index.
        transition: the transition matrix for diffusion
        re_index: ReIndex object to re-index input objects
        n: number of iterations
        betas: list of betas
        prefix: the prefix of the output file
        base_path: the base path of the output file
        num_processors: number of processors to execute in parallel.
    Response:
        A list with the output file paths
    """
    return do_execution(transition, query_response_set, re_index,
            executable_lazy_power_iteration_models(
                lazy_models, n, betas, prefix, base_path)
            )

def execute_heat_lazy_models(query_response_set, transition, re_index,
        n, betas, gammas, prefix, base_path, num_processors = 1):
    """ Execute heat lazy models:
    Args:
        query_response_set: the response of the text index.
        transition: the transition matrix for diffusion
        re_index: ReIndex object to re-index input objects
        n: number of iterations
        betas: list of betas
        gammas: list of gammas
        prefix: the prefix of the output file
        base_path: the base path of the output file
        num_processors: number of processors to execute in parallel.
    Response:
        A list with the output file paths
    """
    return do_execution(transition, query_response_set, re_index,
            executable_heat_lazy_power_iteration_models(
                heat_lazy_models, n, betas, gammas, prefix, base_path)
            )

def execute_all_models(query_response_set, transition, re_index,
        n, betas, gammas, prefix, base_path, num_processors = 1):
    """Execute all models in parallel (up to 8 workers)
    Args:
        query_response_set: the response of the text index.
        transition: the transition matrix for diffusion
        re_index: ReIndex object to re-index input objects
        n: number of iterations
        betas: list of betas
        gammas: list of gammas
        prefix: the prefix of the output file
        base_path: the base path of the output file
        num_processors: number of processors to execute in parallel.
    Response:
        A list with the output file paths
    """
    return do_execution(transition, query_response_set, re_index,
            executable_text_models(text_models, prefix, base_path)
            + executable_lazy_power_iteration_models(lazy_models,
                n, betas, prefix, base_path)
            + executable_heat_lazy_power_iteration_models(heat_lazy_models,
                n, betas, gammas, prefix, base_path),
            num_processors)

def do_execution(transition, query_response_set, reindex, executables, num_processors = 1):
    """ Execute a list of executables in parallel (multiprocess, up to 8 processes)
    Args:
        transition: A transition matrix.
        query_response_set: The result of text index.
        reindex: Index to re-index the query_response_set.
        executable: list of pairs, where the first element is a callable and the
            second one is the list of parameters.
    Response:
        A list with the output for each execution in the same order as they
        were received.
    """
    # Run models sequentially
    ks = []
    for fun, args in executables:
        ks.append(fun(transition, query_response_set, reindex, *args))
    return ks

def execute_all_models_default(query_response_set, transition, re_index,
        prefix, base_path, num_processors = 1):
    """Execute all models with defualt parameters
    Args:
        query_response_set: the response of the text index.
        transition: the transition matrix for diffusion
        re_index: ReIndex object to re-index input objects
        prefix: the prefix of the output file
        base_path: the base path of the output file
        num_processors: number of processors to execute in parallel.
    Response:
        A list with the output file paths
    """
    n = 1
    betas = [0.001, 0.01, 0.1, 0.5, 0.85]
    gammas = [0.001, 0.01, 0.1, 0.5, 1.0]
    return execute_all_models(query_response_set, transition, re_index,
            n, betas, gammas, prefix, base_path, num_processors)
