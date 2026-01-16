# %% [markdown]
## Header

# %%
## basic imports
import types

# %%
##

# %% [markdown]
## Body

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

