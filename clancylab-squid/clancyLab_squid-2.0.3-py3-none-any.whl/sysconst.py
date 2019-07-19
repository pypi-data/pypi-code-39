# System Constants. This includes paths to where things are installed
orca_path = ""
orca4_path = "/home/hherbol/Programs/orca/4.1.2/orca"
use_orca4 = True
sandbox_orca = False

g09_formchk = ""
g09_cubegen = ""
vmd_path = ""
ovito_path = ""
opls_path = "/home/hherbol/Programs/squid/2.0.0/forcefield_parameters/oplsaa.prm"
packmol_path = "/home/hherbol/Programs/packmol/packmol"
lmp_path = "/home/hherbol/Programs/lammps/16Mar18_py3/src/lmp_mpi"
python_path = "/home/hherbol/Programs/anaconda/3.7/bin/python"

mpirun_path = "/home/hherbol/Programs/openmpi/3.1.3/build/bin/mpiexec"

queueing_system = "None" # nbs, pbs, slurm
default_queue = "None"
slurm_default_allocation = None
nbs_ssh = None
nbs_bin_path = ""

# Default modules to load in pysub submission.
default_pysub_modules = ["squid/2.0.0"]

# Submission flags for queueing system
orca_sub_flag = ""

# A list of all paths/environment variables needed for queue submission
env_vars = '''
'''
orca_env_vars = '''
'''
orca4_env_vars = '''
'''
lmp_env_vars = '''
'''

# Mpi preface for job submission
mpi_preface = ""
