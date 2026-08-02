from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    res: list[str] = []
    split = markdown.split("\n\n")
    for string in split:
        if string == "":
            continue
        res.append(string.strip())
    return res

def block_to_block_type(block:str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^```[\s\S]*```$", block):
        return BlockType.CODE
    elif greater_than_on_every_line(block):
        return BlockType.QUOTE
    elif dash_on_every_line(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def greater_than_on_every_line(text:str) -> bool:
    lines = text.split("\n")
    for line in lines:
        if not line.startswith(">"):
            return False
    return True

def dash_on_every_line(text:str) -> bool:
    lines = text.split("\n")
    for line in lines:
        if not line.startswith("- "):
            return False
    return True

def is_ordered_list(text:str) -> bool:
    lines = text.split("\n")
    counter: int = 1
    for line in lines:
        if not line.startswith(f"{counter}. "):
            return False
        counter += 1
    return True

