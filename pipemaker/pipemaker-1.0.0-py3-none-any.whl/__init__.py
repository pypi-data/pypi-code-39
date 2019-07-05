from .utils.dotdict import dotdict

# config
config = dotdict(
    ###### input/output file locations ################

    # path filled at runtime with pathvars
    path ="{filesystem}{datapath}/{job}/{subpath}.pkl",
    pathvars = dotdict(filesystem="osfs://", datapath="pipedata"),

    # dict(subpath=fixedpath) to override path above e.g. for file shared between jobs
    # can also override at task creation e.g. Task(ipaths=dict(afile="xxx"), opath="xxx")
    fixedpaths=dotdict(),

    # parameter inputs not from files
    params = dotdict(),

    # True=rabbitmq, False=immediate
    queue = False
)

######################################################################
# shortcuts for use in notebooks

from .commands import make, make_all, cleanup, load, save