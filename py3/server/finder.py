

import sys
import inspect
import importlib



def find(directory, module_name):
    if directory not in sys.path:
        sys.path.insert(0, directory)

    mod = importlib.import_module(module_name)

    if not hasattr(mod, 'main'):
        raise Exception(str(mod) + ' HAS NO name: main')

    if not inspect.isfunction(mod.main):
        raise Exception('main is not function in ' + str(mod) )

    return mod.main
