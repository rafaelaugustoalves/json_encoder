from typing import Any, Dict

from json_encoder.memento_utils import (
    OBJECT_CLASS_KEY, OBJECT_MEMENTO_KEY, is_default_encoded_object)


# Key should be the name of the class
PUBLIC_OBJECTS = {
}


def is_encoded_public_object(obj: Any) -> bool:
    # Check if object has the expected encoded format
    if not is_default_encoded_object(obj):
        return False  # raise TypeError('Object is not default encoded')

    object_class = obj[OBJECT_CLASS_KEY]
    if object_class in PUBLIC_OBJECTS:
        return True
    else:
        return False


def is_public_object(obj: Any) -> bool:
    # We need to check only for instances, so it does not matter that this will
    # return 'type' for classes
    object_class = type(obj).__name__
    if object_class in PUBLIC_OBJECTS:
        return True
    return False


def load_public_object(encoded_public_object: Dict[str, Any]) -> Any:
    object_class = encoded_public_object[OBJECT_CLASS_KEY]
    object_memento = encoded_public_object[OBJECT_MEMENTO_KEY]
    obj_class = PUBLIC_OBJECTS[object_class]
    object_instance = obj_class.load_memento(object_memento)
    return object_instance
