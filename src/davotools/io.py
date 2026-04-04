# %% [markdown]
## Header

# %%
## imports
import argparse, datetime, json, os, pickle, types
import xml.etree.ElementTree
##
import geojson, tifffile, yaml
import importlib.util
import PIL.Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    extension = path.split('.')[-1]
    ##
    if extension is None:
        msg = "*** davotools.io.read(): an input path with unassigned extension"
        raise Exception(msg)
    ##
    elif extension == 'pkl':
        with open(path, 'rb') as f:
            data = pickle.load(f, **kwargs)
    elif extension == 'npy':
        with open(path, 'rb') as f:
            data = np.load(f, **kwargs)
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
        data = plt.imread(path, **kwargs)
    elif extension in ['tiff', 'tif', 'qptiff']:
        data = tifffile.imread(path, **kwargs)
    ##
    elif extension == 'json':
        with open(path, 'r') as f:
            data = json.load(f, **kwargs)
    elif extension in ['yaml', 'yml']:
        with open(path, 'r') as f:
            data = yaml.safe_load(f, **kwargs)
    elif extension == 'geojson':
        with open(path, 'r') as f:
            data = geojson.load(f, **kwargs)
    elif extension == 'annotations':
            data = xml.etree.ElementTree.parse(path, **kwargs)
    ##
    else:
        msg = "*** Please check the extension."
        raise Exception(msg)
    ##
    if echo:
        print(f"-. path loaded: {path}")
    return data

# %%
## to write data into a file
##
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
    path_dir = path.split('/')
    path_dir = '/'.join( path_dir[:-1] )
    os.makedirs(path_dir, exist_ok=True)
    ##
    file = path.split('/')[-1]
    extension = file.split('.')[-1]
    ##
    if extension is None:
        msg = "*** davotools.io.write(): an output path with unassigned extension"
        raise Exception(msg)
    ##
    elif extension == 'pkl':
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    elif extension == 'npy':
        with open(path, 'wb') as f:
            np.save(f, data)
    ##
    elif extension == 'csv':
        data.to_csv(path, **kwargs)
    elif extension == 'tsv':
        data.to_csv(path, sep='\t', **kwargs)
    ##
    elif extension in ['jpeg', 'jpg']:
        plt.imsave(path, data)
    elif extension == 'png':
        plt.imsave(path, data)
    elif extension in ['tiff', 'tif']:
        _write_tiff(path, data, **kwargs)
    ##
    elif extension == 'json':
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    elif extension == 'yaml':
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    elif extension == 'geojson':
        with open(path, 'w') as f:
            f.write(data)
    ##
    else:
        msg = "*** Please check the extension."
        raise Exception(msg)
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
        channels: list[str] | None = None,
        **kwargs
) -> None:
    """
    a function to write a image file (.tiff)
    Args:
        path: str # output path
        image: np.ndarray # image array (CYX for multi-channel, YX for single)
        channels: list[str] | None = None # channel names for OME metadata
    Returns: None
    """
    if len(image.shape) > 2:
        if channels is None:
            tifffile.imwrite( path, image, metadata={
                'axes': 'CYX',
            }, ome=True, **kwargs )
        else:
            tifffile.imwrite( path, image, metadata={
                'axes': 'CYX', 'Channel': { 'Name': channels, },
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
        msg = f"*** davotools.module.import_module_from_code(): no such {path}"
        raise ValueError(msg)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ##
    return module

# %%

# %%
