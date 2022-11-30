# OMAR parser
import re
import xml.etree.ElementTree as ET
import scraping.pdf_parser.parsed_info_struct as pis
import scraping.utilities.xml.xml_parsing_utils as xml_utils
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.values as values
import logging
import os

log = logging.getLogger("pdf_parser")


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
        attr.pdf_file: xml_utils.file_get_name_pdf(xml_header),
        attr.xml_file: os.path.basename(filepath),
        attr.creation_date: creation_date,
        attr.modification_date: modification_date,
        attr.ema_omar_condition: []
    }

    # loop through sections and parse section if conditions met
    for section in xml_body:
        # scrape attributes specific to authorization annexes

        # Detect a condition
        if xml_utils.section_contains_header_substring_set_all(["comp", "adopted", "on"], section) \
                and not xml_utils.section_is_table_of_contents(section):

            section_string = xml_utils.section_append_paragraphs(section)
            bullet_points = section_string.split("•")

            alternative_treatments = get_alternative_treatments(bullet_points)
            omar_condition_dict = {
                attr.ema_prevalence: get_prevalence(bullet_points),
                attr.ema_insufficient_roi: get_insufficient_roi(bullet_points),
                attr.ema_alternative_treatments: alternative_treatments,
                attr.ema_significant_benefit: get_significant_benefit(bullet_points, alternative_treatments, filepath)
            }

            omar_attributes[attr.ema_omar_condition].append(omar_condition_dict)

    medicine_struct.omars.append(omar_attributes)

    if len(omar_attributes[attr.ema_omar_condition]) == 0:
        log.warning("OMAR PARSER: failed to parse condition from " + omar_attributes[attr.pdf_file])

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
        if "in 10.000" in b or "in 10,000" in b:
            # Remove unnecessary whitespaces and newlines, in addition, removes the space at the start of the string
            clean = re.sub(r'\s+', ' ', b).lstrip(" ")
            return clean

    return values.not_found


# No OMARs have been found containing this piece of information, so far.
def get_insufficient_roi(bullet_points: list[str]) -> str:
    return values.not_found


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
        b = re.sub(r'\s+', ' ', b).lstrip(" ")

        if ("no satisfactory method" in b) or ("no satisfactory treatment" in b):      
            return "No Satisfactory Method"
        if "significant benefit" in b:
            if "does not hold" in b:
                return values.eu_alt_treatment_no_benefit
            else:
                return values.eu_alt_treatment_benefit

    return values.not_found


def get_significant_benefit(bullet_points: list[str], alternative_treatment: str, filepath: str) -> str:
    """
    This function parses out the significant benefit of the OMAR, 
    the result is influenced by the result of a previous attribute.

    Args:
        bullet_points (list[str]): These are all the bullet points from the appropriate section.
        alternative_treatment (str): The result of the get_alternative_treatment function
        filepath (str): Filepath of OMAR file

    Returns:
        str: Returns the appropriate string, depending on what was found in the file.
    """
    contains = False    
    result = ""

    for b in bullet_points:
        b = re.sub(r'\s+', ' ', b).lstrip(" ")

        if "clinically relevant advantage" in b:
            if "could not establish" in b:
                contains = False
            else:
                contains = True
                result += "Clinically Relevant Advantage"
        
        if "significant clinical efficacy" in b:
            contains = True
            result += "Significant Clinical Efficacy"

        if "major contribution" in b:
            if "insufficient and inconclusive data" in b:
                contains = False
            else:
                contains = True
                if result == "":
                    result += "Major Contribution"
                else:
                    result += " + Major Contribution"

    if not contains and alternative_treatment == "Significant Benefit":
        log.warning("OMAR PARSER: Alternative treatment = Significant benefit requires result for " + filepath)

    if contains:
        return result
    else:
        return values.not_found
