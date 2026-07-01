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
def _set_path(echo: bool = True) -> tuple[str, str]:
    module_path = os.path.abspath(__file__)
    module_dir = os.path.dirname(module_path)
    if echo:
        print(f"-. davotools loaded from {module_dir}")
    return module_path, module_dir

# %%
## to load image_old as image
def load_image_old() -> None:
    import importlib.util as _ilu
    import os as _os
    _path = _os.path.join( _os.path.dirname(__file__), '_backup', 'image_old--20260428.py' )
    _spec = _ilu.spec_from_file_location('davotools.image_old', _path)
    _image_old = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_image_old)
    sys.modules[__name__].image = _image_old

# %%
## initialization
module_path, module_dir = _set_path(echo=False)

# %%
