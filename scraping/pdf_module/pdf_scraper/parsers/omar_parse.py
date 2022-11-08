# OMAR parser
import re
from tkinter import HORIZONTAL
import xml.etree.ElementTree as ET
import scraping.pdf_module.pdf_scraper.parsed_info_struct as PIS
import scraping.pdf_module.pdf_scraper.xml_parsing_utils as Utils
import os.path as path


def parse_file(filepath: str, medicine_struct: PIS.parsed_info_struct) -> PIS.parsed_info_struct:
    """
    This function parses the OMAR XML file and returns an updated dictionary.

    Args:
        filepath (str): name of the XML file to be scraped
        medicine_struct (PIS.parsed_info_struct): the dictionary of all currently scraped attributes of this medicine

    Returns:
        PIS.parsed_info_struct: Returns a more complete dictionary of scraped attributes,
            including the attributes of this XML file.
    """
    try:
        xml_tree = ET.parse(filepath)
    except ET.ParseError:
        print("OMAR PARSER: failed to open XML file " + filepath)
        return medicine_struct

    if medicine_struct is None:
        print("OMAR PARSER: medicine_struct is none at " + filepath)
        return 

    result = get_all(filepath, xml_tree)
    medicine_struct.omars.append(result)

    return medicine_struct


def get_all(filepath: str, xml_tree: ET.ElementTree) -> dict:
    """
    This function gets all attributes of the OMAR XML and returns them in a dictionary.

    Args:
        filepath (str): name of the XML file to be scraped
        xml_tree (ET.ElementTree): the whole XML tree of the file

    Returns:
        dict: Dictionary of all parsed attributes, named according to the bible.
    """
    xml_root = xml_tree.getroot()
    xml_header = xml_root[0]
    xml_body = xml_root[1]

    omar = {
        "pdf_file": Utils.file_get_name_pdf(xml_header)
    }

    n_indications = get_conditions_number(xml_body)

    # The prefix for the attributes in the JSON file
    condition_prefix = "condition"

    # Each condition will be parsed and added to the dictionary
    if n_indications == 1:
        omar[f"{condition_prefix}_1"] = get_condition_attributes(xml_body)
    else:
        for i in range(1, n_indications + 1):
            omar_data = get_correct_condition(xml_body, i)
            omar[f"{condition_prefix}_{i}"] = get_condition_attributes(xml_body)

    return omar


def get_condition_attributes(xml_data: ET.Element) -> dict:
    """
    This function will parse out all the attributes from a given piece of XML.

    Args:
        xml_data (ET.Element): This is the XML part to be parsed.

    Returns:
        dict: Returns a dictionary of the parsed piece of XML.
    """    
    at = get_alternative_treatments(xml_data)

    indication = {
        "prevalence": get_prevalence(xml_data),
        "insufficient_roi": get_insufficient_roi(xml_data),
        "alternative_treatments": at,
        "significant_benefit": get_significant_benefit(xml_data, at)
    }

    return indication


def get_correct_condition(xml_data: ET.Element, index: int) -> list[str]:
    # print(index)
    return


def get_conditions_number(xml_data: ET.Element) -> int:
    """
    This function gets the amount conditions for an orphan medicine.
    This is necessary because certain OMARs contain multiple conditions.

    Args:
        xml_data (ET.Element): This is the XML part to be parsed.

    Returns:
        int: If no section is detected which contains an indicator for multiple conditions,
             then it is assumed that there is only a single condition.
    """
    count = 0
    for p in Utils.get_paragraphs_by_header("introductory comment", xml_data):
        if "•" in p:
            count += 1

    # If no header is found then it implies that there is only a single condition
    if count == 0:
        return 1
    else:
        return count


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
                    clean = re.sub('\s+', ' ', b).lstrip(" ")
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
    """
    This function parses out the significant benefit of the OMAR, 
    the result is influenced by the result of a previous attribute.

    Args:
        xml_data (ET.Element): This is the XML part to be parsed.
        alternative_treatment (str): The result of the get_alternative_treatment function

    Returns:
        str: Returns the appropriate string, depending on what was found in the file.
    """    
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
    # if not contains and alternative_treatment == "Significant Benefit":
    # Logger.warning("Alternative treatment = Significant benefit requires result.")

    if contains:
        return result
    else:
        return "NA"
