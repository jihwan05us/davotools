# The current version

### 20260611 v0.3.0
- snapshot.py: new module; scans a directory tree into a dated YAML snapshot file
- __init__.py: import style fix (one submodule per line)

##

# Old versions of 2026

### 20260508 v0.2.1
- io.py: parquet read/write support
- pyproject.toml: pillow >> pyarrow dependency
- __init__.py: removed load_image_old(); _set_path() now silent on import
- io.py: read/write expand ~ in path

### 20260429 v0.2.0
- image.py: robust geojson handling, merged shapely-to-numpy functions, bug fix in if/else structure
- image.py: mask dtype int32, tqdm ncols=70
- io.py: dtype safety check for png/jpg, ValueError for RGB tiff, unified error types
- minor.py: ignore_None >> ignore_none
- image_old.py >> _backup/image_old--20260428.py
- style fixes across all modules

### 20260417 v0.1.1
- io.py: feather write support

### 20260408 v0.1.0b
- image.py: bug fix in convert_multi_shapely_to_numpy (mask indexed by feat_index, not loop variable)
- README.md: load_CLI >> load_cli

### 20260328 v0.1.0
- Suggestions from Claude Code are reflected.
- Some minor elements (such as doctrings) are fixed.

### 20260225 v0.0.4
- removed class structure
- multiprocessing bug fix in image.convert_geojson_to_numpy()

### 20260120 v0.0.3
- changes in module names
- ROI multiprocessing

### 20260116 v0.0.2
- to align functionality with other packages.


##

# Old versions of 2025

### 20251219 v0.0.1
- initial version uploaded into GitHub
