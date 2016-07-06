

import sys
import importlib



def find(directory, module_name):
    if directory not in sys.path:
        sys.path.insert(0, directory)
    print (sys.path)

    mod = importlib.import_module(module_name)

    if not hasattr(mod, 'main'):
        raise Exception(str(mod) + ' HAS NO name: main')

    return mod.main
