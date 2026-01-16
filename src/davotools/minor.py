# %% [markdown]
## Header

# %%
## basic imports
import datetime

# %%
##

# %% [markdown]
## Body

# %%
## to update values of a dictionary
def update_dict(
        orig: dict, # the original dict to update
        new: dict = None, # new dict to update
        echo: bool = False # a checker: whether to visualize details
) -> dict:
    """
    a function to update values of a dictionary
    <input>
        orig: dict, # the original dict to update
        new: dict = None, # new dict to update
        echo: bool = False,
    <output>
        updated: dict # the updated dict
    """
    updated = orig.copy()
    for k, v in new.items():
        updated[k] = v
        if echo:
            print( f"* {k}: {v}")
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
        echo: bool = False # a checker: whether to visualize details
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
## Footer

# %%
##

