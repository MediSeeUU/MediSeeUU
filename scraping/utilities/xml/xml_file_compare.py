import xml.etree.ElementTree as ET
import scraping.utilities.definitions.xml_tags as xml_tags
import xml_parsing_utils as xml_utils
import scraping.utilities.log as log
import os.path as path
import json

def compare_xml_files_dict(new_xml_path: str, old_xml_path: str) -> dict[str, any]:
    try:
        body_old_file = ET.parse(old_xml_path).getroot()[1]
    except ET.ParseError:
        # log.warning("ANNEX COMPARER: failed to open xml file", old_xml_path)
        return {}

    try:
        body_new_file = ET.parse(new_xml_path).getroot()[1]
    except ET.ParseError:
        # log.warning("ANNEX COMPARER: failed to open xml file", new_xml_path)
        return {}
    
    comparison_dict = {"old_file": path.basename(old_xml_path), 
                       "new_file": path.basename(new_xml_path), 
                       "changes": []}

    for new_section in body_new_file:
        in_old_file = False
        new_header_text = xml_utils.section_get_header_text_numberless(new_section).replace("\n","").replace("  ","").strip()   
        new_section_text = xml_utils.section_append_paragraphs(new_section).replace("\n","").replace("  ","").strip() #TODO: fix changes due to page numbers
            
        for old_section in body_old_file:
            old_header_text = xml_utils.section_get_header_text_numberless(old_section).replace("\n","").replace("  ","").strip()
            old_section_text = xml_utils.section_append_paragraphs(old_section).replace("\n","").replace("  ","").strip()

            if new_header_text == old_header_text:
                in_old_file = True

                if new_section_text != old_section_text:
                    change_dict = {}
                    change_dict["change"] = "section text"
                    change_dict["header"] = new_header_text
                    change_dict["old text"] = old_section_text
                    change_dict["new text"] = new_section_text
                    comparison_dict["changes"].append(change_dict)
                    break
        
        if not in_old_file:
            change_dict = {}
            change_dict["change"] = "added section"
            change_dict["header"] = new_header_text
            change_dict["old text"] = ""
            change_dict["new text"] = new_section_text
            comparison_dict["changes"].append(change_dict)

    for old_section in body_old_file:
        in_new_file = False
        old_header_text = xml_utils.section_get_header_text_numberless(old_section).replace("\n","").replace("  ","").strip()
        old_section_text = xml_utils.section_append_paragraphs(old_section).replace("\n","").replace("  ","").strip()

        for new_section in body_new_file:
            new_header_text = xml_utils.section_get_header_text_numberless(new_section).strip()
            in_new_file = old_header_text == new_header_text
        
        if not in_new_file:
            change_dict = {}
            change_dict["change"] = "removed section"
            change_dict["header"] = old_header_text
            change_dict["old text"] = old_section_text
            change_dict["new text"] = ""
            comparison_dict["changes"].append(change_dict)

    return comparison_dict

def compare_xml_files_file(new_xml_path: str, old_xml_path: str, save_dir: str, filename = "comparison.json"):
    comparison_dict = compare_xml_files_dict(new_xml_path, old_xml_path)

    try:
        with open(path.join(save_dir, filename), "w") as comparison_json:
            json.dump(comparison_dict, comparison_json)
    except Exception:
        print("ANNEX COMPARER: write", path.join(save_dir, filename))

new_xml = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_h_a_anx_1.xml"
old_xml = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130\\EU-1-00-130_h_a_anx_0.xml"
save_dir = "D:\\Git_repos\\MediSeeUU\\data\\active_withdrawn\\EU-1-00-130"
compare_xml_files_file(new_xml, old_xml, save_dir)





        
