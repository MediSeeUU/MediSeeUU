# OMAR parser
import re
import xml.etree.ElementTree as ET
import scraping.pdf_module.pdf_scraper.parsed_info_struct as PIS
import scraping.pdf_module.pdf_scraper.xml_parsing_utils as Utils
import os.path as path


def get_all(filepath: str, xml_data: ET.Element) -> dict:
    """
    Gets all attributes of the OMAR XML and returns them in a dictionary
    Args:
        filename (str): name of the XML file to be scraped
        xml_data (ET.Element): the contents of the XML file

    Returns:
        dict: Dictionary of all scraped attributes, named according to the bible
    """
    at = get_alternative_treatments(xml_data)

    omar = {
        "xml_file": get_xml_name(filepath),
        "prevalence": get_prevalence(xml_data),
        "insufficient_roi": get_insufficient_roi(xml_data),
        "alternative_treatments": at,
        "significant_benefit": get_significant_benefit(xml_data, at)
    }

    return omar


def parse_file(filepath: str, medicine_struct: PIS.parsed_info_struct) -> PIS.parsed_info_struct:
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
    try:
        xml_tree = ET.parse(filepath)
    except ET.ParseError:
        print("OMAR PARSER: failed to open XML file " + filepath)
        return medicine_struct

    if medicine_struct is None:
        print("OMAR PARSER: medicine_struct is none at " + filepath)
        return

    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]

    result = get_all(filepath, xml_body)
    medicine_struct.omars.append(result)
    
    return medicine_struct


def get_xml_name(filepath: str) -> str:
    return filepath.split("\\")[-1]


def get_prevalence(xml_data: ET.Element) -> str:
    for p in Utils.get_paragraphs_by_header("comp position adopted", xml_data):
        # Find the paragraph with the bullet points
        if "•" in p:
            bullets = p.split("•")
            # Find the bullet point with the prevalence data in it
            for b in bullets:
                if "the prevalence of" in b:
                    # Remove unnecessary whitespaces and newlines
                    clean = re.sub('\s+',' ', b).lstrip(" ")
                    return clean
    return "NA"


def get_insufficient_roi(xml_data: ET.Element) -> str:
    return "NA"


# WIP WIP WIP WIP WIP
def get_alternative_treatments(xml_data: ET.Element) -> str:
    for p in Utils.get_paragraphs_by_header("comp position adopted", xml_data):
        # Find the paragraph with the bullet points
        if "•" in p:
            bullets = p.split("•")
            # Find the bullet point with the prevalence data in it
            for b in bullets:
                if "no satisfactory methods" in b:
                    return "No Satisfactory Methods"
                if "significant benefit" in b:
                    return "Significant Benefit"
    return "NA"


def get_significant_benefit(xml_data: ET.Element, alternative_treatment: str) -> str: 
    return "NA"














