from typing import Final
from pathlib import Path
from io import BufferedReader
from struct import unpack

LUMP_ENTITIES: Final[int] = 0
HEADER_LUMPS:  Final[int] = 15


class InvalidFormatException(Exception):
    pass
class EndOfFileException(Exception):
    pass


def read_int(file: BufferedReader) -> int:
    """Reads 4 bytes (int32) from the buffer"""
    return unpack('<i', file.read(4))[0]

def read_ntstring(file: BufferedReader, length: int) -> str:
    """Reads a null-terminated string of a set length from the buffer"""
    strbytes = unpack(f"<{length}s", file.read(length))[0]
    string = ''
    for b in strbytes:
        if b == 0:
            break
        string += chr(b)
    return string


class BSPEntReader:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.entities: list[dict[str, str]] = []
        bsplumps: list[tuple[int, int]] = []

        with filepath.open('rb') as file:
            version = read_int(file)
            if version != 30:
                raise InvalidFormatException(
                    f"Invalid BSP version: {version}")
            
            nOffset = read_int(file)
            nLength = read_int(file)
            
            file.seek(nOffset)
            entity_content = read_ntstring(file, nLength)
            self.read_entities(entity_content)
    
    def read_entities(self, content: str):
        entity: dict[str, str] = {}
        for line in content.splitlines():
            line = line.strip()

            if line.startswith('{'):
                entity = {}
                continue

            if line.startswith('//'):
                continue
            
            if line.startswith('"'):
                keyvalue = line.split('"')
                if len(keyvalue) > 5:
                    raise Exception(f"Invalid keyvalue: {keyvalue}.")
                key, value = keyvalue[1].strip(), keyvalue[3].strip()

                entity[key] = value
            
            elif line.startswith('}'):
                self.entities.append(entity)
            
            else:
                raise Exception(f"Unexpected entity data: {line}")
