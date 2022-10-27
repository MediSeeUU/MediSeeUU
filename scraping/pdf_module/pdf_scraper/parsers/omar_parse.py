# EPAR parser
import re
import xml.etree.ElementTree as ET
import scraping.pdf_module.pdf_scraper.parsed_info_struct as PIS
import scraping.pdf_module.pdf_scraper.xml_parsing_utils as Utils
import os.path as path


def parse_file(filepath: str, medicine_struct: PIS.parsed_info_struct):
    try:
        xml_tree = ET.parse(filepath)
    except ET.ParseError:
        print("OMAR PARSER: failed to open xml file " + filepath)
        return medicine_struct

    if medicine_struct is None:
        print("OMAR PARSER: medicine_struct is none at " + filepath)
        return

    xml_root = xml_tree.getroot()
    xml_header = xml_root[0]
    xml_body = xml_root[1]

    is_initial_file = Utils.file_is_initial(xml_header)
    creation_date = Utils.file_get_creation_date(xml_header)
    modification_date = Utils.file_get_modification_date(xml_header)

    # # create omar attribute dictionary with default values
    omar_attributes: dict[str, str] = {
            "pdf_file": Utils.file_get_name_pdf(xml_header),
            "is_initial": is_initial_file,
            "creation_date": creation_date,
            "modification_date": modification_date
        }

    # # add default attribute values for initial authorization annexes
    # if is_initial_file:
    #     omar_attributes["initial_type_of_eu_authorization"] = "standard"
    #     omar_attributes["eu_type_of_medicine"] = "small molecule"

    # # loop through sections and parse section if conditions met
    # for section in xml_body:
    #     # section_header = section[0]
    #     # print(section_header.text)

    #     # scrape attributes specific to authorization annexes
    #     if is_initial_file:
    #         # initial type of eu authorization
    #         # override default value of "standard" if "specific obligation" is present anywhere in text
    #         if Utils.section_contains_substring("specific obligation", section) and \
    #                 annex_attributes["initial_type_of_eu_authorization"] != "conditional":
    #             annex_attributes["initial_type_of_eu_authorization"] = "exceptional or conditional"

    #         # definitely conditional if "conditional approval" anywhere in text
    #         if Utils.section_contains_substring("conditional approval", section):
    #             annex_attributes["initial_type_of_eu_authorization"] = "conditional"

    #         # EU type of medicine
    #         # override default value of "small molecule" if traceability header is present
    #         if Utils.section_contains_header_substring("traceability", section):
    #             annex_attributes["eu_type_of_medicine"] = "biologicals"

    #     # TODO: to add attributes, initial EU conditions and current EU conditions, 50 and 51 in bible

    medicine_struct.omars.append(omar_attributes)
    return medicine_struct















# def get_all(filename: str, xml_data: ET.Element) -> dict:
#     """
#     Gets all attributes of the OMAR XML and returns them in a dictionary
#     Args:
#         filename (str): name of the XML file to be scraped
#         xml_data (ET.Element): the contents of the XML file

#     Returns:
#         dict: Dictionary of all scraped attributes, named according to the bible
#     """
#     omar = {"filename": filename[:len(filename) - 4]}  # removes extension
#     return omar


# def parse_file(filename: str, directory: str, medicine_struct: PIS.parsed_info_struct) -> PIS.parsed_info_struct:
#     """
#     Scrapes all attributes from the OMAR XML file after parsing it
#     Args:
#         filename (str): name of the XML file to be scraped
#         directory (str): path of the directory containing the XML file
#         medicine_struct (PIS.parsed_info_struct): the dictionary of all currently scraped attributes of this medicine

#     Returns:
#         PIS.parsed_info_struct: a more complete dictionary of scraped attributes,
#         including the attributes of this XML file
#     """
#     filepath = path.join(directory, filename)
#     try:
#         xml_tree = ET.parse(filepath)
#     except ET.ParseError:
#         print("OMAR PARSER: failed to open XML file " + filepath)
#         return medicine_struct
#     xml_root = xml_tree.getroot()
#     xml_body = xml_root[1]
#     medicine_struct.omars.append(get_all(filename, xml_body))
#     return medicine_struct
