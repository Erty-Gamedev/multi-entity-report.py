from pathlib import Path
from io import BufferedReader, StringIO
from itertools import batched
from struct import unpack


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

def read_token(content: StringIO) -> str:
    token = ''
    while c := content.read(1):
        if c == '"':
            break
        token += c
    return token

def read_entity(content: StringIO) -> dict[str, str]:
    entity: dict[str, str] = {}
    tokens: list[str] = []

    while c := content.read(1):
        if c.isspace(): continue

        if c == '"':
            tokens.append(read_token(content))
            continue

        if c == '}': break

        raise Exception(f"Unexpected character: '{c}' (at {content.tell()})")

    for key, value in batched(tokens, 2):
        entity[key] = value

    return entity

def read_entities(content: StringIO) -> list[dict[str, str]]:
    entities: list[dict[str, str]] = []

    while c := content.read(1):
        if c.isspace(): continue
        if c == '{':
            entity = read_entity(content)
            entities.append(entity)
    
    return entities

class BSPEntReader:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.entities: list[dict[str, str]] = []

        with filepath.open('rb') as file:
            version = read_int(file)
            if version != 30:
                raise InvalidFormatException(
                    f"Invalid BSP version: {version}")
            
            nOffset = read_int(file)
            nLength = read_int(file)
            
            file.seek(nOffset)
            entity_content = read_ntstring(file, nLength)
            self.entities = read_entities(StringIO(entity_content))
