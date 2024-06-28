from typing import Any


PUBLIC_ENUMS = {
}


def is_public_enum(obj: Any) -> bool:
    # Check if object is an encoded enum
    try:
        if '__enum__' in obj:
            _, name, member = obj.split('.')
            if name in PUBLIC_ENUMS:
                return True
    except TypeError:
        pass

    # Check if object is a python enum
    if type(obj) in PUBLIC_ENUMS.values():
        return True

    return False


def encode_enum(obj: PUBLIC_ENUMS):
    if not is_public_enum(obj):
        raise ValueError(f'Object {obj} is not known public enum')
    return f'__enum__.{obj}'


def decode_enum(d: Any):
    if '__enum__' in d:
        _, name, member = d.split('.')
        return getattr(PUBLIC_ENUMS[name], member)
    else:
        return d
