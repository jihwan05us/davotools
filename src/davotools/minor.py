# %% [markdown]
## Header

# %%
## basic imports
import datetime

# %%

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
    Args:
        orig: dict, # the original dict to update
        new: dict = None, # new dict to update
        ignore_None: bool = False, # a checker: whether to ignore updating None
        echo: bool = False,
    Returns:
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
    Args:
        time: datetime, # the time in datetime format
    Returns:
        time_form: str # the time in str (%Y-%m-%d %H:%M:%S)
    """
    time_form = time.strftime("%Y-%m-%d %H:%M:%S")
    return time_form

# %%

# %% [markdown]
## Footer

