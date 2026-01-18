# %% [markdown]
## Header

# %%
## basic imports
import os, types

# %%
##

# %% [markdown]
## Body

# %%
## main class
class davotools:
    ##
    def __init__( self, echo=False ) -> None:
        """
        <input>
            echo: bool = False # an internal process checker
        <output>
            None # the class itself returned
        """
        module_path = os.path.abspath(__file__)
        module_dir = os.path.dirname(module_path)
        if echo:
            print(f"-. davotools located at {module_dir}")
            print( "* davotools loading started..." )
        ##
        from davotools import minor
        self.minor = minor
        ##
        view = types.ModuleType('davotools.view')
        view.list = minor.view_list
        view.dict = minor.view_dict
        view.pd = minor.view_pd
        self.view = view
        ##
        from davotools import io
        self.io = io
        ##
        from davotools import image
        self.image = image
        ##
        if echo:
            print(f"* davotools loading finished.")
        return None

# %%
##

# %% [markdown]
## Footer

# %%
##

