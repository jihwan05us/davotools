# davotools

### Purpose

This package is intended to organize everyday tools (utility functions in Python),
mostly for digital pathology research projects,
of Jihwan Oh ('DavoLatte' is his WoW character name).

### Installation

Please install with the following shell command to install the package from GitHub.

```bash
pip install git+https://github.com/jihwan05us/davotools.git
# pip install git+https://github.com/jihwan05us/davotools.git --force-reinstall --no-deps
```

### Loading

The package is created as a regular python package.

```python
import davotools
```

### Usage

Here are a list of functions in the package.
Please check docstrings (`print(*.__doc__)`) for details.

```python
## input & output tools
davotools.io.read
davotools.io.write
davotools.io.import_module_from_code
davotools.io.load_cli

## checking tools
davotools.view.list
davotools.view.dict
davotools.view.pd

## image analysis tools
davotools.image.convert_geojson_to_numpy
davotools.image.convert_geojson_to_shapely
davotools.image.convert_shapely_to_numpy
davotools.image.convert_multi_shapely_to_numpy
davotools.image.generate_patch_coords
davotools.image.generate_subinterval_1d_centered

## minor tools
davotools.minor.update_dict
davotools.minor.time_keep
```

### License

Copyright 2025-2026 Jihwan Oh

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

