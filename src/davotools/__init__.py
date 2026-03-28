# %% [markdown]
## Header

# %%
## basic imports
import os, types

# %%

# %% [markdown]
## Body

# %%
## davotools submodules
from davotools import minor
minor = minor
##
from davotools import io
io = io
##
from davotools import image
image = image

# %%
## davotools submodule: view
from davotools import view as _view
##
view = types.ModuleType('view')
##
view.list = _view.view_list
view.dict = _view.view_dict
view.pd = _view.view_pd

# %%
## initializer
def initialize(
        echo: bool = False
) -> tuple[str, str]:
    """
    Args:
        echo: bool = False # whether to show internal details
    Returns:
        module_path: str # the full path of the module
        module_dir: str # the directory of module_path
    Raises:
        None
    """
    module_path = os.path.abspath(__file__)
    module_dir = os.path.dirname(module_path)
    if echo:
        print(f"-. davotools loaded from {module_dir}")
    return module_path, module_dir

# %%
## to initialize
module_path, module_dir = initialize( echo=True )

# %%

# %% [markdown]
## Footer

# %%

