# %% [markdown]
## Header

# %%
## basic imports
import argparse, datetime, json, os, pickle, types, xml, yaml
##
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
## additional imports
import geojson, tifffile
import importlib.util
import PIL.Image

# %%
##

# %% [markdown]
## Body

# %%
## to read a data file
def read(
        path: str, # a path of the data file
        echo: bool = False, # a checker: whether to visualize details
        **kwargs
):
    """
    a function to read a data file
    <input>
        path: str, # a path of the data file
        echo: bool = False, # a checker: whether to visualize details
        **kwargs
    <output>
        data: (multiple format) # data object read from the file
    """
    extension = path.split('.')[-1]
    ##
    if extension is None:
        raise Exception( "*** davotools.io.read(): an input path with unassigned extension" )
    elif extension in [ 'tif', 'tiff', 'qptiff' ]:
        data = tifffile.imread( path, **kwargs )
    elif extension == 'png' :
        data = plt.imread( path, **kwargs )
    elif extension == 'csv':
        data = pd.read_csv( path, **kwargs )
    elif extension == 'tsv':
        data = pd.read_csv( path, sep='\t', **kwargs )
    elif extension in [ 'xlsx', 'xls' ]:
        data = pd.read_excel( path, **kwargs )
    elif extension == 'pkl':
        with open( path, 'rb' ) as f:
            data = pickle.load( f, **kwargs )
    elif extension == 'npy':
        with open( path, 'rb' ) as f:
            data = np.load( f, **kwargs )
    elif extension == 'json':
        with open( path, 'r' ) as f:
            data = json.load( f, **kwargs )
    elif extension in [ 'yaml', 'yml' ]:
        with open( path, 'r' ) as f:
            data = yaml.safe_load( f, **kwargs )
    elif extension == 'annotations':
            data =  xml.etree.parse( path, **kwargs )
    elif extension == 'geojson':
        with open( path, 'r' ) as f:
            data = geojson.load( f, **kwargs )
    else:
        raise Exception( "*** Please check the extension." )
    ##
    if echo:
        print( f"-. path loaded: {path}" )
    return data

# %%
## to write data into a file
##
def write(
        path: str, # a path of the file
        data, # a data to be written into a file
        echo: bool = False, # a checker: whether to visualize details
        **kwargs
) -> None:
    """
    a function to write data into a file
    <input>
        path: str, # a path of the file
        data, # a data to be written into a file
        echo: bool = False, # a checker: whether to visualize details
        **kwargs
    <output>
        None
    """
    dir = path.split('/')
    dir = '/'.join( dir[:-1] )
    os.makedirs( dir, exist_ok=True )
    ##
    file = path.split('/')[-1]
    extension = file.split('.')[-1]
    ##
    if extension is None:
        raise Exception( "*** davotools.io.write(): an output path with unassigned extension" )
    elif extension == 'pkl':
        with open( path, 'wb' ) as f:
            pickle.dump( data, f )
    elif extension == 'npy':
        with open( path, 'wb' ) as f:
            np.save( f, data )
    elif extension == 'csv':
        data.to_csv( path, **kwargs )
    elif extension == 'png':
        data.savefig(path)
    elif extension == 'jpg':
        PIL.Image.fromarray(data).save(path)
    elif extension == 'tiff':
        write_tiff( path, data, **kwargs )
    elif extension == 'json':
        with open( path, 'w') as f:
            json.dump( data, f, indent='\t' )
    elif extension == 'yaml':
        with open( path, 'w') as f:
            yaml.dump( data, f, default_flow_style=False, sort_keys=False )
    elif extension == 'geojson':
        with open( path, 'w' ) as f:
            f.write(data)
    else:
        raise Exception( "*** Please check the extension." )
    ##
    if echo:
        time_now = datetime.datetime.now()
        time_now_form = time_now.strftime( "%Y-%m-%d %H:%M:%S" )
        print( f"-. path saved [{time_now_form}]: {path}" )

# %%
## to write a image file (.tiff)
def write_tiff( path, image, channels=None, **kwargs ):
    if len( image.shape ) > 2:
        if channels is None:
            tifffile.imwrite( path, image, metadata={
                'axes': 'CYX',
            }, ome=True, **kwargs )
        else:
            tifffile.imwrite( path, image, metadata={
                'axes': 'CYX', 'Channel': { 'Name': channels, },
            }, ome=True, **kwargs )
    else:
        tifffile.imwrite( path, image, **kwargs )

# %%
##

# %% [markdown]
## Body: module

# %%
## to load a module from a source code
def load_module_from_code(
        name: str, # the name of the module
        path: str, # a source code path of the module
) -> types.ModuleType:
    """
    a function to load a module from a source code
    <input>
        name: str, # the name of the module
        path: str, # a source code path of the module
    <output>
        module: types.ModuleType
    """
    if not os.path.exists(path):
        raise ValueError( f"*** davotools.module.load_module_from_code(): no such {path}" )
    spec = importlib.util.spec_from_file_location( name, path )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ##
    return module

# %%
##

# %% [markdown]
## Body: CLI

# %%
## to load command line interface (CLI) inputs
def load_CLI(
        parser: argparse.Namespace, # CLI arguments
        in_IPy: bool # a checker of IPython interface
) -> dict:
    """
    a function to load command line interface (CLI) inputs
    <input>
        parser: argparse.Namespace, # CLI argument settings
        in_IPy: bool # a checker: whether being inside an IPython interface
    <output>
        CLI: dict
    """
    ##
    CLI = parser.parse_args() if not in_IPy \
        else parser.parse_args("") # for Jupyter interface
    CLI = vars(CLI)
    return CLI

# %%
##

# %% [markdown]
## Footer

# %%
##

