# %% [markdown]
## Header

# %%
## imports
import os

# %%

# %% [markdown]
## Body

# %%
## to scan a directory into a nested dict of subdirs and files
def scan(
        path: str,
        exclude: list[str] | None = ['_backup', '_defer', '_old', '_test'],
        depth: int | None = None,
        current_depth: int = 0,
) -> dict:
    """
    a function to scan a directory into a nested dict of subdirs and files
    Args:
        path: str # path to the directory to scan
        exclude: list[str] | None = ['_backup', '_defer', '_old', '_test']
            # dirs whose names match are included but not recursed into;
            # None means no exclusions
        depth: int | None = None # max recursion depth; None means unlimited
    Returns:
        result: dict # nested dict; files listed under '__files__' key
    """
    if exclude is None:
        exclude = []
    result = {}
    entries = sorted( os.listdir(path) )
    files = [ e for e in entries if os.path.isfile( os.path.join(path, e) ) ]
    dirs = [ e for e in entries if os.path.isdir( os.path.join(path, e) ) ]
    if files:
        result['__files__'] = files
    for d in dirs:
        if d in exclude:
            result[d] = {}
        elif depth is not None and current_depth >= depth:
            result[d] = {}
        else:
            result[d] = scan(
                os.path.join(path, d),
                exclude=exclude,
                depth=depth,
                current_depth=current_depth + 1,
            )
    return result

# %%
## (internal) to compute the next version integer for snapshot filename
def _next_version(
        path: str,
        date: str,
) -> int:
    """
    an internal function to compute the next version integer for snapshot filename
    Args:
        path: str # directory to check for existing snapshot files
        date: str # date string in yyyymmdd format
    Returns:
        version: int # next version integer (1-based, increments by 1)
    """
    prefix = f"snapshot--{date}-"
    existing = [
        e for e in os.listdir(path)
        if e.startswith(prefix) and e.endswith('.yaml')
    ]
    if not existing:
        return 1
    versions = []
    for e in existing:
        stem = e[ len(prefix) : -len('.yaml') ]
        if stem.isdigit():
            versions.append( int(stem) )
    if not versions:
        return 1
    return max(versions) + 1

# %%

