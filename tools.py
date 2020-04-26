import re
from pathlib import Path

_unauthorized_char = "!\"#$%&()*,./:;<=>?@[]\\^_`|"


def break_path(path):
    """
    Take a path as a string and return the filename
    and the type in a tuple : (filename,type)
    """
    tmpPath = Path(path)
    return (tmpPath.stem,tmpPath.suffix[1:])

def construct_filename(name,typename):
    """
    Construct filename using name and typename.
    Use normalize_field()
    """
    name = normalize_field(name).lower().replace(" ","_")
    return name+"."+typename.lower()

def normalize_field(name):
    """
    Delete the unauthorized characters
    of the entry.
    """
    name = "".join(filter(
        lambda char:char not in _unauthorized_char,name))
    name = re.sub(r" +",' ',name)
    return name.strip().title()
