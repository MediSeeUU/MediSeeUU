import xml_parsing_utils as Utils
import parsedinfostruct as PIS
import re

def scrape_medicine_name(section: Utils.ET.Element, parsed_info: PIS.ParsedInfoStruct):
    name_containing_text = Utils.section_get_paragraph_index(0, section)
    parsed_info.name = re.search("an application for Marketing Authorisation to the European Medicines Agency (EMEA) for (.*),")


def scrape_shelf_life(parsed_info: PIS.ParsedInfoStruct, section: Utils.ET.Element):
    if not Utils.section_contains_head_substring_set(["shelflife", "shelf", "life", "shelf life"], section):
        return
    
    parsed_info.shelfLife = Utils.combine_paragraph_texts(section)