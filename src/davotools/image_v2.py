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
##
try:
    from IPython.display import display
except ImportError:
    display = print

# %%
## additional imports
import geojson
import shapely.geometry
import skimage.draw

# %%

# %% [markdown]
## Body: annotation

# %%
## to convert a geojson object into shapely objects
def convert_geojson_to_shapely(
        G: geojson.FeatureCollection,
) -> tuple[ pd.DataFrame, dict ]:
    """
    a function to convert a geojson object into shapely objects
    Args:
        G: geojson.FeatureCollection # a geojson object imported by geojson.load()
    Returns:
        info: pd.DataFrame # information of every annotation
        shapes: dict[int, shapely.geometry] # shapely objects keyed by feat_index (1-based)
    """
    info = pd.DataFrame( columns=[
        'feat_index', 'feat_type', 'feat_id',
        'geo_type', 'prop_type', 'prop_name', 'prop_class',
    ] )
    shapes = {}
    ##
    for i0, v0 in enumerate( G['features'] ):
        feat_index = i0 + 1
        feat = v0
        feat_type = feat['type'] if 'type' in feat.keys() else None
        feat_id = feat['id'] if 'id' in feat.keys() else None
        geo = feat['geometry'] if 'geometry' in feat.keys() else None
        prop = feat['properties'] if 'properties' in feat.keys() else None
        ##
        geo_type = geo['type'] if 'type' in geo.keys() else None
        ##
        prop_type = prop['objectType'] if 'objectType' in prop.keys() else None
        prop_name = prop['name'] if 'name' in prop.keys() else None
        prop_class = ( prop['classification']['name']
            if 'classification' in prop.keys()
            else None )
        ##
        info_new = {
            'feat_index': feat_index,
            'feat_type':  feat_type,
            'feat_id':    feat_id,
            'geo_type':   geo_type,
            'prop_type':  prop_type,
            'prop_name':  prop_name,
            'prop_class': prop_class,
        }
        info.loc[ len(info) ] = info_new
        shapes[feat_index] = shapely.geometry.shape(geo)
    ##
    return info, shapes

# %%
## internal: fill a single shapely Polygon into a mask array
def _fill_polygon(
        mask: np.ndarray,
        poly: shapely.geometry.Polygon,
        feat_index: int,
) -> None:
    """
    an internal function to fill a shapely Polygon into a mask array.
    Exterior ring is filled with feat_index; interior rings (holes) are filled with 0.
    Args:
        mask: np.ndarray # (H, W) int array, modified in place
        poly: shapely.geometry.Polygon
        feat_index: int # value to write for the exterior
    Returns: None
    """
    ## exterior ring
    ## GeoJSON coords are (x, y) = (col, row)
    coords = np.array(poly.exterior.coords)
    rows = coords[:, 1]
    cols = coords[:, 0]
    rr, cc = skimage.draw.polygon(rows, cols, shape=mask.shape)
    mask[rr, cc] = feat_index
    ##
    ## interior rings (holes): reset to background (0)
    for interior in poly.interiors:
        coords_h = np.array(interior.coords)
        rows_h = coords_h[:, 1]
        cols_h = coords_h[:, 0]
        rr_h, cc_h = skimage.draw.polygon(rows_h, cols_h, shape=mask.shape)
        mask[rr_h, cc_h] = 0

# %%
## to convert shapely objects into a numpy array (mask)
def convert_shapely_to_numpy(
        size: tuple[int, int],
        info: pd.DataFrame,
        shapes: dict,
) -> np.ndarray:
    """
    a function to convert shapely objects into a numpy array (mask)
    Args:
        size: tuple[int, int] # the size of the mask (H, W)
        info: pd.DataFrame # output from convert_geojson_to_shapely
        shapes: dict # output from convert_geojson_to_shapely
    Returns:
        mask: np.ndarray # integer mask (stores feat_index per pixel)
    """
    mask = np.zeros(size, dtype=int)
    ##
    for _, info_row in tqdm( info.iterrows(), total=info.shape[0], ncols=50 ):
        feat_index = info_row['feat_index']
        shape = shapes[feat_index]
        ##
        if isinstance(shape, shapely.geometry.Polygon):
            _fill_polygon(mask, shape, feat_index)
        elif isinstance(shape, shapely.geometry.MultiPolygon):
            for poly in shape.geoms:
                _fill_polygon(mask, poly, feat_index)
    ##
    return mask

# %%
## worker for convert_multi_shapely_to_numpy
def _convert_multi_shapely_to_numpy_worker(args):
    feat_index, shape, size = args
    exterior_list = []
    hole_list = []
    ##
    polys = list(shape.geoms) if isinstance(shape, shapely.geometry.MultiPolygon) else [shape]
    for poly in polys:
        coords = np.array(poly.exterior.coords)
        rr, cc = skimage.draw.polygon(coords[:, 1], coords[:, 0], shape=size)
        exterior_list.append((rr, cc))
        ##
        for interior in poly.interiors:
            coords_h = np.array(interior.coords)
            rr_h, cc_h = skimage.draw.polygon(coords_h[:, 1], coords_h[:, 0], shape=size)
            hole_list.append((rr_h, cc_h))
    ##
    return feat_index, exterior_list, hole_list

# %%
## to convert shapely objects into a numpy array (mask) using multiprocessing
def convert_multi_shapely_to_numpy(
        size: tuple[int, int],
        info: pd.DataFrame,
        shapes: dict,
        cpu_max: int | None = None,
) -> np.ndarray:
    """
    a function to convert shapely objects into a numpy array (mask) using multiprocessing
    Args:
        size: tuple[int, int] # the size of the mask (H, W)
        info: pd.DataFrame # output from convert_geojson_to_shapely
        shapes: dict # output from convert_geojson_to_shapely
        cpu_max: int | None = None # the maximum number of cpu cores for multiprocessing
    Returns:
        mask: np.ndarray # integer mask (stores feat_index per pixel)
    """
    mask = np.zeros(size, dtype=np.int64)
    ##
    cpus_all = os.cpu_count()
    cpus_use = max( min(cpu_max, cpus_all - 1), 1 ) if cpu_max is not None else cpus_all
    print(f"-. (cpus_all, cpus_use) = ({cpus_all}, {cpus_use})")
    ##
    args = [
        ( int(row['feat_index']), shapes[ int(row['feat_index']) ], size )
        for _, row in info.iterrows()
    ]
    ##
    with multiprocessing.Pool(cpus_use) as pool:
        results = pool.map(_convert_multi_shapely_to_numpy_worker, args)
    ##
    for feat_index, exterior_list, hole_list in results:
        for rr, cc in exterior_list:
            mask[rr, cc] = feat_index
        for rr, cc in hole_list:
            mask[rr, cc] = 0
    ##
    return mask

# %%
## to convert a geojson file path into a numpy array (mask)
def convert_geojson_to_numpy(
        path: str,
        size: tuple[int, int],
        multi: int | bool = True,
) -> tuple[ pd.DataFrame, np.ndarray ]:
    """
    a function to convert a geojson file path into a numpy array (mask)
    Args:
        path: str # a path to geojson object
        size: tuple[int, int] # the size of a numpy mask (H, W)
        multi: int | bool = True # bool to toggle multiprocessing; int to set cpu count (bool checked first as bool is subclass of int)
    Returns:
        info: pd.DataFrame # information of every annotation
        mask: np.ndarray # integer mask (stores feat_index per pixel)
    """
    with open(path) as f:
        G = geojson.load(f)
    ##
    info, shapes = convert_geojson_to_shapely(G)
    if isinstance(multi, bool):
        if multi is True:
            mask = convert_multi_shapely_to_numpy( size, info, shapes, max( 1, os.cpu_count() - 1 ) )
        else:
            mask = convert_shapely_to_numpy(size, info, shapes)
    elif isinstance(multi, int):
        mask = convert_multi_shapely_to_numpy(size, info, shapes, multi)
    else:
        msg = f"*** the core count for multiprocessing is not well defined!!!"
        raise ValueError(msg)
    ##
    return info, mask

# %%

# %% [markdown]
## Body: patch

# %%
## to generate equal length subintervals from a 1d interval
def generate_subinterval_1d_centered(
        interval: tuple[int,int],
        size: int = 256,
        frame: int = 0,
        center: int = None,
        patch_count_limit_max: int = 1000,
        echo: bool = False,
        **kwargs
) -> pd.DataFrame:
    """
    a function to generate equal length subintervals from a 1d interval
    Args:
        interval: tuple[int,int] # interval to be split into grids
        size: int = 256 # grid size
        frame: int = 0 # frame for overlap between a pair of consecutive grids
        center: int = None # origin on which grids will span out
        patch_count_limit_max: int = 1000 # ( maximum size / 2 ) of grids
        echo: bool = False # whether to print internal details
    Returns:
        grids: pd.DataFrame
            # row: each grid
            # column: each grid's lower interval, higher interval, and length
    """
    interval_min, interval_max = interval
    if center is None:
        center = int( (interval_min + interval_max) / 2 )
    frame_low = int( frame / 2 )
    frame_high = frame - frame_low
    if echo:
        print(f"-. details:")
        print(f"* {interval_min = } & {interval_max = }")
        print(f"* {center = }")
        print(f"* {frame = } & {frame_low = } & {frame_high = }")
    ##
    grids = pd.DataFrame()
    ##
    if True: # higher-side expansion from the center
        low = center - frame_low
        i = 0
        while (i < patch_count_limit_max):
            high = low + size + frame
            if (low >= high) or (low >= interval_max):
                break
            ##
            final_low = interval_min if low < interval_min else low
            final_high = interval_max if high > interval_max else high
            new = pd.Series( { 'low': final_low, 'high': final_high } )
            grids = pd.concat( [grids, new], axis=1, ignore_index=True )
            ##
            if high > interval_max:
                break
            low = high - frame
            i = i + 1
    if echo:
        display(grids)
    ##
    if True: # lower-side expansion from the center
        high = center + frame_high
        i = 0
        while (i < patch_count_limit_max):
            low = high - size - frame
            if (low >= high) or (high <= interval_min):
                break
            ##
            final_low = interval_min if low < interval_min else low
            final_high = interval_max if high > interval_max else high
            new = pd.Series( { 'low': final_low, 'high': final_high } )
            grids = pd.concat( [grids, new], axis=1, ignore_index=True )
            ##
            if low < interval_min:
                break
            high = low + frame
            i = i + 1
    if echo:
        display(grids)
    ##
    grids = grids.T
    grids = grids.sort_values( by=['low', 'high'] )
    grids = grids.reset_index(drop=True)
    grids['length'] = grids['high'] - grids['low']
    if echo:
        display(grids)
    ##
    if grids.loc[ grids['low'] == interval_min ].shape[0] > 1:
        grids = grids.iloc[1:]
    if grids.loc[ grids['high'] == interval_max ].shape[0] > 1:
        grids = grids.iloc[:-2]
    ##
    if echo:
        display(grids)
    return grids

# %%
## to generate coordinates of patches from a big image
def generate_patch_coords(
        image_size: tuple[int,int],
        patch_size: tuple[int,int],
        patch_overlap: tuple[int,int] = (0,0),
        echo: bool = False,
) -> pd.DataFrame:
    """
    a function to generate coordinates of patches from a big image
    Args:
        image_size: tuple[int,int] # the size of an entire image
        patch_size: tuple[int,int] # the wanted size of patches
        patch_overlap: tuple[int,int] = (0,0) # the size of overlapping region
        echo: bool = False # whether to print internal details
    Returns:
        coords: pd.DataFrame
            # row: each patch
            # column: coordinates (top, bottom, left, right, height, width, edge)
    """
    image_h, image_w = image_size
    patch_h, patch_w = patch_size
    overlap_h, overlap_w = patch_overlap
    ##
    center = (
        math.ceil(image_h / 2),
        math.ceil(image_w / 2)
    )
    if echo:
        print(f"-. {image_size = }")
        print(f"-. {center = }")
        print(f"-. {patch_size = }")
        print(f"-. {patch_overlap = }")
    ##
    coords_h = generate_subinterval_1d_centered( (0,image_h), patch_h, frame=overlap_h )
    coords_h.columns = ['top', 'bottom', 'height']
    if echo:
        display(coords_h)
    ##
    coords_w = generate_subinterval_1d_centered( (0,image_w), patch_w, frame=overlap_w )
    coords_w.columns = ['left', 'right', 'width']
    if echo:
        display(coords_w)
    ##
    coords = pd.DataFrame()
    for _, row_h in coords_h.iterrows():
        for _, row_w in coords_w.iterrows():
            entry = pd.concat( [row_h, row_w] )
            coords = pd.concat( [coords, entry], axis=1, ignore_index=True )
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

# %%

