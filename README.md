# davotools

### Purpose

This package is intended to organize everyday tools (utility functions in Python) of Jihwan Oh ('DavoLatte' is his WoW character name).

### Installation

Please install with the following shell command to install the package from GitHub.

```bash
pip install git@github.com:ohjihw_merck/davotools.git
```

### Loading

The package is created within a class structure.

```python
import davotools
davotools = datovools.davotools()
```

### Usage

Here are headers of functions in davotools. Please check print(*.__doc__) for details.

```python
## to convert: from a geojson file path a numpy array (mask)
davotools.convert.from_geojson_to_numpy
## to display: a list
davotools.display.view_list
## to display: a dict
davotools.display.view_dict
## to display: a pandas table
davotools.display.view_pd
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
