import json

# TODO: Rewrite documentation when QA comes up with a standard


def save_urls(url_dict_list: dict[str, [dict]]):
    with open("CSV/urls.json", 'w') as file:
        json.dump(url_dict_list, file)


def save_single_url(eu_num: str, url_dict: dict):
    existing_json = load_urls()

    existing_json[eu_num] = url_dict

    save_urls(existing_json)


def load_urls() -> dict[str, [dict]]:
    with open("CSV/urls.json", 'r') as file:
        return json.load(file)
