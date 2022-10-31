import json
import os.path


class JsonHelper:
    def __init__(self, path: str):
        self.path = path
        self.local_dict: dict = self.load_json()

    def save_dict(self):
        """
        Save the dictionary to disk.
        Meant to be run when no more changes are expected to be made.

        Returns: None
        """
        # 'w+' mode creates or overwrites a file with the name
        with open(self.path, 'w+') as file:
            json.dump(self.local_dict, file)

    def load_json(self) -> dict[str, [dict]]:
        """
        Loads the json from disk with the path given on class initialization
        If no json file exists at the path, return an empty dictionary.

        Returns: Dictionary representing the json at the path
        """
        if not os.path.isfile(self.path):
            return {}

        with open(self.path, 'r') as file:
            return json.load(file)

    def add_to_dict(self, new_dict: dict):
        """
        Wrapper for merge_nested_dict. Used the self.local_dict as old_dict

        Args:
            new_dict: Dictionary used as second dictionary in merge_nested_dict

        Returns: None
        """
        self.merge_nested_dict(self.local_dict, new_dict)

    def overwrite_dict(self, new_dict: dict):
        """
        Overwrites the dictionary stored in the class with the input

        Args:
            new_dict: Dictionary to replace the existing dictionary

        Returns: None
        """
        self.local_dict = new_dict

    def merge_nested_dict(self, old_dict: dict, new_dict: dict):
        """
        Recursive function for merging two dictionaries. Merges the attributes of all nested dictionaries. Also merges
        lists in the dictionaries.

        Args:
            old_dict: First dictionary. Non-list and -dictionary elements get overwritten by elements from new_dict.
            new_dict: Second dictionary. Non-list and -dictionary elements from this dictionary will overwrite items
                         from the old_dict

        Returns: Merged dictionary from the two inputs
        """
        for key in new_dict.keys():
            if key in old_dict and isinstance(old_dict[key], dict) and isinstance(new_dict[key], dict):
                # Recursive call if both items are dictionaries
                old_dict = self.merge_nested_dict(old_dict[key], new_dict[key])

            elif key in old_dict and isinstance(old_dict[key], list) and isinstance(new_dict[key], list):
                # Edge case call if both items are lists
                old_dict[key] += new_dict[key]

            else:
                # Normal data replacement call
                old_dict[key] = new_dict[key]

        return old_dict
