from dagfactory.common.infrastructures.utils.import_tools import import_from_string

def cast_with_type(data):
    """Recursively cast dictionaries with a __type__ key."""
    if isinstance(data, dict):
        # Handle typed list
        if data.get("__type__") == "builtins.list" and "items" in data:
            return [cast_with_type(item) for item in data["items"]]

        # Normal typed dict
        processed = {k: cast_with_type(v) for k, v in data.items() if k not in ("__type__", "__args__")}

        # Recursively handle 'args' if present
        raw_args = data.get("__args__")
        args = []
        if raw_args is not None:
            casted_args = cast_with_type(raw_args)  # Cast the whole args object
            if not isinstance(casted_args, list):
                raise ValueError(f"'args' must resolve to a list, got {type(casted_args)}")
            args = casted_args

        if "__type__" in data:
            class_type = import_from_string(data["__type__"])
            return class_type(*args, **processed)

        return processed

    elif isinstance(data, list):
        return [cast_with_type(item) for item in data]

    return data