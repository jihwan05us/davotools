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
    ## to load command line interface (CLI) inputs
    <input>
        parser: argparse.Namespace, # CLI arguments
        in_IPy: bool # a checker: whether being inside an IPython interface
    <output>
        vars: dict
    """
    ##
    CLI = parser.parse_args() if not in_IPy \
        else parser.parse_args("") # for Jupyter interface
    vars = vars(CLI)
    return vars

# %%
## To update a configuration of pipeline with CLIs
def update_config_with_CLI(
        config: dict, # configuration
        CLI: argparse.Namespace, # commaned line arguments
) -> dict:
    ##
    config_update = { 'cwd': os.getcwd() }
    config_update = { **config_update, **config }
    ##
    for k, v in CLI.items():
        if v is not None:
            config_update[k] = v
    ##
    return config_update

# %%
## to update values of a dictionary
def update_dict(
        orig: dict, # the original dict to update
        new: dict = None, # new dict to update
        echo: bool = False,
) -> dict:
    """
    <input>
        orig: dict, # the original dict to update
        new: dict = None, # new dict to update
        echo: bool = False,
    <output>
        dict # the updated dict
    """
    output = orig.copy()
    for k, v in new.items():
        output[k] = v
        if echo:
            print( f"* {k}: {v}")
    ##
    return output

# %% [markdown]
## Footer

# %%
##

