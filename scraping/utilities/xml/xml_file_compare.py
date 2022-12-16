import xml.etree.ElementTree as ET
import scraping.utilities.definitions.xml_tags as xml_tags
import xml_parsing_utils as xml_utils
import scraping.utilities.log as log
import os.path as path
import json

def clean_string(string: str):
    return string.replace("\n","").replace("\t","").replace(" ","")


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

new_xml = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_h_anx_1.xml"
old_xml = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_h_anx_0.xml"
save_dir = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130"
compare_xml_files_file(new_xml, old_xml, save_dir)





        
