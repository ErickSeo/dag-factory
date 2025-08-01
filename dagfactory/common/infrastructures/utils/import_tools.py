import importlib

def import_from_string(class_path: str):
    """Dynamically import a class from a string."""
    try:
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Could not import '{class_path}': {e}")