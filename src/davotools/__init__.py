# %% [markdown]
## Header

# %%
## imports
import os, types

# %%

# %% [markdown]
## Body

# %%
## davotools submodules
from davotools import image
from davotools import io
from davotools import minor
from davotools import snapshot

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
def _set_path(echo: bool = True) -> tuple[str, str]:
    module_path = os.path.abspath(__file__)
    module_dir = os.path.dirname(module_path)
    if echo:
        print(f"-. davotools loaded from {module_dir}")
    return module_path, module_dir

# %%
## initialization
module_path, module_dir = _set_path(echo=False)

# %%
