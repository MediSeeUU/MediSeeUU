import attributes.id as attr_id
import attributes.sources as attr_src
import attributes.combine as attr_combine

import json
import os.path as path

def combine_folder(filepath: str, folder_name: str):
    # with open(path.join(filepath, folder_name + "_filedates.json"), "r") as filedates_json:
    #     filedates: dict[any, any] = json.load(filedates_json)

    with open(path.join(filepath, folder_name + "_pdf_parser.json"), "r") as pdf_data_json:
        pdf_data: dict[any, any] = json.load(pdf_data_json)

    with open(path.join(filepath, folder_name + "_webdata.json"), "r") as web_data_json:
        web_data: dict[any, any] = json.load(web_data_json)

    decision_files = sorted([(int(dictionary["filename"][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["decisions"]], key=lambda x : x[0])
    annex_files = sorted([(int(dictionary["pdf_file"][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["annexes"]], key=lambda x : x[0])

    #TODO: try catch deez nutz
    file_dicts = {
        "dec": decision_files[-1][1],
        "dec_initial": decision_files[0][1],
        "anx": annex_files[-1][1],
        "anx_initial": annex_files[0][1],
        # "epar": pdf_data["epars"][0]["filename"],
        # "omar": pdf_data["omars"][0]["filename"],
        "web": web_data
    }

    combined_dict: dict[str, any] = {}
    value, all_equal = get_attribute(attr.id.eu_aut_date.value["name"], sources_to_dicts(attr_src., file_dicts), attr.id.eu_aut_date.value["combine"])
    combined_dict[attr.id.eu_aut_date.value["name"]] = value

    # for attribute in [attribute["name"] for attribute in dir(attr) where "__"]:
    #     value, all_equal = get_attribute(attribute["name"], sources_to_dicts(attribute["sources"], file_dicts))
    #     combined_dict[attribute["name"]] = value

        # if not all_equal:
        #     print("shiiit boi, log dis")
    
    combined_json = open(path.join(filepath, folder_name + "_combined.json"), "w")
    json.dump(combined_dict, combined_json)
    combined_json.close()


def sources_to_dicts(sources: list[str], file_dicts: dict[str, dict]) -> list[dict]:
    source_dicts: list[str] = []

    for source in sources:
        source_dicts.append(file_dicts[source])
    
    return source_dicts

def get_attribute(attribute_name: str, dicts: list[dict], combine_attributes = False) -> tuple[str, bool]:
    attributes: set[str] = []    
    for dict in dicts:
        attributes.append(dict[attribute_name])
    all_equal = len(set(attributes)) == 1

    if combine_attributes:
        return (" / ".join(attributes), all_equal)

    return (attributes[0], all_equal)

# combine_folder("D:\Git_repos\MediSeeUU\data\EU-1-99-126", "EU-1-99-126")
# print(attr.id.atc_code.value["name"])
print(attr.atc_code_name)
print(attr.atc_code_sources)
all_names = [attribute for attribute in dir(attr) if "_alias" in attribute]
print(all_names)
