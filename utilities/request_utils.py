from flask import jsonify
from dataclasses import is_dataclass, fields
from typing import get_origin, get_args

def create_instance_from_request(request, dataclass_type):
    """
    Create an instance of a dataclass from the JSON data in a Flask request.

    Args:
        request: The Flask request object.
        dataclass_type: The dataclass type to instantiate.

    Returns:
        An instance of the dataclass or a Flask response in case of an error.
    """

    try:
        data = request.get_json()
        if not is_dataclass(dataclass_type):
            raise ValueError(f"{dataclass_type.__name__} is not a dataclass")

        # Verifica e converte i tipi dei campi
        for field in fields(dataclass_type):
            if field.name in data:
                field_value = data[field.name]
                expected_type = field.type
                if get_origin(expected_type):  # Per i tipi generici come List[str]
                    if not isinstance(field_value, get_origin(expected_type)):
                        raise ValueError(f"Invalid type for field {field.name}")
                    expected_arg_type = get_args(expected_type)[0]
                    if any(not isinstance(item, expected_arg_type) for item in field_value):
                        raise ValueError(f"Invalid type in list for field {field.name}")
                else:  # Per i tipi non generici
                    if not isinstance(field_value, expected_type):
                        try:
                            data[field.name] = expected_type(field_value)
                        except (ValueError, TypeError):
                            raise ValueError(f"Invalid type for field {field.name}")

        instance = dataclass_type(**data)
        return instance
    except (TypeError, ValueError) as e:
        return jsonify({"code": 400, "message": str(e)}), 400
