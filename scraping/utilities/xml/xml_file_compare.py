import xml.etree.ElementTree as ET
import scraping.utilities.definitions.xml_tags as xml_tags
import xml_parsing_utils as xml_utils
import scraping.utilities.log as log
import joblib
import multiprocessing
from tqdm import tqdm
import os.path as path
import os
import datetime
import json

def clean_string(string: str):
    return string.replace("\n","").replace("\t","").replace("\r","").replace(" ","")


def remove_header_number(header_text) -> str:
    text_start_index = 0
    for i in range(0, len(header_text)):
        if all(map(lambda c: c.isnumeric() or c == '.', header_text[0:i])):
            text_start_index = i
        else:
            break
    return header_text[text_start_index:].strip()


def clean_renamed_header_text(header_text: str):
    occurence_number = header_text.split("|")[0].strip()
    header_text = header_text.split("|")[-1].strip()
    header_text = remove_header_number(header_text)

    return occurence_number + " | " + header_text


def rename_duplicate_headers(xml_body: ET.ElementTree) -> ET.ElementTree:
    occurences: dict[str, int] = {}
    new_body: ET.Element = ET.Element(xml_tags.body)

    for section in xml_body:
        header_text = xml_utils.section_get_header_text(section)
        header_text_clean = clean_string(remove_header_number(header_text))

        if header_text_clean not in occurences.keys():
            occurences[header_text_clean] = 1
        else:
            occurences[header_text_clean] += 1
        
        count = occurences[header_text_clean]
        new_body.append(xml_utils.section_set_header_text(str(count) + " | " + header_text, section))

    return new_body


def create_section_dict(xml_body: ET.Element) -> dict[str, (str, str)]:
    section_dict = {}
    for section in xml_body:
        header_text = xml_utils.section_get_header_text(section)
        section_header = clean_renamed_header_text(header_text)
        section_key = clean_string(section_header)
        section_text = xml_utils.section_append_paragraphs(section)
        section_dict[section_key] = (section_header, section_text)

    return section_dict


def open_xml_path(xml_path: str) -> ET.Element:
    try:
        xml_body = ET.parse(xml_path).getroot()[1] # get xml_body
        xml_body = rename_duplicate_headers(xml_body)
    except ET.ParseError:
        # log.warning("ANNEX COMPARER: failed to open xml file", xml_path) #TODO: enable logging
        return {}

    return xml_body


def compare_xml_files_dict(new_xml_path: str, old_xml_path: str) -> dict[str, any]:
    body_new_file = open_xml_path(new_xml_path)
    body_old_file = open_xml_path(old_xml_path)

    if body_new_file == {} or body_old_file == {}:
        return {}
    
    comparison_dict = {"old_file": path.basename(old_xml_path), 
                       "new_file": path.basename(new_xml_path), 
                       "changes": []}            

    sections_new_file = create_section_dict(body_new_file)
    sections_old_file = create_section_dict(body_old_file)

    shared_keys = sections_new_file.keys() & sections_old_file.keys()
    added_keys = [key for key in sections_new_file.keys() if key not in shared_keys]
    removed_keys = [key for key in sections_old_file.keys() if key not in shared_keys]

    for section_key in added_keys:
        change_dict = {
            "change": "added section",
            "header": sections_new_file[section_key][0],
            "section_text": sections_new_file[section_key][1]
        }
        change_dict["change_note"] = change_dict_to_string(change_dict)
        comparison_dict["changes"].append(change_dict)
    
    for section_key in removed_keys:
        change_dict = {
            "change": "removed section",
            "header": sections_old_file[section_key][0],
            "section_text": sections_old_file[section_key][1]
        }
        change_dict["change_note"] = change_dict_to_string(change_dict)
        comparison_dict["changes"].append(change_dict)

    for section_key in shared_keys:
        if clean_string(sections_old_file[section_key][1]) != clean_string(sections_new_file[section_key][1]):
            change_dict = {
                "change": "changed section content",
                "header": sections_new_file[section_key][0],
                "old_content": sections_old_file[section_key][1],
                "new_content": sections_new_file[section_key][1]
            }
            change_dict["change_note"] = change_dict_to_string(change_dict)
            comparison_dict["changes"].append(change_dict)

    return comparison_dict


def compare_xml_files_file(new_xml_path: str, old_xml_path: str, save_dir: str, filename = "comparison.json"):
    comparison_dict = compare_xml_files_dict(new_xml_path, old_xml_path)

    try:
        with open(path.join(save_dir, filename), "w") as comparison_json:
            json.dump(comparison_dict, comparison_json)
    except Exception:
        print("ANNEX COMPARER: write", path.join(save_dir, filename))


def folder_changelog_up_to_date(folder: str, filepath: str) -> bool:
    annex_files = [path.join(folder, file) for file in os.listdir(folder) if ".xml" in file and "anx_" in file]
    changelogs = []

    try:
        with open(filepath) as comparison_file:
            comparison_dict = json.load(comparison_file)
            changelogs = comparison_dict["changelogs"]
    except FileNotFoundError:
        return len(annex_files) == 0
    except json.JSONDecodeError as e:
        print("ANNEX COMPARER:", e, "| invalid json file", filepath)
        os.remove(filepath)
        return len(annex_files) == 0
    except Exception as e:
        print("ANNEX COMPARER:", e, "| cannot determine whether changelog is up to date:", filepath)
        return False
        
    if (len(annex_files) - 1) != len(changelogs):
        print("up to date")
        print("annex_files:", len(annex_files))
        print("changelogs:", len(changelogs))

    return  (len(annex_files) - 1) == len(changelogs)


def annex_changelog_json_folder(folder: str, replace_all = False, filename_suffix: str = "_annex_changelog.json"):
    annex_files = [path.join(folder, file) for file in os.listdir(folder) if ".xml" in file and "anx_" in file]
    annex_files.sort(key= lambda annex_name: int(annex_name.split(".")[0].split("_")[-1]))
    subfolders = [path.join(folder, subfolder) for subfolder in os.listdir(folder) if path.isdir(path.join(folder, subfolder))]
    comparisons = {"eu_number": path.basename(folder),
                   "last_updated": datetime.datetime.now(),
                   "changelogs": []}
    # filename = path.basename(folder) + filename_suffix
    filename = path.join(folder, path.basename(folder) + filename_suffix)

    if folder_changelog_up_to_date(folder, filename) and not replace_all:
        annex_files = []

    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(annex_changelog_json_folder)(subfolder) for subfolder in
        tqdm(subfolders))

    comparisons["changelogs"] = joblib.Parallel(
        n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(compare_xml_files_dict)(annex_files[i], annex_files[i - 1]) for i in
        range(1, len(annex_files)))


    # single threaded version for debugging
    # for subfolder in subfolders:
    #     compare_annexes_folder(subfolder)

    # for i in range(1, len(annex_files)):
    #     comparisons["changelogs"].append(compare_xml_files_dict(annex_files[i], annex_files[i - 1]))

    if len(annex_files) > 0:
        try:
            print("writing to file", str(filename))
            with open(filename, "w") as comparison_json:
                json.dump(comparisons, comparison_json, default=str)
        except Exception as e:
            print("ANNEX COMPARER: cannot write", filename)
            print(e)


def clean_section_text(change_key: str, change: dict[str, str]) -> str:
    enter_seperator = "\n\t\t"
    return enter_seperator.join(list(map(str.strip, change[change_key].split("\n"))))


def change_dict_to_string(change: dict[str,str]) -> str:
    text = "\t" + change["change"].strip() + ": " + change["header"].replace("\n", "").strip() + "\n\n"
    keys = change.keys()

    if "section_text" in keys:
        text += "\t\t" + "section_text:\n"
        section_text = clean_section_text("section_text", change)
        text += "\t\t" + section_text + "\n"
    if "new_content" in keys:
        text += "\t\t" + "new_content:\n"
        section_text = clean_section_text("new_content", change)
        text += "\t\t" + section_text + "\n"
    if "old_content" in keys:
        text += "\t\t" + "old_content:\n"
        section_text = clean_section_text("old_content", change)
        text += "\t\t" + section_text + "\n"
        
        text += "\n"

    return text


# def changelog_json_to_text(changelog_filepath: str) -> str:
#     changelog_dict = {}
#     try:
#         with open(changelog_filepath, "r") as changelog_json:
#             changelog_dict = json.load(changelog_json)
#     except Exception:
#         print("ANNEX COMPARER:", changelog_filepath, "does not exist")
#         return ""
    
#     text = ""
#     for changelog in changelog_dict["changelogs"]:
#         text += changelog["new_file"] + ":\n\n"

#         for change_dict in changelog["changes"]:
#             text += change_dict["change_note"]

#     return text


def changelog_json_to_text_file(changelog_filepath: str, save_filepath: str):
    # skip making new annex_changelog.txt the existing one is up to date
    try:
        json_modify_date = path.getmtime(changelog_filepath)
        txt_modify_date = path.getmtime(changelog_filepath.replace(".json", ".txt"))
        if json_modify_date < txt_modify_date:
            return
    except:
        pass # should try to make a new annex_changelog.txt if failed
    
    try:
        with open(changelog_filepath, "r") as changelog_json:
            changelog_dict = json.load(changelog_json)
    except Exception as e:
        print("ANNEX COMPARER:", e, "| file does not exist:", changelog_filepath)
        return
        
    try:
        changelog_text_file = open(save_filepath, "w", encoding="utf-8")
    except Exception as e:
        print("ANNEX COMPARER:", e, "| cannot create", save_filepath)
        return
        

    for changelog_dict in changelog_dict["changelogs"]:
        try:
            changelog_text_file.write(changelog_dict["new_file"] + ":\n\n")
        except Exception as e:
            print(e)
            return
        for change_dict in changelog_dict["changes"]:
            text = change_dict["change_note"]
            try:
                changelog_text_file.write(text)
            except Exception as e:
                print("ANNEX COMPARER:", e, "| cannot write line: ", text)

    changelog_text_file.close()


def annex_changelog_text_folder(folder: str):
    changelog_jsons = [path.join(folder, file) for file in os.listdir(folder) if ".json" in file and "changelog" in file]
    subfolders = [path.join(folder, subfolder) for subfolder in os.listdir(folder) if path.isdir(path.join(folder, subfolder))]

    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(annex_changelog_text_folder)(subfolder) for subfolder in
        tqdm(subfolders))

    for changelog_json in changelog_jsons:
        changelog_json_to_text_file(changelog_json, changelog_json.replace("json", "txt"))


def main(directory: str):
    annex_changelog_json_folder(directory)
    annex_changelog_text_folder(directory)

data_folder = "D:\\Git_repos\\MediSeeUU\\data"
# new_xml         = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_h_anx_2.xml"
# old_xml         = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_h_anx_1.xml"
# changelog_json  = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_annex_changelog.json"
# changelog_txt   = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_annex_changelog.txt"
# save_dir = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130"
# compare_xml_files_file(new_xml, old_xml, save_dir)
# changelog_json_to_text_file(changelog_json, changelog_txt)
# compare_annexes_folder(data_folder)
# create_changelogs_folder(data_folder)
main(data_folder)


        
