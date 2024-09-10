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

| Argument         | Description                        |
| ---------------- | ---------------------------------- |
| -c, --classname  | classnames that must match         |
| -k, --key        | keys that must match               |
| -v, --value      | values that must match             |
| -f, --flags      | spawnflags that must match (ALL must match unless --flags_or is used) |
| -o, --flags_or   | change spawnflag check mode to ANY |

### Spawnflags

The `--flags` argument will by default match entities that have all the
specified spawnflags enabled, i.e. `-f 2 -f 8` will only match entities that have
both the second (2) and fourth (8) spawnflags enabled.

All `--flags` arguments are bitwise OR'd together,
which means `-f 1 -f 4` is equivalent to `-f 5`.

Using the `--flags_or` argument changes the spawnflags check to ANY mode.
This means only one of the specified spawnflags must be enabled to match.
