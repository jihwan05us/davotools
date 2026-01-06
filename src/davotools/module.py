# %% [markdown]
## Header

# %%
## basic imports
import types

# %%
## additional imports
import importlib.util

# %%
##

# %% [markdown]
## Body

# %%
## To load a module from a source code
def load_module_from_code(
        name: str, # the name of the module
        path: str, # a source code path of the module
) -> types.ModuleType:
    """
    <input>
        name: str, # the name of the module
        path: str, # a source code path of the module
    <output>
        module: types.ModuleType
    """
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

