import re

_unauthorized_char = "!\"#$%&()*,./:;<=>?@[]\\^_`|"

def normalize_field(name):
    name = "".join(filter(
        lambda char:char not in _unauthorized_char,name))
    name = re.sub(r" +",' ',name)
    return name.strip().title()

def construct_filename(name,typename):
    name = normalize_field(name).lower().replace(" ","_")
    return name+"."+typename.lower()

