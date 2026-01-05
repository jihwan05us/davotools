# %% [markdown]
## Header

# %%
## basic imports
import datetime, math, os, sys, time, types
import argparse, json, yaml
##
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
##
from IPython.display import display
from tqdm import tqdm

# %%
## additional imports
#import geojson
#import shapely.geometry
#import skimage.draw

# %%
##

# %% [markdown]
## Body

# %%
## to print a list
def print_list(
        l: list, # list
        k: str = None, # keyword
) -> None:
    """
    <return>
    None
    """
    if k is not None:
        print( f"-. {k}" )
    for v in l:
        print( f"* {v}" )
    ##
    return None

# %%
## To print a dict
def print_dict(
        d: dict, # dictionary
        k: str = None, # keyword
        i: int = 0, # layer index
) -> None:
    """
    <return>
    None
    """
    if i == 0:
        bullet = '-.'
    else:
        bullet = "".join( ['*'] * i )
    ##
    if not isinstance( d, dict ):
        print( f"{bullet} {k}: {d}" )
    else:
        if k is not None:
            print( f"{bullet} {k}" )
        for k1, d1 in d.items():
            print_dict( d1, k1, i+1 )
    ##
    return None

# %%
## To update values of a dictionary
def update_dict(
        orig: dict, # the original dict to update
        new: dict = None, # new dict to update
        echo: bool = False, **kwargs
) -> dict:
    """
    <return>
    output: dict # the updated dict
    """
    output = orig.copy()
    for k, v in new.items():
        output[k] = v
        if echo:
            print( f"* {k}: {v}")
    ##
    return output

# %%
## To load a module from a source code
from importlib.util import spec_from_file_location as iu_spec_from_file_location
from importlib.util import module_from_spec as iu_module_from_spec
##
def load_module_from_code(
        name: str, # the name of the module
        path: str, # a source code path of the module
) -> types.ModuleType:
    """
    <return>
    module: types.ModuleType
    """
    spec = iu_spec_from_file_location( name, path )
    module = iu_module_from_spec(spec)
    spec.loader.exec_module(module)
    ##
    return module

# %%
##

# %% [markdown]
## Footer

# %%
##

