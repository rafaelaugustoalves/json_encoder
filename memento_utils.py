import copy
from typing import Dict, Any

OBJECT_CLASS_KEY = 'OBJECT_CLASS_KEY'
OBJECT_MEMENTO_KEY = 'OBJECT_MEMENTO_KEY'


def create_basic_memento(object_instance: Any) -> Dict[str, Any]:
    class_name = type(object_instance).__name__
    attributes = copy.deepcopy(vars(object_instance))
    memento = {OBJECT_CLASS_KEY: class_name, OBJECT_MEMENTO_KEY: attributes}
    return memento


def format_object_memento(
    object_instance: Any,
    memento: Dict[str, Any],
) -> Dict[str, Any]:
    class_name = type(object_instance).__name__
    return {OBJECT_CLASS_KEY: class_name, OBJECT_MEMENTO_KEY: memento}


def is_default_encoded_object(obj: Any) -> bool:
    # Check if object has the expected encoded format
    expected_keys = [OBJECT_CLASS_KEY, OBJECT_MEMENTO_KEY]
    expected_keys.sort()
    try:
        keys = list(obj.keys())
        keys = sorted(keys)
        if keys == expected_keys:
            return True
    except AttributeError:
        return False
    return False
