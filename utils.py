import json


def load_config(file_path):
    """
    Load the configuration from the given file path.
    """
    with open(file_path, 'r') as file:
        return json.load(file)
