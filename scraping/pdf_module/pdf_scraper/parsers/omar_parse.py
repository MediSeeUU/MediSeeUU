# EPAR parser
import re
import scraping.pdf_module.pdf_scraper.xml_parsing_utils as xpu
import xml.etree.ElementTree as ET
import scraping.pdf_module.pdf_scraper.parsed_info_struct as PIS
import os.path as path


def get_all(filename: str, xml_data: ET.Element) -> dict:
    """
    Gets all attributes of the OMAR XML and returns them in a dictionary
    Args:
        filename (str): name of the XML file to be scraped
        xml_data (ET.Element): the contents of the XML file

    Returns:
        dict: Dictionary of all scraped attributes, named according to the bible
    """
    omar = {"filename": filename[:len(filename) - 4]}  # removes extension
    return omar


def parse_file(filename: str, directory: str, medicine_struct: PIS.parsed_info_struct) -> PIS.parsed_info_struct:
    """
    Scrapes all attributes from the OMAR XML file after parsing it
    Args:
        filename (str): name of the XML file to be scraped
        directory (str): path of the directory containing the XML file
        medicine_struct (PIS.parsed_info_struct): the dictionary of all currently scraped attributes of this medicine

    Returns:
        PIS.parsed_info_struct: a more complete dictionary of scraped attributes,
        including the attributes of this XML file
    """
    filepath = path.join(directory, filename)
    try:
        xml_tree = ET.parse(filepath)
    except ET.ParseError:
        print("OMAR PARSER: failed to open XML file " + filepath)
        return medicine_struct
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]
    medicine_struct.omars.append(get_all(filename, xml_body))
    return medicine_struct
