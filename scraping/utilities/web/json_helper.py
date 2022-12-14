import json
import os.path


class JsonHelper:
    """
    Helper class for creating, editing, merging and saving JSON files.
    Contains a path for the JSON file and a local dictionary for that JSON.
    """
    def __init__(self, path: str, init_dict: dict = None):
        self.path = path
        if init_dict or init_dict == {}:
            self.local_dict: dict = init_dict
            self.save_dict()
        else:
            self.local_dict: dict = self.load_json()

    def save_dict(self):
        """
        Save the dictionary to disk.
        Meant to be run when no more changes are expected to be made.
        """
        # 'w+' mode creates or overwrites a file with the name
        with open(self.path, 'w+') as file:
            json.dump(self.local_dict, file, indent=4)

    def load_json(self) -> dict[str, [dict]]:
        """
        Loads the json from disk with the path given on class initialization
        If no json file exists at the path, return an empty dictionary.

        Returns:
            (dict[str, [dict]]): Dictionary representing the json at the path
        """
        if not os.path.isfile(self.path):
            return {}
        with open(self.path, 'r') as file:
            return json.load(file)

    def add_to_dict(self, new_dict: dict):
        """
        Wrapper for merge_nested_dict. Used the self.local_dict as old_dict

        Args:
            new_dict (dict): Dictionary used as second dictionary in merge_nested_dict
        """
        self.merge_nested_dict(self.local_dict, new_dict)

    def overwrite_dict(self, new_dict: dict):
        """
        Overwrites the dictionary stored in the class with the input

        Args:
            new_dict (dict): Dictionary to replace the existing dictionary
        """
        self.local_dict = new_dict

    def merge_nested_dict(self, old_dict: dict, new_dict: dict) -> dict:
        """
        Recursive function for merging two dictionaries. Merges the attributes of all nested dictionaries. Also merges
        lists in the dictionaries.

        Args:
            old_dict (dict): First dictionary. Non-list and -dictionary elements get overwritten by elements from new_dict.
            new_dict (dict): Second dictionary. Non-list and -dictionary elements from this dictionary will overwrite items
                         from the old_dict

        Returns:
            dict: Merged dictionary from the two inputs
        """
        for key in new_dict.keys():
            if key in old_dict and isinstance(old_dict[key], dict) and isinstance(new_dict[key], dict):
                # Recursive call if both items are dictionaries
                old_dict = self.merge_nested_dict(old_dict[key], new_dict[key])

            elif key in old_dict and isinstance(old_dict[key], list) and isinstance(new_dict[key], list):
                # Edge case call if both items are lists
                old_list = old_dict[key]
                old_list.extend(new_dict[key])
                merged_list = old_list
                # Keep ordering, remove duplicates
                seen = set()
                seen_add = seen.add
                no_dup_list = [x for x in merged_list if not (tuple(x) in seen or seen_add(tuple(x)))]
                old_dict[key] = no_dup_list

            else:
                # Normal data replacement call
                old_dict[key] = new_dict[key]

        return old_dict
