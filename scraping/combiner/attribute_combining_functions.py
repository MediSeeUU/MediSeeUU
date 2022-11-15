import definitions.value as value
import definitions.attributes as attr
import json
import os.path as path

def combine_folder(filepath: str, folder_name: str):
    # with open(path.join(filepath, folder_name + "_filedates.json"), "r") as filedates_json:
    #     file_dates: dict[any, any] = json.load(filedates_json)

    with open(path.join(filepath, folder_name + "_pdf_parser.json"), "r") as pdf_data_json:
        pdf_data: dict[any, any] = json.load(pdf_data_json)

    with open(path.join(filepath, folder_name + "_webdata.json"), "r") as web_data_json:
        web_data: dict[any, any] = json.load(web_data_json)

    decision_files = sorted([(int(dictionary["filename"][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["decisions"]], key=lambda x : x[0])
    annex_files = sorted([(int(dictionary["pdf_file"][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["annexes"]], key=lambda x : x[0])

    #TODO: try catch deez nutz
    file_dicts = {
        attr.decision: decision_files[-1][1],
        attr.decision_initial: decision_files[0][1],
        attr.annex: annex_files[-1][1],
        attr.annex_initial: annex_files[0][1],
        # attr.epar: pdf_data["epars"][0]["filename"],
        # attr.omar: pdf_data["omars"][0]["filename"],
        attr.web: web_data
        # attr.file_dates: file_dates
    }
    
    combined_dict: dict[str, any] = {}
    #__TEST__
    # value, all_equal = get_attribute(attr.id.eu_aut_date.value["name"], sources_to_dicts(attr_src., file_dicts), attr.id.eu_aut_date.value["combine"])
    # combined_dict[attr.id.eu_aut_date.value["name"]] = value

    for key in attr.all_attributes.keys():
        attribute = attr.all_attributes[key]
        value, all_equal = get_attribute(attribute.name, sources_to_dicts(attribute.sources, file_dicts), attribute.combine)
        combined_dict[attribute.name] = value

        if not all_equal:
            print("found multiple values for " + attribute.name + ": " + value + "in " + str(sources_to_dicts(attribute.sources, file_dicts)))
    
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
    print(attribute_name + ": " + str(dicts))
    for dict in dicts:
        try:
            attributes.append(dict[attribute_name])
        except Exception:
            print(attribute_name + " attribute id is not'st'n't contained in " + str(dict))

    all_equal = len(set(attributes)) == 1

    if combine_attributes:
        return (" / ".join(attributes), all_equal)

    attributes.append(value.not_found)
    return (attributes[0], all_equal)

combine_folder("D:\Git_repos\MediSeeUU\data\EU-1-99-126", "EU-1-99-126")