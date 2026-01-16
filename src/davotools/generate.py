# %% [markdown]
## Header

# %%
## basic imports
import math
##
import pandas as pd
##
from IPython.display import display

# %%
##

# %% [markdown]
## Body

# %%
## to generate: equal length subintervals from a 1d interval
def subinterval_1d_centered(
        range: tuple[int,int], # range to be split into grids
        size: int = 256, # grid size
        frame: int = 0, # frame for overlap between a pair of consecutive grids
        center: int = None, # origin on which grids will span out
        patch_count_limit_max: int = 1000, # ( maximum size / 2 ) of grids
        echo: bool = False,
) -> pd.DataFrame:
    """
    a function to generate: equal length subintervals from a 1d interval
    <input>
        range: tuple[int,int], # range to be split into grids
        size: int = 256, # grid size
        frame: int = 0, # frame for overlap between a pair of consecutive grids
        center: int = None, # origin on which grids will span out
        patch_count_limit_max: int = 1000, # ( maximum size / 2 ) of grids
        echo: bool = False,
    <output>
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
def patch_coords(
        image_size: tuple[int,int], # the size of an entire image
        patch_size: tuple[int,int], # the wanted size of patches
        patch_overlap: tuple[int,int] = (0,0), # the size of overlapping region
        echo: bool = False, # whether to display internal results
) -> pd.DataFrame:
    """
    a function to generate: coordinates of patches from a big image
    <input>
        image_size: tuple[int,int],
        patch_size: tuple[int,int],
        patch_overlap: tuple[int,int] = (0,0),
        echo: bool = False,
    <output>
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
    coords_h = subinterval_1d_centered( (0,image_h), patch_h, frame=overlap_h )
    coords_h.columns = [ 'top', 'bottom', 'height' ]
    if echo:
        display(coords_h)
    ##
    coords_w = subinterval_1d_centered( (0,image_w), patch_w, frame=overlap_w )
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
##


# %% [markdown]
## Footer

# %%
##

