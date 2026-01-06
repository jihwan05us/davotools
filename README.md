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

Here are headers of functions in davotools. Example codes will be updated soon.

```python
## to convert: from a geojson file path a numpy array (mask)
davotools.convert.from_geojson_to_numpy(
        path: str, # a path to geojson object
        size: tuple[int, int] = None, # the size of a mask (vertical*horizontal)
) -> np.ndarray[bool]:
## to display: a list
davotools.display.view_list(
        l: list, # a list
        k: str = None, # a keyword describing 'l'
) -> None:
## to display: a dict
davotools.display.view_dict(
        d: dict, # a dictionary
        k: str = None, # a keyword describing 'd'
        i: int = 0, # a layer index for checking depth
) -> None:
## to display: a pandas table
davotools.display.view_pd(
        table: pd.DataFrame, # a pandas table
        k: str = None, # a keyword describing 'table'
        iloc: list[int] = [0,1,-1], # a location index
) -> None:
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
