# Multi Entity Report

CLI utility for performing 'entity report'-like search on an entire GoldSrc maps directory.

Output is a list of BSP files containing the entities matching the search query.<br>
Each BSP will have its own list of the matching entities by their classnames,
index in the entity lump, and targetname if it has one.

## Usage

Call the script in a commandline followed by the path to a maps directory,
and one or more arguments defining the search query.

The following arguments are available for building a search query.
Using them more than once builds a list of possible terms to match against,
i.e. `-k targetname -v my_entity1 -v my_entity2` will match any entity whose targetname is *either* my_entity1 or my_entity2.

By default a partial match is used for classnames, keys and values,
only the beginning of each field need to match the query
(meaning the classname query "monster_alien" will match "monster_alien_controller", "monster_alien_grunt" and "monster_alien_slave").<br>
One can change this by using `--exact` for whole term matches only.

| Argument         | Description                        |
| ---------------- | ---------------------------------- |
| -c, --classname  | Classnames that must match         |
| -k, --key        | Keys that must match               |
| -v, --value      | Values that must match             |
| -f, --flags      | Spawnflags that must match (ALL must match unless --flags_or is used) |
| -o, --flags_or   | Change spawnflag check mode to ANY |
| -e, --exact      | Matches must be exact (whole term) |

### Example

```cli
python mer.py C:/Steam/Steamapps/common/Half-Life/valve/maps -c monster_gman -v argument
```

Will result in

```txt
c1a0.bsp: [
  monster_gman (index 54, targetname 'argumentg')
]
```

### Spawnflags

The `--flags` argument will by default match entities that have all the
specified spawnflags enabled, i.e. `-f 2 -f 8` will only match entities that have
both the second (2) and fourth (8) spawnflags enabled.

All `--flags` arguments are bitwise OR'd together,
which means `-f 1 -f 4` is equivalent to `-f 5`.

Using the `--flags_or` argument changes the spawnflags check to ANY mode.
This means only one of the specified spawnflags must be enabled to match.
