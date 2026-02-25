# %% [markdown]
## Header

# %%
## basic imports
import math, os
import multiprocessing
##
import numpy as np
import pandas as pd
##
from tqdm import tqdm
from IPython.display import display

# %%
## additional imports
import geojson
import shapely.geometry
import skimage.draw

# %%

# %% [markdown]
## Body: annotation

# %%
## to convert: a geojson object into shapely objects
def convert_geojson_to_shapely(
        G, # a geojson object imported by >> G = geojson.load( open(path) )
) -> tuple[ pd.DataFrame, dict, dict[ int, np.ndarray ] ]:
    """
    a function to convert: a geojson object into shapely objects
    Args:
        G, # a geojson object imported by >> G = geojson.load( open(path) )
    Returns:
        info: pd.DataFrame, # information of every annotation
        shapes: dict, # shapely objects of every annotation
        coords: dict[ int, np.ndarray ], # coordinates of every annotation
    """
    info = pd.DataFrame( columns=[
        'feat_index', 'feat_type', 'feat_id',
        'geo_type', 'prop_type', 'prop_name', 'prop_class',
    ] )
    shapes = {}
    coords = {}
    ##
    i = 0
    for i0, v0 in enumerate( G['features'] ):
        feat_index = i0
        feat = v0
        feat_type = feat['type'] if 'type' in feat.keys() else None
        feat_id = feat['id'] if 'id' in feat.keys() else None
        geo = feat['geometry'] if 'geometry' in feat.keys() else None
        prop = feat['properties'] if 'properties' in feat.keys() else None
        ##
        if True:
            geo_coord = geo['coordinates'] if 'coordinates' in geo.keys() else None
            geo_type = geo['type'] if 'type' in geo.keys() else None
        if True:
            prop_type = prop['objectType'] if 'objectType' in prop.keys() else None
            prop_name = prop['name'] if 'name' in prop.keys() else None
            prop_class = ( prop['classification']['name']
                if 'classification' in prop.keys()
                else None )
        ##
        info_new = {}
        info_new['feat_index'] = feat_index + 1
        info_new['feat_type'] = feat_type
        info_new['feat_id'] = feat_id
        info_new['geo_type'] = geo_type
        info_new['prop_type'] = prop_type
        info_new['prop_name'] = prop_name
        info_new['prop_class'] = prop_class
        shapes[feat_index] = shapely.geometry.shape(geo)
        ##
        if geo_type == 'Polygon':
            for _, v1 in enumerate( geo_coord ):
                info.loc[i] = info_new
                coords[i] = np.array(v1).astype(int)
                ##
                i = i + 1
        elif geo_type == 'MultiPolygon':
            for _, v1 in enumerate( geo_coord ):
                for _, v2 in enumerate(v1):
                    info.loc[i] = info_new
                    coords[i] = np.array(v2).astype(int)
                    ##
                    i = i + 1
        else:
            print( info_new )
    ##
    return info, shapes, coords

# %%
## to convert: shapely objects into a numpy array (mask)
def convert_shapely_to_numpy(
        size: tuple[int, int], # the size of a binary mask (vertical*horizontal)
        info: pd.DataFrame, # output from convert_geojson_shapely
        coords: dict[int, np.ndarray], # output from convert_geojson_shapely
) -> np.ndarray[bool]:
    """
    a function to convert: shapely objects into a numpy array (mask)
    Args:
        size: tuple[int, int], # the size of a binary mask (vertical*horizontal)
        info: pd.DataFrame, # output from convert_geojson_shapely
        coords: dict[int, np.ndarray], # output from convert_geojson_shapely
    Returns:
        mask: np.ndarray[bool] # binary mask of the roi
    """
    mask = np.full( size, 0, dtype=int )
    ##
    for i, info_row in tqdm( info.iterrows(), total=info.shape[0], ncols=50 ):
        coord = coords[i]
        (h, v) = skimage.draw.polygon( coord[:,0], coord[:,1] )
        ##
        for Ia, Va in enumerate(h):
            vv = v[Ia]
            hh = Va
            ##
            if ( vv < 0 ) or ( vv >= mask.shape[0] ):
                continue
            if ( hh < 0 ) or ( hh >= mask.shape[1] ):
                continue
            mask[vv, hh] = info_row['feat_index']
    ##
    return mask

# %%
## to convert (multiprocessing): shapely objects into a numpy array (mask)
def convert_multi_shapely_to_numpy(
        size: tuple[int, int], # the size of a binary mask (vertical*horizontal)
        coords: dict[int, np.ndarray], # output from convert_geojson_shapely
        cpu_max: int = None, # the maximum number of cpu cores for multiprocessing
) -> np.ndarray[bool]:
    """
    a function to convert: shapely objects into a numpy array (mask)
    Args:
        size: tuple[int, int], # the size of a binary mask (vertical*horizontal)
        coords: dict[int, np.ndarray], # output from convert_geojson_shapely
        cpu_max: int = None, # the maximum number of cpu cores for multiprocessing
    Returns:
        mask: np.ndarray[bool] # binary mask of the roi
    """
    mask = np.full( size, 0, dtype=np.int64 )
    ##
    cpus = os.cpu_count()
    cpus_use = cpus
    if cpu_max is not None:
        cpus_use = min( cpu_max, cpus-1 )
    cpus_use = max( cpus_use, 1 )
    print( f"-. total {cpus=} and {cpus_use=}" )
    ##
    with multiprocessing.Pool(cpus_use) as pool:
        results = pool.map( convert_multi_shapely_to_numpy_worker, coords.items() )
    ##
    for i, h, v in results:
        h[h<0] = 0
        h[ h >= mask.shape[1] ] = mask.shape[1] - 1
        v[v<0] = 0
        v[ v >= mask.shape[0] ] = mask.shape[0] - 1
        mask[v, h] = i
    ##
    return mask
##
def convert_multi_shapely_to_numpy_worker(coords_items):
    i, coord = coords_items
    (h, v) = skimage.draw.polygon( coord[:,0], coord[:,1] )
    return (i, h, v)

# %%
## to convert: a geojson file path into a numpy array (mask)
def convert_geojson_to_numpy(
        path: str, # a path to geojson object
        size: tuple[int, int], # the size of a numpy mask (vertical*horizontal)
        multi: bool = True, # a checker: whether to use multiprocessing
) -> tuple[ pd.DataFrame, np.ndarray[bool] ]:
    """
    a function to convert: a geojson file path into a numpy array (mask)
    Args:
        path: str, # a path to geojson object
        size: tuple[int, int], # the size of a numpy mask (vertical*horizontal)
        multi: bool = True, # a checker: whether to use multiprocessing
    Returns:
        info: pd.DataFrame, # information of every annotation
        mask: np.ndarray[bool] # a binary mask
    """
    G = geojson.load( open(path) )
    ##
    info, _, coords = convert_geojson_to_shapely(G)
    if multi == True:
        mask = convert_multi_shapely_to_numpy(size, coords)
    else:
        mask = convert_shapely_to_numpy(size, info, coords)
    ##
    return info, mask

# %%

# %% [markdown]
## Body: annotation

# %%
## to generate: equal length subintervals from a 1d interval
def generate_subinterval_1d_centered(
        range: tuple[int,int], # range to be split into grids
        size: int = 256, # grid size
        frame: int = 0, # frame for overlap between a pair of consecutive grids
        center: int = None, # origin on which grids will span out
        patch_count_limit_max: int = 1000, # ( maximum size / 2 ) of grids
        echo: bool = False,
) -> pd.DataFrame:
    """
    a function to generate: equal length subintervals from a 1d interval
    Args:
        range: tuple[int,int], # range to be split into grids
        size: int = 256, # grid size
        frame: int = 0, # frame for overlap between a pair of consecutive grids
        center: int = None, # origin on which grids will span out
        patch_count_limit_max: int = 1000, # ( maximum size / 2 ) of grids
        echo: bool = False,
    Returns:
        grids: pd.DataFrame
            # row: each grid
            # column: each grid's lower range, higher range, and length
    """
    ( min, max ) = range
    if center is None:
        center = max + min
        center = int( center / 2 )
    frame_low = int( frame / 2 )
    frame_high = frame - frame_low
    if echo:
        print( f"-. details:" )
        print( f"* {min = } & {max = }" )
        print( f"* {center = }" )
        print( f"* {frame = } & {frame_low = } & {frame_high = }" )
    ##
    grids = pd.DataFrame()
    ##
    if True: # higher-side expansion from the center
        low = center - frame_low
        i = 0
        while ( i < patch_count_limit_max ):
            high = low + size + frame
            if ( low >= high ) or ( low >= max ):
                break
            ##
            final_low = min if low < min else low
            final_high = max if high > max else high
            new = pd.Series( { 'low': final_low, 'high': final_high } )
            grids = pd.concat( [ grids, new ], axis=1, ignore_index=True )
            ##
            if high > max:
                break 
            low = high - frame
            i = i + 1
    if echo:
        display(grids)
    ##
    if True: # lower-side expansion from the center
        high = center + frame_high
        i = 0
        while ( i < patch_count_limit_max ):
            low = high - size - frame
            if ( low >= high ) or ( high <= min ):
                break
            ##
            final_low = min if low < min else low
            final_high = max if high > max else high
            new = pd.Series( { 'low': final_low, 'high': final_high } )
            grids = pd.concat( [ grids, new ], axis=1, ignore_index=True )
            ##
            if low < min:
                break 
            high = low + frame
            i = i + 1
    if echo:
        display(grids)
    ##
    grids = grids.T
    grids = grids.sort_values(by='high')
    grids = grids.sort_values(by='low')
    grids = grids.reset_index(drop=True)
    grids['length'] = grids['high'] - grids['low']
    if echo:
        display(grids)
    ##
    if grids.loc[ grids['low'] == min ].shape[0] > 1:
        grids = grids.iloc[1:]
    if grids.loc[ grids['high'] == max ].shape[0] > 1:
        grids = grids.iloc[:-2]
    ##
    if echo:
        display(grids)
    return grids

# %%
## to generate: coordinates of patches from a big image
def generate_patch_coords(
        image_size: tuple[int,int], # the size of an entire image
        patch_size: tuple[int,int], # the wanted size of patches
        patch_overlap: tuple[int,int] = (0,0), # the size of overlapping region
        echo: bool = False, # whether to display internal results
) -> pd.DataFrame:
    """
    a function to generate: coordinates of patches from a big image
    Args:
        image_size: tuple[int,int],
        patch_size: tuple[int,int],
        patch_overlap: tuple[int,int] = (0,0),
        echo: bool = False,
    Returns:
        coords: pd.DataFrame
            # row: each patch
            # column: coordinates (top, bottom, left, right, height, width, edge)
    """
    ( image_h, image_w ) = image_size
    ( patch_h, patch_w ) = patch_size
    ( overlap_h, overlap_w ) = patch_overlap
    ##
    center = (
        math.ceil( image_h / 2 ),
        math.ceil( image_w / 2 ) )
    ( center_h, center_w ) = center
    if echo:
        print( f"-. {image_size = }" )
        print( f"-. {center = }" )
        print( f"-. {patch_size = }" )
        print( f"-. {patch_overlap = }" )
    ##
    coords_h = generate_subinterval_1d_centered( (0,image_h), patch_h, frame=overlap_h )
    coords_h.columns = [ 'top', 'bottom', 'height' ]
    if echo:
        display(coords_h)
    ##
    coords_w = generate_subinterval_1d_centered( (0,image_w), patch_w, frame=overlap_w )
    coords_w.columns = [ 'left', 'right', 'width' ]
    if echo:
        display(coords_w)
    ##
    coords = pd.DataFrame()
    for _, row_h in coords_h.iterrows():
        for _, row_w in coords_w.iterrows():
            entry = pd.concat( [ row_h, row_w ] )
            coords = pd.concat( [ coords, entry ], axis=1, ignore_index=True )
    coords = coords.T
    ##
    coords['edge'] = False
    coords.loc[ coords['top'] == 0, 'edge' ] = True
    coords.loc[ coords['bottom'] == image_size[0], 'edge' ] = True
    coords.loc[ coords['left'] == 0, 'edge' ] = True
    coords.loc[ coords['right'] == image_size[1], 'edge' ] = True
    ##
    if echo:
        display(coords)
    return coords

# %%

# %% [markdown]
## Footer

