"""Utility module for JSON file persistence operations."""
import json
import os


def load_json_list(file_path, entity_name="data"):
    """Load a list of records from a JSON file.

    Args:
        file_path: Path to the JSON file.
        entity_name: Name of the entity for error messages.

    Returns:
        List of dictionaries loaded from the file.
    """
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                print(
                    f"Error: {entity_name} data file has invalid format."
                )
                return []
            return data
    except json.JSONDecodeError as exc:
        print(f"Error reading {entity_name} data file: {exc}")
        return []
    except OSError as exc:
        print(f"Error accessing {entity_name} data file: {exc}")
        return []


def save_json_list(data, file_path):
    """Save a list of records to a JSON file.

    Args:
        data: List of dictionaries to save.
        file_path: Path to the JSON file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
