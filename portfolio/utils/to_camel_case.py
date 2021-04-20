import re

def to_camel_case(input_str):
    parts = re.split('[_-]', input_str)
    return parts[0] + ''.join([x.title() for x in parts[1:]])