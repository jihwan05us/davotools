# davotools

### Purpose

This package is intended to organize everyday tools (utility functions in Python),
mostly for digital pathology research projects,
of Jihwan Oh ('DavoLatte' is his WoW character name).

### Installation

Please install with the following shell command to install the package from GitHub.

```bash
pip install git+https://github.com/ohjihw_merck/davotools.git
# pip install --force-reinstall git+https://github.com/ohjihw_merck/davotools.git
```

### Loading

The package is created within a class structure.

```python
import davotools
davotools = datovools.davotools()
```

### Usage

Here are a list of functions in the package.
Please check docstrings (`print(*.__doc__)`) for details.

```python
## input & output tools
davotools.io.read
davotools.io.write
davotools.io.load_module_from_code
davotools.io.load_CLI

## checking tools
davotools.view.list
davotools.view.dict
davotools.view.pd

## image analysis tools
davotools.image.convert_geojson_to_numpy
davotools.image.generate_patch_coords
```

### License

Copyright 2026 Jihwan Oh

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

