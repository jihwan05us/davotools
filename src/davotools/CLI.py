# %% [markdown]
## Header

# %%
## basic imports
import argparse

# %%
##

# %% [markdown]
## Body

# %%
## to load command line interface (CLI) inputs
def load_inputs(
        parser: argparse.Namespace, # CLI arguments
        in_IPy: bool # a checker of IPython interface
) -> dict:
    """
    a function to load command line interface (CLI) inputs
    <input>
        parser: argparse.Namespace, # CLI argument settings
        in_IPy: bool # a checker: whether being inside an IPython interface
    <output>
        CLI: dict
    """
    ##
    CLI = parser.parse_args() if not in_IPy \
        else parser.parse_args("") # for Jupyter interface
    CLI = vars(CLI)
    return CLI

# %% [markdown]
## Footer

# %%
##

