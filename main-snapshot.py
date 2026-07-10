# %% [markdown]
## Header

# %%
## imports
import argparse, datetime, os
##
import yaml
##
import davotools

# %%

# %% [markdown]
## Body

# %%
## CLI
parser = argparse.ArgumentParser(
    description="snapshot a directory tree into a YAML file" )
parser.add_argument(
    'path', type=str, nargs='?', default=None,
    help="directory to snapshot (default: current working directory)" )
parser.add_argument(
    '--exclude', type=str, nargs='*',
    default=['_backup', '_defer', '_old', '_test'],
    help="dir names to include but not recurse into" )
parser.add_argument(
    '--depth', type=int, default=None,
    help="max recursion depth (default: unlimited)" )
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
version = davotools.snapshot._next_version(target, date)
result = davotools.snapshot.scan(target, exclude=CLI['exclude'], depth=CLI['depth'])
result = { '__cwd__': target, **result }

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

