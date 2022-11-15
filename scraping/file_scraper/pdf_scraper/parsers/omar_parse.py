# OMAR parser
import re
import xml.etree.ElementTree as ET
import scraping.file_scraper.pdf_scraper.parsed_info_struct as pis
import scraping.file_scraper.xml_converter.xml_parsing_utils as xml_utils
import scraping.logger as logger
import os

log = logger.PDFLogger.log


def parse_file(filepath: str, medicine_struct: pis.ParsedInfoStruct):
    """
    1. Load the XML file.
    2. Create a dictionary with all the attributes that need to be scraped.
    3. Loop through the body of the XML and find the attributes.
    4. Append the attributes to the struct and return it.

    Args:
        filepath (str): Path of the XML file to be scraped.
        medicine_struct (PIS.ParsedInfoStruct): The dictionary of all currently scraped attributes of this medicine.

    Returns:
        PIS.ParsedInfoStruct: Returns an updated struct, with the current attributes added to it.
    """

    try:
        xml_tree = ET.parse(filepath)
    except ET.ParseError:
        log.warning("OMAR PARSER: failed to open xml file " + filepath)
        return medicine_struct

    if medicine_struct is None:
        log.warning("OMAR PARSER: medicine_struct is none at " + filepath)
        return medicine_struct

    xml_root = xml_tree.getroot()
    xml_header = xml_root[0]
    xml_body = xml_root[1]

    creation_date = xml_utils.file_get_creation_date(xml_header)
    modification_date = xml_utils.file_get_modification_date(xml_header)

    # create annex attribute dictionary with default values
    omar_attributes = {
        "pdf_file": xml_utils.file_get_name_pdf(xml_header),
        "xml_file": os.path.basename(filepath),
        "creation_date": creation_date,
        "modification_date": modification_date,
        "conditions": []
    }

    # loop through sections and parse section if conditions met
    for section in xml_body:
        # scrape attributes specific to authorization annexes

        # Detect a condition
        if xml_utils.section_contains_header_substring("COMP position adopted on", section) \
                and not xml_utils.section_is_table_of_contents(section):

            section_string = xml_utils.section_append_paragraphs(section)
            bullet_points = section_string.split("•")

            alternative_treatments = get_alternative_treatments(bullet_points)
            omar_condition_dict = {
                "prevalence": get_prevalence(bullet_points),
                "insufficient_roi": get_insufficient_roi(bullet_points),
                "alternative_treatments": alternative_treatments,
                "significant_benefit": get_significant_benefit(bullet_points, alternative_treatments)
            }

            omar_attributes["conditions"].append(omar_condition_dict)

    medicine_struct.omars.append(omar_attributes)

    return medicine_struct


def get_prevalence(bullet_points: list[str]) -> str:
    """
    Finds the paragraph that contains the information about the prevalence of the medicine.

    Args:
        bullet_points (list[str]): These are all the bullet points from the appropriate section.

    Returns:
        str: Return the string with the relevant information about the prevalence or NA if it cannot be found.
    """
    for b in bullet_points:
        if "the prevalence of" in b:
            # Remove unnecessary whitespaces and newlines
            clean = re.sub(r'\s+', ' ', b).lstrip(" ")
            return clean

    return "NA"


# No OMARs have been found containing this piece of information, so far.
def get_insufficient_roi(bullet_points: list[str]) -> str:
    return "NA"


def get_alternative_treatments(bullet_points: list[str]) -> str:
    """
    Finds the bullet point that contains the appropriate information and return
        short description about the findings.

    Args:
        bullet_points (list[str]): These are all the bullet points from the appropriate section.

    Returns:
        str: Return a short description depending on what was found in the bullet point.
    """
    for b in bullet_points:
        if "no satisfactory methods" in b:
            return "No Satisfactory Methods"
        if "significant benefit" in b:
            return "Significant Benefit"

    return "NA"


def get_significant_benefit(bullet_points: list[str], alternative_treatment: str) -> str:
    """
    This function parses out the significant benefit of the OMAR, 
    the result is influenced by the result of a previous attribute.

    Args:
        bullet_points (list[str]): These are all the bullet points from the appropriate section.
        alternative_treatment (str): The result of the get_alternative_treatment function

    Returns:
        str: Returns the appropriate string, depending on what was found in the file.
    """
    contains = False
    result = ""

    for b in bullet_points:
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