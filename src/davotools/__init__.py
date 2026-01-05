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
## Beginning
module_path = os.path.abspath(__file__)
module_dir = os.path.dirname(module_path)
print(f"-. davotools located at {module_dir}")
##
print( "* davotools loading started..." )

## Main
class davotools:
    ##
    def __init__(self) -> None:
        """
        <return>
        None
        """
        from davotools import display
        self.display = display
        ##
        from davotools import convert
        self.convert = convert
        ##
        print(f"* davotools loading finished.")
        return None

# %%
##

# %% [markdown]
## Footer

# %%
##

