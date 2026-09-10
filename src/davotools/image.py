# %% [markdown]
## Header

# %%
## imports
import math, multiprocessing, os
##
import geojson
import rasterio.features
import rasterio.transform
import shapely.geometry
import shapely.ops
import skimage.draw
import numpy as np
import pandas as pd
from tqdm import tqdm
try:
    from IPython.display import display
except ImportError:
    display = print

# %%

# %% [markdown]
## Body: thumbnail

# %%
## to stretch a 2d grayscale image array to uint8 for display
def thumb(image: np.ndarray, skip: int = 1) -> np.ndarray:
    """
    a function to stretch a 2d grayscale image array to uint8 for display.
    Uses 1st-99th percentile clipping. For multichannel images, use
    thumb_rgb or thumb_multi instead.
    Args:
        image: np.ndarray # 2d input array of any numeric dtype
        skip: int = 1 # spatial downsampling stride; <=1 means no downsampling
    Returns:
        out: np.ndarray # uint8 array with values in [0, 255]
    """
    if skip > 1:
        image = image[::skip, ::skip]
    ch = image.astype(float)
    lo, hi = np.percentile(ch, [1, 99])
    if hi == lo:
        out = np.zeros_like(ch, dtype=np.uint8)
    else:
        out = (ch - lo) / (hi - lo) * 255
        out = np.clip(out, 0, 255)
        out = out.astype(np.uint8)
    return out

# %%
## to stretch an RGB image to uint8 for display, per channel
def thumb_rgb(
        image: np.ndarray,
        channel_dim: int = 2,
        skip: int = 1,
) -> np.ndarray:
    """
    a function to stretch an RGB image to uint8 for display, per channel.
    Applies thumb independently to each channel. RGB channel is typically
    at the 3rd dimension (channel_dim=2), i.e. (H, W, 3).
    Args:
        image: np.ndarray # RGB array of any numeric dtype
        channel_dim: int = 2 # axis along which channels are stored
        skip: int = 1 # spatial downsampling stride; <=1 means no downsampling
    Returns:
        out: np.ndarray # uint8 array with same shape as input
    """
    if skip > 1:
        slices = tuple( slice(None) if i == channel_dim else slice(None, None, skip)
                        for i in range(image.ndim) )
        image = image[slices]
    n = image.shape[channel_dim]
    channels = [
        thumb( np.take(image, c, axis=channel_dim) )
        for c in range(n)
    ]
    return np.stack(channels, axis=channel_dim)

# %%
## to stretch a multichannel image to uint8 for display, per channel
def thumb_multi(
        image: np.ndarray,
        channel_dim: int = 0,
        skip: int = 1,
) -> np.ndarray:
    """
    a function to stretch a multichannel image to uint8 for display,
    per channel. Applies thumb independently to each channel.
    Multichannel images typically have channels at the 1st dimension
    (channel_dim=0), i.e. (C, H, W).
    Args:
        image: np.ndarray # multichannel array of any numeric dtype
        channel_dim: int = 0 # axis along which channels are stored
        skip: int = 1 # spatial downsampling stride; <=1 means no downsampling
    Returns:
        out: np.ndarray # uint8 array with same shape as input
    """
    if skip > 1:
        slices = tuple( slice(None) if i == channel_dim else slice(None, None, skip)
                        for i in range(image.ndim) )
        image = image[slices]
    n = image.shape[channel_dim]
    channels = [
        thumb( np.take(image, c, axis=channel_dim) )
        for c in range(n)
    ]
    return np.stack(channels, axis=channel_dim)

# %%

# %% [markdown]
## Body: annotation

# %%
## to convert a geojson object into shapely objects
def convert_geojson_to_shapely(
        G,
        geo_types: list[str] | None = None,
) -> tuple[pd.DataFrame, dict]:
    """
    a function to convert a geojson object into shapely objects.
    Handles FeatureCollection, bare Feature, and bare geometry.
    Args:
        G # a geojson object imported by geojson.load()
        geo_types: list[str] | None = None
            # if provided, only features with matching geo_type are included
    Returns:
        info: pd.DataFrame # information of every annotation
        shapes: dict[int, shapely.geometry]
            # shapely objects keyed by feat_index (1-based)
    """
    ## normalize input to a list of features
    if hasattr(G, 'features'):
        features = G['features']
    elif hasattr(G, 'geometry'):
        features = [G]
    else:
        features = [ { 'type': 'Feature', 'geometry': G, 'properties': {} } ]
    ##
    info = pd.DataFrame( columns=[
        'feat_index', 'feat_type', 'feat_id',
        'geo_type', 'prop_type', 'prop_name', 'prop_class',
    ] )
    shapes = {}
    ##
    for i0, feat in enumerate(features):
        feat_index = i0 + 1
        feat_type = feat['type'] if 'type' in feat.keys() else None
        feat_id = feat['id'] if 'id' in feat.keys() else None
        geo = feat['geometry'] if 'geometry' in feat.keys() else None
        prop = feat['properties'] if 'properties' in feat.keys() else None
        ##
        geo_type = (
            geo['type'] if geo is not None and 'type' in geo.keys() else None
        )
        if geo_types is not None:
            if geo_type not in geo_types:
                continue
        ##
        prop_type = (
            prop['objectType']
            if prop is not None and 'objectType' in prop.keys() else None
        )
        prop_name = (
            prop['name'] if prop is not None and 'name' in prop.keys() else None
        )
        prop_class = (
            prop['classification']['name']
            if prop is not None and 'classification' in prop.keys() else None
        )
        ##
        info_new = {
            'feat_index': feat_index,
            'feat_type': feat_type,
            'feat_id': feat_id,
            'geo_type': geo_type,
            'prop_type': prop_type,
            'prop_name': prop_name,
            'prop_class': prop_class,
        }
        info.loc[ len(info) ] = info_new
        shapes[feat_index] = shapely.geometry.shape(geo)
    ##
    return info, shapes

# %%
## (internal) to fill a single shapely Polygon into a mask array
def _fill_polygon(
        mask: np.ndarray,
        poly: shapely.geometry.Polygon,
        feat_index: int,
) -> None:
    """
    an internal function to fill a shapely Polygon into a mask array.
    Exterior ring is filled with feat_index; interior rings (holes) are
    filled with 0.
    Args:
        mask: np.ndarray # (H, W) int array, modified in place
        poly: shapely.geometry.Polygon
        feat_index: int # value to write for the exterior
    Returns: None
    """
    ## exterior ring; GeoJSON coords are (x, y) = (col, row)
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
## (internal) to rasterize a single shapely shape into pixel index lists
def _convert_shapely_to_numpy_worker(args: tuple) -> tuple:
    feat_index, shape, size = args
    exterior_list = []
    hole_list = []
    ##
    polys = (
        list( shape.geoms ) if isinstance(shape, shapely.geometry.MultiPolygon)
        else [shape]
    )
    for poly in polys:
        coords = np.array(poly.exterior.coords)
        rr, cc = skimage.draw.polygon(coords[:, 1], coords[:, 0], shape=size)
        exterior_list.append((rr, cc))
        ##
        for interior in poly.interiors:
            coords_h = np.array(interior.coords)
            rr_h, cc_h = skimage.draw.polygon(
                coords_h[:, 1], coords_h[:, 0], shape=size
            )
            hole_list.append((rr_h, cc_h))
    ##
    return feat_index, exterior_list, hole_list

# %%
## to convert shapely objects into a numpy array (mask)
def convert_shapely_to_numpy(
        size: tuple[int, int],
        info: pd.DataFrame,
        shapes: dict,
        cpu_max: int | None = None,
        backend: str = 'rasterio',
) -> np.ndarray:
    """
    a function to convert shapely objects into a numpy array (mask)
    Args:
        size: tuple[int, int] # the size of the mask (H, W)
        info: pd.DataFrame # output from convert_geojson_to_shapely
        shapes: dict # output from convert_geojson_to_shapely
        cpu_max: int | None = None # max cpu cores; None or 1 = single-core (skimage only)
        backend: str = 'rasterio' # 'rasterio' or 'skimage'
    Returns:
        mask: np.ndarray # integer mask (stores feat_index per pixel)
    """
    if backend == 'rasterio':
        geom_val_pairs = [
            (shapes[row['feat_index']], int(row['feat_index']))
            for _, row in info.iterrows()
        ]
        if len(geom_val_pairs) == 0:
            return np.zeros(size, dtype=np.int32)
        mask = rasterio.features.rasterize(
            geom_val_pairs,
            out_shape=size,
            transform=rasterio.transform.Affine(1, 0, 0, 0, 1, 0),
            dtype=np.int32,
        )
        return mask
    ##
    mask = np.zeros(size, dtype=np.int32)
    if cpu_max is None or cpu_max <= 1:
        ITER = tqdm( info.iterrows(), total=info.shape[0], ncols=70 )
        for _, info_row in ITER:
            feat_index = info_row['feat_index']
            shape = shapes[feat_index]
            ##
            if isinstance(shape, shapely.geometry.Polygon):
                _fill_polygon(mask, shape, feat_index)
            elif isinstance(shape, shapely.geometry.MultiPolygon):
                for poly in shape.geoms:
                    _fill_polygon(mask, poly, feat_index)
    else:
        cpus_all = os.cpu_count() or 1
        cpus_use = max( min(cpu_max, cpus_all - 1), 1 )
        print(f"-. (cpus_all, cpus_use) = ({cpus_all}, {cpus_use})")
        ##
        args = [
            ( row['feat_index'], shapes[ row['feat_index'] ], size )
            for _, row in info.iterrows()
        ]
        ##
        with multiprocessing.get_context('fork').Pool(cpus_use) as pool:
            ITER = tqdm(
                pool.imap( _convert_shapely_to_numpy_worker, args ),
                total=len(args), ncols=70,
            )
            results = list(ITER)
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
        size: tuple[int, int] | None = None,
        multi: int | bool = True,
        geo_types: list[str] | None = None,
        **kwargs,
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    a function to convert a geojson file path into a numpy array (mask)
    Args:
        path: str # a path to geojson object
        size: tuple[int, int] | None = None # the size of a numpy mask (H, W);
            if None, auto-determined from polygon bounds
        multi: int | bool = True # bool to toggle multiprocessing;
            int to set cpu count (bool checked first as bool is subclass of int)
        geo_types: list[str] | None = None
            # if provided, only features with matching geo_type are included
        **kwargs: any # passed to convert_shapely_to_numpy (e.g. backend='skimage')
    Returns:
        info: pd.DataFrame # information of every annotation
        mask: np.ndarray # integer mask (stores feat_index per pixel)
    """
    with open(path) as f:
        G = geojson.load(f)
    ##
    info, shapes = convert_geojson_to_shapely(G, geo_types=geo_types)
    ##
    if size is None:
        union = shapely.ops.unary_union( list( shapes.values() ) )
        _, _, maxx, maxy = union.bounds
        size = ( int(maxy) + 1, int(maxx) + 1 )
    ##
    if isinstance(multi, bool):
        cpu_max = max( 1, (os.cpu_count() or 1) - 1 ) if multi is True else 1
    elif isinstance(multi, int):
        cpu_max = multi
    else:
        _msg = "*** the core count for multiprocessing is not well defined"
        raise ValueError(_msg)
    mask = convert_shapely_to_numpy(size, info, shapes, cpu_max, **kwargs)
    ##
    return info, mask

# %%

# %% [markdown]
## Body: patch

# %%
## to generate equal length subintervals from a 1d interval
def generate_subinterval_1d_centered(
        interval: tuple[int, int],
        size: int = 256,
        frame: int = 0,
        center: int | None = None,
        patch_count_limit_max: int = 1000,
        echo: bool = False,
) -> pd.DataFrame:
    """
    a function to generate equal length subintervals from a 1d interval
    Args:
        interval: tuple[int, int] # interval to be split into grids
        size: int = 256 # grid size
        frame: int = 0 # frame for overlap between a pair of consecutive grids
        center: int | None = None # origin on which grids will span out
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
        print(f"-. {interval_min = } & {interval_max = }")
        print(f"-. {center = }")
        print(f"-. {frame = } & {frame_low = } & {frame_high = }")
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
        image_size: tuple[int, int],
        patch_size: tuple[int, int],
        patch_overlap: tuple[int, int] = (0, 0),
        echo: bool = False,
) -> pd.DataFrame:
    """
    a function to generate coordinates of patches from a big image
    Args:
        image_size: tuple[int, int] # the size of an entire image
        patch_size: tuple[int, int] # the wanted size of patches
        patch_overlap: tuple[int, int] = (0, 0) # the size of overlapping region
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
    coords_h = generate_subinterval_1d_centered(
        (0, image_h), patch_h, frame=overlap_h,
    )
    coords_h.columns = ['top', 'bottom', 'height']
    if echo:
        display(coords_h)
    ##
    coords_w = generate_subinterval_1d_centered(
        (0, image_w), patch_w, frame=overlap_w,
    )
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

