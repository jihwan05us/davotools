# %% [markdown]
## Header

# %%
## imports
import os, sys, types

# %%

# %% [markdown]
## Body

# %%
## davotools submodules
from davotools import minor, io
from davotools import image

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
## (internal) to set the module path
def _set_path(
        echo: bool = True
) -> tuple[str, str]:
    """
    an internal function to set the module path
    Args:
        echo: bool = True # whether to show internal details
    Returns:
        module_path: str # the full path of the module
        module_dir: str # the directory of module_path
    """
    module_path = os.path.abspath(__file__)
    module_dir = os.path.dirname(module_path)
    if echo:
        print(f"-. davotools loaded from {module_dir}")
    return module_path, module_dir

# %%
## to load image_old as image
def load_image_old() -> None:
    """
    a function to replace davotools.image with davotools.image_old
    Args: None
    Returns: None
    """
    import davotools.image_old as _image_old
    sys.modules[__name__].image = _image_old

# %%
## initialization
module_path, module_dir = _set_path()

# %%

