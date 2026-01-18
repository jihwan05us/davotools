# %% [markdown]
## Header

# %%
## basic imports
import os, types

# %%
## additional imports
import importlib.util

# %%
##

# %% [markdown]
## Body: module

# %%
## to load a module from a source code
def load_module_from_code(
        name: str, # the name of the module
        path: str, # a source code path of the module
) -> types.ModuleType:
    """
    a function to load a module from a source code
    <input>
        name: str, # the name of the module
        path: str, # a source code path of the module
    <output>
        module: types.ModuleType
    """
    if not os.path.exists(path):
        raise ValueError( f"*** davotools.module.load_module_from_code(): no such {path}" )
    spec = importlib.util.spec_from_file_location( name, path )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ##
    return module

# %%
##

# %% [markdown]
## Footer

# %%
##

