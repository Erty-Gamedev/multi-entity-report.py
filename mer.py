"""
Multi Entity Report

CLI utility for performing 'entity report'-like search on an entire maps directory.
"""

import argparse
import dataclasses
from pathlib import Path
from functools import reduce
from bspentreader import BSPEntReader


@dataclasses.dataclass
class Args:
    maps: str
    classnames: list[str] = dataclasses.field(default_factory=list)
    keys: list[str] = dataclasses.field(default_factory=list)
    values: list[str] = dataclasses.field(default_factory=list)
    flags: int = 0
    flags_or: bool = False

def parse_args() -> tuple[argparse.ArgumentParser, Args]:
    argparser = argparse.ArgumentParser(
        prog='Multi Entity Report',
        description='Searches an entire maps folder for entities of specific '\
                    'classnames, keys, values, or combinations of these.'
    )
    argparser.add_argument(
        'maps', nargs='?', type=str,
        help='maps folder to search')
    argparser.add_argument(
        '--version', action='version', version="%(prog)s 1.0.0",
        help='display current version')
    
    argparser.add_argument(
        '-c', '--classname', action='append', metavar='',
        help='classnames that must match')
    
    argparser.add_argument(
        '-k', '--key', action='append', metavar='',
        help='keys that must match')
    
    argparser.add_argument(
        '-v', '--value', action='append', metavar='',
        help='values that must match')
    
    argparser.add_argument(
        '-f', '--flags', action='append', metavar='',
        help='spawnflags that must match (ALL must match unless --flags_or is used)')
    
    argparser.add_argument(
        '-o', '--flags_or', action='store_true',
        help='change spawnflag check mode to ANY')
    
    args = argparser.parse_args(
        # ['.', '-c', 'a']
        )
    flags = 0 if not args.flags else reduce(lambda a, b: int(a)|int(b), args.flags, 0)

    if not args.maps:
        argparser.print_help()
        argparser.exit(0)

    if not (args.classname or args.key or args.value or flags):
        argparser.exit(0, 'No arguments used. '\
            'Please build a search query using CLI arguments '\
            '(use --help to see list of available arguments).')

    return argparser, Args(args.maps, args.classname, args.key, args.value, flags, args.flags_or)


def check_map(filepath: Path, args: Args) -> list[tuple[int, dict[str, str]]]:
    reader = BSPEntReader(filepath)
    entities: list[tuple[int, dict[str, str]]] = []

    for index, entity in enumerate(reader.entities, start=-1):
        if args.classnames:
            if entity['classname'] not in args.classnames:
                continue
        if args.keys:
            skip = True
            for key in entity.keys():
                if key in args.keys:
                    skip = False
            if skip:
                continue
        if args.values:
            skip = True
            for value in entity.values():
                if value in args.values:
                    skip = False
            if skip:
                continue
        if args.flags:
            spawnflags = 0
            if 'spawnflags' in entity:
                spawnflags = int(entity['spawnflags'])
            matches = spawnflags & args.flags
            if matches == 0:
                continue
            if not args.flags_or and matches != args.flags:
                continue

        entities.append((index, entity))

    return entities


if __name__ == '__main__':
    argparser, args = parse_args()

    maps_dir = Path(args.maps)

    if not maps_dir.is_dir():
        argparser.exit(1, f"'{maps_dir.absolute()}' is not a directory")
    
    maps: dict[str, list[tuple[int, dict[str, str]]]] = {}
    for glob in maps_dir.glob('*.bsp'):
        entities = check_map(glob, args)
        if entities:
            maps[glob.name] = entities
    
    if not maps:
        argparser.exit(2, "No maps with entities matching the query found")
    
    mapstrings: list[str] = []

    for map, entities in maps.items():
        mapstr = f"{map}: [\n"
        entstrings: list[str] = []

        for index, entity in entities:
            entstr = f"  {entity['classname']} (index {index}"
            if 'targetname' in entity:
                entstr += f", targetname '{entity['targetname']}'"
            entstr += ')'
            entstrings.append(entstr)
        
        mapstr += ",\n".join(entstrings)
        mapstr += "  \n]"

        mapstrings.append(mapstr)

    print(",\n".join(mapstrings), end='')

    argparser.exit(0)
