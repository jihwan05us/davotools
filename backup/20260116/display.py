# %% [markdown]
## Header

# %%
## basic imports
import pandas as pd
##
from IPython.display import display as Id_display

# %%
##

# %% [markdown]
## Body

# %%
## to display: a list
def view_list(
        l: list, # a list
        k: str = None, # a keyword describing 'l'
) -> None:
    """
    a function to display: a list
    <input>
        l: list, # a list
        k: str = None, # a keyword describing 'l'
    <output>
        None
    """
    if k is not None:
        print(f"-. {k}")
    for v in l:
        print(f"* {v}")
    ##
    return None

# %%
## to display: a dict
def view_dict(
        d: dict, # a dictionary
        k: str = None, # a keyword describing 'd'
        i: int = 0, # a layer index for checking depth
) -> None:
    """
    a function to display: a dict
    <input>
        d: dict, # a dictionary
        k: str = None, # a keyword describing 'd'
        i: int = 0, # a layer index for checking depth
    <output>
        None
    """
    if i == 0:
        bullet = '-.'
    else:
        bullet = "".join( ['*'] * i )
    ##
    if not isinstance(d, dict):
        print(f"{bullet} {k}: {d}")
    else:
        if k is not None:
            if i == 0:
                print(f"{bullet} {k}: { type(d) }")
            else:
                print(f"{bullet} {k}")
        for k1, d1 in d.items():
            view_dict(d1, k1, i+1)
    ##
    return None

# %%
## to display: a pandas table
def view_pd(
        table: pd.DataFrame, # a pandas table
        k: str = None, # a keyword describing 'table'
        iloc: list[int] = [0,1,-1], # a location index
) -> None:
    """
    a function to display: a pandas table
    <input>
        table: pd.DataFrame, # a pandas table
        k: str = None, # a keyword describing 'table'
        iloc: list[int] = [0,1,-1], # a location index
    <output>
        None
    """
    if k is None:
        k = 'table'
    print(f"-. {k}: { type(table) } {table.shape}")
    Id_display( table.iloc[iloc] )
    ##
    return None

# %%
##

# %% [markdown]
## Footer

# %%
##

