# %% [markdown]
## Header

# %%
## basic imports
import datetime
##
import pandas as pd

# %%
## additional imports
from IPython.display import display as Id_display

# %%
##

# %% [markdown]
## Body

# %%
## to update values of a dictionary
def update_dict(
        orig: dict, # the original dict to update
        new: dict = None, # new dict to update
        ignore_None: bool = False, # a checker: whether to ignore updating None
        echo: bool = False # a checker: whether to visualize details
) -> dict:
    """
    a function to update values of a dictionary
    <input>
        orig: dict, # the original dict to update
        new: dict = None, # new dict to update
        ignore_None: bool = False, # a checker: whether to ignore updating None
        echo: bool = False,
    <output>
        updated: dict # the updated dict
    """
    updated = orig.copy()
    for k, v in new.items():
        if echo:
            print( f"* {k}: {v}")
        if ( ignore_None is True ) and ( v is None ):
            continue
        else:
            updated[k] = v
    ##
    return updated

# %%
##

# %% [markdown]
## Body: time

# %%
## to keep a track of time
def time_keep(
        time_start: datetime = None, # the starting time if time spent is needed
        echo: bool = True # a checker: whether to visualize details
) -> datetime:
    ##
    """
    a function to keep a track of time
    <input>
        time_start: datetime = None, # the starting time
        echo: bool = False # a checker: whether to visualize details
    <output>
        time_return: datetime
            (1) if time_start is None, then the time_start is returned.
            (1) if time_start not None, then the time_end is returned.
    """
    if time_start is None:
        time_start = datetime.datetime.now()
        time_start_form = time_format(time_start)
        if echo:
            print( f"-. Time (start): {time_start_form}" )
        time_return = time_start
    else:
        time_end = datetime.datetime.now()
        time_end_form = time_format(time_end)
        if echo:
            print( f"-. Time (end): {time_end_form}" )
        ##
        time_spent = time_end - time_start
        if echo:
            print( f"-. Time (spent): { str(time_spent) }" )
        time_return = time_end
    ##
    return time_return

# %%
## to change the format of a datetime object into str
def time_format(
        time: datetime, # the time in datetime format
) -> str:
    ##
    """
    a function to change the format of a datetime object into str
    <input>
        time: datetime, # the time in datetime format
    <output>
        time_form: str # the time in str (%Y-%m-%d %H:%M:%S)
    """
    time_form = time.strftime("%Y-%m-%d %H:%M:%S")
    return time_form

# %%
##

# %% [markdown]
## Body: view

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
    if table.shape[0] > 5:
        Id_display( table.iloc[iloc] )
    else:
        Id_display(table)
    ##
    return None

# %%
##

# %% [markdown]
## Footer

# %%
##

