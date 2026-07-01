# davotools

**Jihwan Oh**

---

## 1. Purpose

davotools is a personal utility library for everyday Python tasks in digital pathology
research. It collects functions that appear repeatedly across projects (mIFit, CISAM,
PANDA, and others) and centralizes them in one installable package so that each project
can depend on a shared, versioned implementation rather than copying code between
repositories.

The package is organized into four submodules:

| Submodule | Contents |
|---|---|
| `davotools.io` | Reading and writing files in various formats |
| `davotools.view` | Quick terminal/Jupyter inspection of common data structures |
| `davotools.image` | GeoJSON annotation processing and image patch generation |
| `davotools.minor` | Small utilities: dict updating, elapsed-time tracking |

---

## 2. io

`io` provides a format-agnostic interface for reading and writing data files. The
caller specifies only the file path; the format is inferred from the extension. This
removes per-format boilerplate from pipeline scripts and ensures consistent handling
of edge cases (directory creation, dtype validation, OME metadata for tiff) across
all projects.

### 2.1 `read`

Reads a file and returns a Python object. The extension determines the backend:

| Extensions | Returns |
|---|---|
| `.pkl` | Arbitrary Python object (pickle) |
| `.npy` | `numpy.ndarray` |
| `.csv`, `.tsv`, `.xlsx`, `.xls` | `pandas.DataFrame` |
| `.feather`, `.parquet` | `pandas.DataFrame` |
| `.jpg`, `.jpeg`, `.png` | `numpy.ndarray` (via skimage) |
| `.tiff`, `.tif`, `.qptiff` | `numpy.ndarray` (via tifffile) |
| `.json` | `dict` / `list` |
| `.yaml`, `.yml` | `dict` / `list` |
| `.geojson` | `geojson.FeatureCollection` |
| `.annotations` | `xml.etree.ElementTree` (QuPath XML) |

`**kwargs` are forwarded to the underlying reader, allowing caller-side control (e.g.,
`index_col` for pandas, `key` for numpy).

### 2.2 `write`

Writes a Python object to a file. The same extension-driven dispatch as `read`.
Output directories are created automatically. A timestamped log line is printed when
`echo=True`.

Additional behavior by format:
- **tiff / tif**: writes multi-channel arrays in `CYX` OME-TIFF format; accepts an
  optional `channel_names` list to embed channel metadata.
- **jpg / jpeg**: raises an error if the array dtype is not `uint8` or `uint16`,
  preventing silent precision loss.
- **png**: uses `matplotlib.pyplot.imsave`, which supports float arrays and colormaps.

### 2.3 `import_module_from_code`

Loads a Python source file at an arbitrary path and returns it as a live module
object. This is useful for importing project-specific scripts (e.g., a panel config or
a custom model definition) without installing them as packages.

```python
cfg = davotools.io.import_module_from_code('config', '/path/to/config.py')
```

### 2.4 `load_cli`

Wraps `argparse.ArgumentParser.parse_args()` to work in both terminal and
IPython/Jupyter contexts. In IPython, `parse_args("")` is called instead of
`parse_args()` to avoid consuming Jupyter's internal argv. Returns a plain `dict`.

---

## 3. view

`view` provides three quick-inspection functions for common container types. All three
print a structured summary to the terminal (or Jupyter cell output via `IPython.display`
if available). They are accessed as `davotools.view.list`, `davotools.view.dict`, and
`davotools.view.pd` -- the module re-exports them under these shortened names.

An optional `k` argument labels the output with a keyword description.

### 3.1 `view.list`

Prints each element of a list with an asterisk bullet. Intended for quick enumeration
of string lists (file paths, channel names, etc.).

### 3.2 `view.dict`

Recursively traverses a nested dictionary and prints its structure with increasing
indentation per depth level. Leaf values are printed alongside the type of their parent
dict, which helps quickly identify the shape of complex config or result dicts.

### 3.3 `view.pd`

Prints the type and shape of a DataFrame, then displays a sample (first two rows and
last row by default). If the table has five or fewer rows, all rows are shown. An
`iloc` argument accepts a custom list of row indices.

---

## 4. image

`image` contains two groups of functions: annotation processing (GeoJSON to numpy mask)
and patch coordinate generation.

### 4.1 Annotation processing

The typical entry point is `convert_geojson_to_numpy`, which reads a `.geojson` file
and returns an integer mask array where each pixel holds the 1-based index of the
annotation feature it belongs to (background = 0). The two lower-level functions
`convert_geojson_to_shapely` and `convert_shapely_to_numpy` are available separately
for cases where the caller needs intermediate access to the shapely geometry objects
(e.g., to filter by annotation class before rasterizing).

#### `convert_geojson_to_numpy`

High-level wrapper. Reads the file, calls the two steps below, and returns
`(info, mask)`. If `size` is not provided, the mask dimensions are inferred from the
bounding box of all polygon vertices. Multiprocessing is configurable via `multi`:
`True` uses all CPUs minus one; an integer sets an explicit count; `False` runs
single-threaded.

#### `convert_geojson_to_shapely`

Parses a GeoJSON object (FeatureCollection, bare Feature, or bare geometry) into a
shapely geometry dict. Handles normalization so the caller does not need to inspect the
GeoJSON type. Returns:
- `info`: DataFrame with one row per feature. Columns: `feat_index` (1-based),
  `feat_type`, `feat_id`, `geo_type`, `prop_type`, `prop_name`, `prop_class`.
- `shapes`: dict mapping `feat_index` to `shapely.geometry` object.

`prop_class` is read from `properties.classification.name`, which is the field
QuPath writes for annotation classifications.

#### `convert_shapely_to_numpy`

Rasterizes a set of shapely geometries into an integer mask of shape `(H, W)`.
Supports `Polygon` and `MultiPolygon`. Polygon holes (interior rings) are reset to
background after the exterior is filled. When `cpu_max > 1`, rasterization is
parallelized over features using `multiprocessing`.

### 4.2 Patch coordinate generation

#### `generate_patch_coords`

Generates a tiling of an image into patches of a fixed size, with optional overlap.
Patches expand bidirectionally from the image center so that the center is always
covered cleanly. Returns a DataFrame with columns `top`, `bottom`, `left`, `right`,
`height`, `width`, and an `edge` flag that is `True` for patches touching any image
boundary.

| Parameter | Default | Description |
|---|---|---|
| `image_size` | -- | `(H, W)` of the full image |
| `patch_size` | -- | `(H, W)` of each patch |
| `patch_overlap` | `(0, 0)` | Overlap in pixels between adjacent patches |

#### `generate_subinterval_1d_centered`

The 1D building block used by `generate_patch_coords`. Divides a 1D interval into
equal-length sub-intervals of a given `size`, expanding bidirectionally from a center
point. An optional `frame` argument adds overlap between consecutive sub-intervals.
Boundary sub-intervals are clipped to the interval endpoints rather than discarded.
Returns a DataFrame with columns `low`, `high`, `length`.

---

## 5. minor

### 5.1 `update_dict`

Returns a shallow copy of `orig` updated with values from `new`. When
`ignore_none=True`, keys in `new` with `None` values are skipped, preserving the
original value for those keys. The original dict is never modified.

This is useful for merging default parameter dicts with caller-supplied overrides,
especially when the caller may omit some keys by passing `None`.

### 5.2 `time_keep`

A two-call timing utility. The first call (no argument) records and prints the start
time and returns the `datetime` object. The second call (passing the start time)
records the end time, prints both the end time and the elapsed duration, and returns
the end `datetime`.

```python
t = davotools.minor.time_keep() # prints start time
# ... work ...
davotools.minor.time_keep(t) # prints end time and elapsed
```

`echo=False` suppresses all printing while still returning the datetime, useful for
capturing timing in automated pipelines without cluttering stdout.
