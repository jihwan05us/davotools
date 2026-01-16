# %% [markdown]
## Header

# %%
## basic imports
import os

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
        from davotools import display
        self.display = display
        ##
        from davotools import module
        self.module = module
        ##
        from davotools import CLI
        self.CLI = CLI
        ##
        from davotools import convert
        self.convert = convert
        ##
        from davotools import generate
        self.generate = generate
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

