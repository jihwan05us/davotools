# %% [markdown]
## Header

# %%
## imports
import os

# %%
##

# %% [markdown]
## Body

# %%
## main class
class davotools:
    ##
    def __init__(self) -> None:
        """
        <return>
        None
        """
        module_path = os.path.abspath(__file__)
        module_dir = os.path.dirname(module_path)
        print(f"-. davotools located at {module_dir}")
        print( "* davotools loading started..." )
        ##
        from davotools import module
        self.module = module
        ##
        from davotools import display
        self.display = display
        ##
        from davotools import convert
        self.convert = convert
        ##
        from davotools import generate
        self.generate = generate
        ##
        from davotools import minor
        self.minor = minor
        ##
        print(f"* davotools loading finished.")
        return None

# %%
##

# %% [markdown]
## Footer

# %%
##

