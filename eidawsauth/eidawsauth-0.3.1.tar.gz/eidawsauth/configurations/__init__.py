# With this code in place, you can call `import configurations` and all .py files in there will be available in the code : configurations.Production.authdb for instance.
import os
import importlib
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
#    importlib.import_module(module[:-3])
    importlib.import_module('.'+module[:-3], 'configurations')
del module
