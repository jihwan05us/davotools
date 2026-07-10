# %% [markdown]
## Header

# %%
## imports
import pandas as pd
try:
    from IPython.display import display
except ImportError:
    display = print

# %%

# %% [markdown]
## Body: view

# %%
## to view a list
def view_list(
        l: list,
        k: str | None = None,
) -> None:
    """
    a function to view a list
    Args:
        l: list # a list
        k: str | None = None # a keyword describing 'l'
    Returns: None
    """
    if k is not None:
        print(f"-. {k}")
    for v in l:
        print(f"* {v}")

# %%
## to view a dict
def view_dict(
        d: dict,
        k: str | None = None,
        i: int = 0,
) -> None:
    """
    a function to view a dict
    Args:
        d: dict # a dictionary
        k: str | None = None # a keyword describing 'd'
        i: int = 0 # a layer index for checking depth
    Returns: None
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

# %%
## to view a pandas table
def view_pd(
        table: pd.DataFrame,
        k: str | None = None,
        iloc: list[int] | None = None,
) -> None:
    """
    a function to view a pandas table
    Args:
        table: pd.DataFrame # a pandas table
        k: str | None = None # a keyword describing 'table'
        iloc: list[int] | None = None # a location index (default: [0,1,-1])
    Returns: None
    """
    if iloc is None:
        iloc = [0, 1, -1]
    if k is None:
        k = 'table'
    print(f"-. {k}: { type(table) } {table.shape}")
    if table.shape[0] > 5:
        display( table.iloc[iloc] )
    else:
        display(table)

# %%

