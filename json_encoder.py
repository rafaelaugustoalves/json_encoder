from typing import Any

import numpy

from json_encoder.memento_utils import create_basic_memento
from json_encoder.public_enums import (
    is_public_enum, encode_enum, decode_enum)
from json_encoder.public_objects import (
    is_public_object, is_encoded_public_object, load_public_object)


def to_json_encodable(obj: Any) -> Any:
    """
    Transform an object to an equivalent object which can be serialized/encoded
    by Json default encoder (e.g. and encodable object)

    Note: this function is used recursively and is prone to wrongly catching
    unexpected exceptions. To reduce this risk, exceptions messages are used to
    distinguish between expected and not expected errors.
    """
    # Case when the object is a known Enum
    if is_public_enum(obj):
        return encode_enum(obj)

    if is_public_object(obj):
        try:
            memento = obj.create_memento()
        except AttributeError:
            memento = create_basic_memento(obj)
        return to_json_encodable(memento)

    if isinstance(obj, numpy.ndarray):
        encodable_obj = obj.tolist()
        return to_json_encodable(encodable_obj)

    # Case where object is dict like
    try:
        encodable_obj = {}
        for key, value in obj.items():
            encodable_key = to_json_encodable(key)
            encodable_value = to_json_encodable(value)
            encodable_obj[encodable_key] = encodable_value
        return encodable_obj
    except AttributeError as error:
        if "object has no attribute 'items'" not in repr(error):
            raise error from None

    # Case when object is a string
    # This must be checked before checking for sequence-like because string is
    # considered a sequence
    if isinstance(obj, str):
        return obj

    # Case when obj is sequence like
    try:
        encodable_obj = []
        for value in obj:
            encodable_value = to_json_encodable(value)
            encodable_obj.append(encodable_value)
        return encodable_obj
    except TypeError as error:
        if 'object is not iterable' not in repr(error):
            raise error from None

    # When there are no other known processing to make the object json
    # encodable, it is assumed that it's already encodable
    return obj


def from_json_encodable(encodable_obj: Any) -> Any:
    """
    Decode a json serialized object
    """
    # Case when object is a known Public Object
    if is_encoded_public_object(encodable_obj):
        return load_public_object(encodable_obj)

    if is_public_enum(encodable_obj):
        return decode_enum(encodable_obj)

    # Case where object is dict like
    try:
        decoded_obj = {}
        for key, value in encodable_obj.items():
            decoded_key = from_json_encodable(key)
            decoded_value = from_json_encodable(value)
            decoded_obj[decoded_key] = decoded_value
        return decoded_obj
    except AttributeError as error:
        if "object has no attribute 'items'" not in repr(error):
            raise error from None

    # Case when object is a string
    # This must be checked before checking for sequence-like because string is
    # considered a sequence
    if isinstance(encodable_obj, str):
        return encodable_obj

    # Case when obj is sequence like
    try:
        decoded_obj = []
        for value in encodable_obj:
            decoded_value = from_json_encodable(value)
            decoded_obj.append(decoded_value)
        return decoded_obj
    except TypeError as error:
        if 'object is not iterable' not in repr(error):
            raise error from None

    # When there are no other known processing to further deserialize, the object
    # is assumed already deserialized
    return encodable_obj
