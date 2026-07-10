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
## initialization
module_path = os.path.abspath(__file__)
module_dir = os.path.dirname(module_path)

# %%
