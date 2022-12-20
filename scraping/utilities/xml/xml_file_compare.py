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
        comparison_dict["changes"].append({
            "change": "added section",
            "header": sections_new_file[section_key][0],
            "section text": sections_new_file[section_key][1]
        })
    
    for section_key in removed_keys:
        comparison_dict["changes"].append({
            "change": "removed section",
            "header": sections_old_file[section_key][0],
            "section text": sections_old_file[section_key][1]
        })

    for section_key in shared_keys:
        if clean_string(sections_old_file[section_key][1]) != clean_string(sections_new_file[section_key][1]):
            comparison_dict["changes"].append({
                "change": "changed section content",
                "header": sections_new_file[section_key][0],
                "old content": sections_old_file[section_key][1],
                "new content": sections_new_file[section_key][1]
            })

    return comparison_dict


def compare_xml_files_file(new_xml_path: str, old_xml_path: str, save_dir: str, filename = "comparison.json"):
    comparison_dict = compare_xml_files_dict(new_xml_path, old_xml_path)

    try:
        with open(path.join(save_dir, filename), "w") as comparison_json:
            json.dump(comparison_dict, comparison_json)
    except Exception:
        print("ANNEX COMPARER: write", path.join(save_dir, filename))


def folder_changelog_up_to_date(folder: str, filepath: str, force_replace = False):
    annex_files = [path.join(folder, file) for file in os.listdir(folder) if ".xml" in file and "anx_" in file]
    compared_annex_files = []

    try:
        with open(filepath) as comparison_file:
            comparison_dict = json.load(comparison_file)
            compared_annex_files = comparison_dict["changelog"]
    except FileNotFoundError:
        return len(annex_files) == 0
    except Exception:
        print("ANNEX COMPARER: cant open", filepath)
        
    return len(annex_files) == (len(compared_annex_files) - 1)


def compare_annexes_folder(folder: str, replace_all = False, filename_suffix: str = "_annex_changelog.json"):
    annex_files = [path.join(folder, file) for file in os.listdir(folder) if ".xml" in file and "anx_" in file]
    annex_files.sort(key= lambda annex_name: int(annex_name.split(".")[0].split("_")[-1]))
    subfolders = [path.join(folder, subfolder) for subfolder in os.listdir(folder) if path.isdir(path.join(folder, subfolder))]
    comparisons = {"eu_number": path.basename(folder),
                   "update date": datetime.datetime.now(),
                   "changelogs": []}
    filename = path.basename(folder) + filename_suffix

    if folder_changelog_up_to_date(folder, filename):
        annex_files = []

    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(compare_annexes_folder)(subfolder) for subfolder in
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
        print("writing to file", str(path.join(folder, path.basename(folder), filename)))
        try:
            with open(path.join(folder, filename), "w") as comparison_json:
                json.dump(comparisons, comparison_json)
        except Exception:
            print("ANNEX COMPARER: cannot write", path.join(folder, filename))


def clean_section_text(change_key: str, change: dict[str, str]) -> str:
    enter_seperator = "\n\t\t\t"
    return enter_seperator.join(list(map(str.strip, change[change_key].split("\n"))))

def changelog_to_text(changelog: dict[str,str]) -> str:
    text = ""
    text += changelog["new_file"] + ":\n\n"

    for change in changelog["changes"]:
        text += "\t" + change["change"].strip() + ": " + change["header"].replace("\n", "").strip() + "\n\n"
        keys = change.keys()

        if "section text" in keys:
            text += "\t\t" + "section text:\n"
            section_text = clean_section_text("section text", change)
            text += "\t\t\t" + section_text + "\n"
        if "new content" in keys:
            text += "\t\t" + "new content:\n"
            section_text = clean_section_text("new content", change)
            text += "\t\t\t" + section_text + "\n"
        if "old content" in keys:
            text += "\t\t" + "old content:\n"
            section_text = clean_section_text("old content", change)
            text += "\t\t\t" + section_text + "\n"
            
        text += "\n"

    return text


def changelog_json_to_text(changelog_filepath: str) -> str:
    changelog_dict = {}
    try:
        with open(changelog_filepath, "r") as changelog_json:
            changelog_dict = json.load(changelog_json)
    except Exception:
        print("ANNEX COMPARER:", changelog_filepath, "does not exist")
        return ""
    
    text = ""
    for changelog in changelog_dict["changelogs"]:
        text += changelog_to_text(changelog)

    return text


def changelog_json_to_text_file(changelog_filepath: str, save_filepath: str):
    file_content = changelog_json_to_text(changelog_filepath)
    file_lines = file_content.split("\n")
    print(file_lines)
    try:
        changelog_text_file = open(save_filepath, "w")
    except Exception:
        print("ANNEX COMPARER: cannot create", save_filepath)
        return

    for line in file_lines:
        try:
            changelog_text_file.write(line + "\n")
        except Exception:
            print("ANNEX COMPARER: cannot write line: ", line)

    try:
        changelog_text_file.write(file_content)
    except Exception:
        print("ANNEX COMPARER: cannot write file_content: ", file_content)

    changelog_text_file.close()
    print("closed file")



# data_folder = "D:\\Git_repos\\MediSeeUU\\data"
# new_xml         = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_h_anx_2.xml"
# old_xml         = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_h_anx_1.xml"
# changelog_json  = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_annex_changelog.json"
# changelog_txt   = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_annex_changelog.txt"
# save_dir = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130"
# compare_xml_files_file(new_xml, old_xml, save_dir)
# changelog_json_to_text_file(changelog_json, changelog_txt)
# compare_annexes_folder(data_folder)



        
