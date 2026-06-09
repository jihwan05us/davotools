# %% [markdown]
## Header

# %%
## imports
import datetime, os
##
import yaml

# %%

# %% [markdown]
## Body

# %%
## to scan a directory into a nested dict of subdirs and files
def scan(
        path: str,
) -> dict:
    """
    a function to scan a directory into a nested dict of subdirs and files
    Args:
        path: str # path to the directory to scan
    Returns:
        result: dict # nested dict; files listed under '_files' key
    """
    result = {}
    entries = sorted( os.listdir(path) )
    files = [ e for e in entries if os.path.isfile( os.path.join(path, e) ) ]
    dirs = [ e for e in entries if os.path.isdir( os.path.join(path, e) ) ]
    if files:
        result['_files'] = files
    for d in dirs:
        result[d] = scan( os.path.join(path, d) )
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

if __name__ == '__main__':

    # %%
    ## imports
    import argparse

    # %%
    ## CLI
    parser = argparse.ArgumentParser(
        description="snapshot a directory tree into a YAML file" )
    parser.add_argument(
        'path', type=str, nargs='?', default=None,
        help="directory to snapshot (default: current working directory)" )
    CLI = vars( parser.parse_args() )

    # %%
    ## resolve path
    if CLI['path'] is not None:
        target = os.path.expanduser( CLI['path'] )
    else:
        target = os.getcwd()

    # %%
    ## build snapshot
    date = datetime.datetime.now().strftime('%Y%m%d')
    version = _next_version(target, date)
    result = scan(target)

    # %%
    ## write
    filename = f"snapshot--{date}-{version}.yaml"
    out_path = os.path.join(target, filename)
    with open(out_path, 'w') as f:
        yaml.dump(
            result, f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    print(f"-. written: {out_path}")

# %%

