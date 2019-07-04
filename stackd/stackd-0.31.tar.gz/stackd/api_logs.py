import sys
from .run_shell import run_shell

def api_logs(env_vars={}, args=[]):
  fullServiceName = env_vars['STACKD_STACK_NAME']+'_'+args.pop(0)
  process = run_shell(['docker','service','logs',fullServiceName,args])
  if(process.returncode != 0):
      sys.exit(process.returncode)