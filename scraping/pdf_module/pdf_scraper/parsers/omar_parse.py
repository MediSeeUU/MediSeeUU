# OMAR parser
import re
from tkinter import HORIZONTAL
import xml.etree.ElementTree as ET
import scraping.pdf_module.pdf_scraper.parsed_info_struct as PIS
import scraping.pdf_module.pdf_scraper.xml_parsing_utils as Utils
import os.path as path


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


def get_all(filepath: str, xml_data: ET.Element) -> dict:
    """
    Gets all attributes of the OMAR XML and returns them in a dictionary
    Args:
        filename (str): name of the XML file to be scraped
        xml_data (ET.Element): the contents of the XML file

    Returns:
        dict: Dictionary of all scraped attributes, named according to the bible
    """
    omar = {
        "xml_file": get_xml_name(filepath)
        }
    
    n_indications = get_indications(xml_data)

    if (n_indications == 1):
        omar["indication_1"] = get_indication_attributes(xml_data)
    else:
        for i in range(1, n_indications + 1):
            omar_data = get_correct_indication(xml_data, i)
            omar[f'indication_{i}'] = get_indication_attributes(xml_data)

    return omar

def get_indication_attributes(xml_data: ET.Element) -> dict:
    at = get_alternative_treatments(xml_data)

    indication = {
        "prevalence": get_prevalence(xml_data),
        "insufficient_roi": get_insufficient_roi(xml_data),
        "alternative_treatments": at,
        "significant_benefit": get_significant_benefit(xml_data, at)
    }

    return indication


def get_correct_indication(xml_data: ET.Element, index: int) -> list[str]:
    #print(index)
    return



def get_indications(xml_data: ET.Element) -> int:
    count = 0
    for p in Utils.get_paragraphs_by_header("introductory comment", xml_data):
        if "•" in p:
            count += 1

    if count == 0:
        return 1
    else:
        return count


def get_xml_name(filepath: str) -> str:
    return filepath.split("\\")[-1]


def get_prevalence(xml_data: ET.Element) -> str:
    """
    Finds the paragraph that contains the information about the prevalence of the medicine.

    Args:
        xml_data (ET.Element): This is the XML part to be parsed.

    Returns:
        str: Return the string with the relevant information about the prevalence or NA if it cannot be found.
    """    
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


# Nog geen OMAR gevonden waar dit in staat dus kan nog niet gedaan worden
def get_insufficient_roi(xml_data: ET.Element) -> str:
    return "NA"


# WIP WIP WIP WIP WIP
def get_alternative_treatments(xml_data: ET.Element) -> str:
    for p in Utils.get_paragraphs_by_header("comp position adopted", xml_data):
        # Find the paragraph with the bullet points
        if "•" in p:
            bullets = p.split("•")
            # Find the bullet point with the alternative treatment data in it
            for b in bullets:
                if "no satisfactory methods" in b:
                    return "No Satisfactory Methods"
                if "significant benefit" in b:
                    return "Significant Benefit"
    return "NA"


def get_significant_benefit(xml_data: ET.Element, alternative_treatment: str) -> str: 
    contains = False
    result = ""

    for p in Utils.get_paragraphs_by_header("comp position adopted", xml_data):
        # Find the paragraph with the bullet points
        if "•" in p:
            bullets = p.split("•")
            # Find the bullet point with the prevalence data in it
            for b in bullets:
                if "clinically relevant advantage" in b:
                    contains = True
                    result += "Clinically Relevant Advantage"
                if "major contribution" in b:
                    contains = True
                    if result == "":
                        result += "Major Contribution"
                    else:
                        result += " + Major Contribution"

    # TODO: Uncomment this if logger works
    #if not contains and alternative_treatment == "Significant Benefit":        
        # Logger.warning("Alternative treatment = Significant benefit requires result.")

    if contains:
        return result
    else:
        return "NA"














