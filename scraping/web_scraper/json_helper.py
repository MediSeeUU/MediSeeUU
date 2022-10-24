import json

# TODO: Rewrite documentation when QA comes up with a standard


class JsonHelper:
    def __init__(self, path: str):
        self.path = path

    def save_urls(self, url_dict_list: dict[str, [dict]]):
        with open(self.path, 'w+') as file:
            json.dump(url_dict_list, file)

    def save_single_url(self, eu_num: str, url_dict: dict, overwrite_existing: bool = False):
        existing_json = self.load_urls()

        if not overwrite_existing:
            # |= operator appends dict to another dict
            existing_json[eu_num] |= url_dict
        else:
            existing_json[eu_num] = url_dict

        self.save_urls(existing_json)

    def load_urls(self) -> dict[str, [dict]]:
        with open(self.path, 'r') as file:
            return json.load(file)

    def load_single_url(self, eu_num: str) -> dict:
        full_dict = self.load_urls()
        return full_dict[eu_num]
