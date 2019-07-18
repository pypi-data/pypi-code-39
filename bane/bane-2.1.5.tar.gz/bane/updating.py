import os
def updater(version=None):
 if os.path.isdir('/home/')==True:
  os.system('sudo pip uninstall bane -y')
  if version:
   os.system('sudo pip install bane')
  else:
   os.system('sudo pip install bane=='+str(version))
 else:
  os.system('pip uninstall bane -y')
  if version:
   os.system('pip install bane')
  else:
   os.system('sudo pip install bane=='+str(version))
