# %% [markdown]
## Header

# %%
## basic imports
import numpy as np
import pandas as pd
##
from tqdm import tqdm

# %%
## additional imports
import geojson
import shapely.geometry
import skimage.draw

# %%
##

# %% [markdown]
## Body

# %%
## to convert: from a geojson object to shapely objects
def from_geojson_to_shapely(
        G, # a geojson object imported by >> G = geojson.load( open(path) )
) -> tuple[ pd.DataFrame, dict, dict[ int, np.ndarray ] ]:
    """
    <input>
        G, # a geojson object imported by >> G = geojson.load( open(path) )
    <output>
        info: pd.DataFrame, # information of every annotation
        shapes: dict # shapely objects of every annotation
        coords: dict[ int, np.ndarray ] # coordinates of every annotation
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
        info_new['feat_index'] = feat_index
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
## to convert: from shapely objects to a numpy array (mask)
def from_shapely_to_numpy(
        size: tuple[int, int], # the size of a binary mask (vertical*horizontal)
        info: pd.DataFrame, # output from convert_geojson_shapely
        coords: dict[int, np.ndarray], # output from convert_geojson_shapely
) -> np.ndarray[bool]:
    """
    <input>
        size: tuple[int, int], # the size of a binary mask (vertical*horizontal)
        info: pd.DataFrame, # output from convert_geojson_shapely
        coords: dict[int, np.ndarray], # output from convert_geojson_shapely
    <output>
        mask: np.ndarray[bool] # binary mask of the roi
    """
    mask = np.full(size, False)
    ##
    for i, _ in tqdm( info.iterrows(), total=info.shape[0], ncols=50 ):
        coord = coords[i]
        ( h, v ) = skimage.draw.polygon( coord[:,0], coord[:,1] )
        ##
        for Ia, Va in enumerate(h):
            vv = v[Ia]
            hh = Va
            ##
            if ( vv < 0 ) or ( vv >= mask.shape[0] ):
                continue
            if ( hh < 0 ) or ( hh >= mask.shape[1] ):
                continue
            mask[ vv, hh ] = True
    ##
    return mask

# %%
## to convert: from a geojson file path a numpy array (mask)
def from_geojson_to_numpy(
        path: str, # a path to geojson object
        size: tuple[int, int] = None, # the size of a numpy mask (vertical*horizontal)
) -> np.ndarray[bool]:
    """
    <input>
        path: str, # a path to geojson object
        size: tuple[int, int] = None, # the size of a numpy mask (vertical*horizontal)
    <output>
        mask: np.ndarray[bool] # a binary mask
    """
    G = geojson.load( open(path) )
    ##
    info, _, coords = from_geojson_to_shapely(G)
    mask = from_shapely_to_numpy(size, info, coords)
    ##
    return info, mask

# %%
##

# %% [markdown]
## Footer

# %%
##

