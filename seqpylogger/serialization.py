import json
from datetime import datetime, date, time
from decimal import Decimal


def serialize(obj):
    """JSON serializer for objects not serializable by default JSON encoder."""

    # Handle datetime, date, and time types
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()

    # Handle Decimal type
    if isinstance(obj, Decimal):
        return float(obj)

    # Handle custom objects (with __dict__)
    if hasattr(obj, "__dict__"):
        return {key: serialize(value) for key, value in vars(obj).items()}

    # Handle lists and tuples recursively
    if isinstance(obj, (list, tuple)):
        return [serialize(item) for item in obj]

    # Handle dictionaries recursively
    if isinstance(obj, dict):
        return {serialize(key): serialize(value) for key, value in obj.items()}

    # Fallback for default serialization
    return str(obj)


def json_serialize(obj):
    try:
        return json.dumps(
            obj,
            separators=(",", ":"),
            indent=None,
            default=serialize,
        )
    except Exception:
        return str(obj)
