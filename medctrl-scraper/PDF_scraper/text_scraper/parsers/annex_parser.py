import pdf_xml_converter as xmlc
import xml.etree.ElementTree as ET
import xml_parsing_utils as Utils
import parsed_info_struct as PIS
import parsers.annex_parsing_functions as APF
import os


def parse_file(filepath: str, medicine_struct: PIS.parsed_info_struct):
    xml_tree = ET.parse(filepath)
    xml_root = xml_tree.getroot()
    xml_header = xml_root[0]
    xml_body = xml_root[1]

    is_initial_file = Utils.file_is_initial(xml_header)

    #create annex attribute dictionary with default values
    annex_attributes: dict[str,str] = {}
    annex_attributes["pdf_file"] = Utils.file_pdf_name(xml_header)
    annex_attributes["is_initial"] = is_initial_file
    
    # add default attribute values for initial authorization annexes
    if is_initial_file:
        annex_attributes["initial_type_of_eu_authorization"] = "standard"
        annex_attributes["eu_type_of_medicine"] = "small molecule"

    for section in xml_body:
        section_header = section[0]
        # print(section_header.text)

        # scrape attributes specific to authorization annexes
        if is_initial_file:
            # initial type of eu authorization
            # override default value of "standard" if "specific obligation" is present in text
            if Utils.section_contains_head_substring("specific obligation", section):
                annex_attributes["initial_type_of_eu_authorization"] = "exceptional or conditional"
            
            # definately conditional if "conditional approval" in text
            if Utils.section_contains_head_substring("conditional approval", section):
                annex_attributes["initial_type_of_eu_authorization"] = "conditional"

            # eu type of medicine
            # override default value of "small molecule" if traceability header is present
            if Utils.section_contains_head_substring("traceability", section):
                annex_attributes["eu_type_of_medicine"] = "biologicals"

        #TODO: to add attributes, initial EU conditions and current EU conditions, 50 and 51 in bible

    medicine_struct.annexes.append(annex_attributes)
    return medicine_struct
