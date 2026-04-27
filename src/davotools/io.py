# %% [markdown]
## Header

# %%
## imports
import argparse, datetime, json, os, pickle, types
import importlib.util
import xml.etree.ElementTree
##
import geojson
import numpy as np
import pandas as pd
import skimage.io
import tifffile
import yaml

# %%

# %% [markdown]
## Body

# %%
## to read a data file
def read(
        path: str,
        echo: bool = False,
        **kwargs
) -> object:
    """
    a function to read a data file
    Args:
        path: str # a path of the data file
        echo: bool = False # whether to print internal details
        **kwargs
    Returns:
        data: (object) # data object read from the file
    """
    filename = path.split('/')[-1]
    if '.' not in filename:
        _msg = f"*** davotools.io.read(): no file extension in '{path}'"
        raise ValueError(_msg)
    extension = filename.split('.')[-1]
    ##
    if extension == 'pkl':
        with open(path, 'rb') as f:
            data = pickle.load(f, **kwargs)
    elif extension == 'npy':
        data = np.load(path, **kwargs)
    ##
    elif extension == 'csv':
        data = pd.read_csv(path, **kwargs)
    elif extension == 'tsv':
        data = pd.read_csv(path, sep='\t', **kwargs)
    elif extension in ['xlsx', 'xls']:
        data = pd.read_excel(path, **kwargs)
    elif extension == 'feather':
        data = pd.read_feather(path, **kwargs)
    ##
    elif extension in ['jpg', 'jpeg', 'png']:
        data = skimage.io.imread(path, **kwargs)
    elif extension in ['tiff', 'tif', 'qptiff']:
        data = tifffile.imread(path, **kwargs)
    ##
    elif extension == 'json':
        with open(path, 'r') as f:
            data = json.load(f, **kwargs)
    elif extension in ['yaml', 'yml']:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
    elif extension == 'geojson':
        with open(path, 'r') as f:
            data = geojson.load(f, **kwargs)
    elif extension == 'annotations':
            data = xml.etree.ElementTree.parse(path, **kwargs)
    ##
    else:
        _msg = "*** Please check the extension."
        raise Exception(_msg)
    ##
    if echo:
        print(f"-. path loaded: {path}")
    return data

# %%
## to write data into a file
def write(
        path: str,
        data: object,
        echo: bool = False,
        **kwargs
) -> None:
    """
    a function to write data into a file
    Args:
        path: str # a path of the file
        data: object # a data to be written into a file
        echo: bool = False # whether to print internal details
        **kwargs
    Returns: None
    """
    path_dir = os.path.dirname(path)
    if path_dir:
        os.makedirs(path_dir, exist_ok=True)
    ##
    file = path.split('/')[-1]
    if '.' not in file:
        _msg = f"*** davotools.io.write(): no file extension in '{path}'"
        raise ValueError(_msg)
    extension = file.split('.')[-1]
    ##
    if extension == 'pkl':
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    elif extension == 'npy':
        np.save(path, data, **kwargs)
    ##
    elif extension == 'csv':
        data.to_csv(path, **kwargs)
    elif extension == 'tsv':
        data.to_csv(path, sep='\t', **kwargs)
    elif extension == 'feather':
        data.to_feather(path, **kwargs)
    ##
    elif extension in ['jpeg', 'jpg', 'png']:
        skimage.io.imsave(path, data, **kwargs)
    elif extension in ['tiff', 'tif']:
        _write_tiff(path, data, **kwargs)
    ##
    elif extension == 'json':
        with open(path, 'w') as f:
            json.dump(data, f, indent=4, **kwargs)
    elif extension == 'yaml':
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    elif extension == 'geojson':
        with open(path, 'w') as f:
            f.write(data)
    ##
    else:
        _msg = "*** Please check the extension."
        raise Exception(_msg)
    ##
    if echo:
        time_now = datetime.datetime.now()
        time_now_form = time_now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"-. path saved [{time_now_form}]: {path}")

# %%
## to write a image file (.tiff)
def _write_tiff(
        path: str,
        image: np.ndarray,
        channel_names: list[str] | None = None,
        **kwargs
) -> None:
    """
    a function to write a image file (.tiff)
    Args:
        path: str # output path
        image: np.ndarray # image array (CYX for multi-channel, YX for single)
        channel_names: list[str] | None = None # channel names for OME metadata
    Returns: None
    """
    if len(image.shape) == 3 and image.shape[2] in [3, 4]:
        _msg = f"*** davotools.io._write_tiff(): RGB/RGBA images (YXC) are not supported."
        _msg += f" Use jpg/png instead."
        raise ValueError(_msg)
    if len(image.shape) > 2:
        if channel_names is None:
            tifffile.imwrite( path, image, metadata={
                'axes': 'CYX',
            }, ome=True, **kwargs )
        else:
            tifffile.imwrite( path, image, metadata={
                'axes': 'CYX', 'Channel': {'Name': channel_names},
            }, ome=True, **kwargs )
    else:
        tifffile.imwrite(path, image, **kwargs)

# %%

# %% [markdown]
## Body: module

# %%
## to import a module from a source code
def import_module_from_code(
        name: str,
        path: str,
) -> types.ModuleType:
    """
    a function to import a module from a source code
    Args:
        name: str # the name of the module
        path: str # a source code path of the module
    Returns:
        module: types.ModuleType
    """
    if not os.path.exists(path):
        _msg = f"*** davotools.module.import_module_from_code(): no such {path}"
        raise ValueError(_msg)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ##
    return module

# %%

# %% [markdown]
## Body: cli

# %%
## to load command line interface inputs
def load_cli(
        parser: argparse.ArgumentParser,
        in_IPy: bool,
) -> dict:
    """
    a function to load command line interface inputs
    Args:
        parser: argparse.ArgumentParser # cli arguments
        in_IPy: bool # whether being inside an IPython interface
    Returns:
        cli: dict
    """
    ##
    cli = parser.parse_args() if not in_IPy \
        else parser.parse_args("") # for Jupyter interface
    cli = vars(cli)
    return cli

# %%

