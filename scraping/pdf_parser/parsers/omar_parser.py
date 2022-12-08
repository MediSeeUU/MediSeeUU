# OMAR parser
import re
import xml.etree.ElementTree as ET
import scraping.pdf_parser.parsed_info_struct as pis
import scraping.utilities.xml.xml_parsing_utils as xml_utils
import scraping.utilities.pdf.helper as helper
import scraping.utilities.definitions.values as values
import scraping.utilities.definitions.attributes as attr
import logging
import os
import datetime

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

    pdf_file = xml_utils.file_get_name_pdf(xml_header)
    xml_file = os.path.basename(filepath)
    creation_date = xml_utils.file_get_creation_date(xml_header)
    modification_date = xml_utils.file_get_modification_date(xml_header)
    report_date = get_report_date(xml_body, pdf_file)

    # Create the initial dictionary without the attributes per condition
    omar_attributes = {
        attr.pdf_file: xml_utils.file_get_name_pdf(xml_header),
        attr.xml_file: os.path.basename(filepath),
        attr.creation_date: creation_date,
        attr.modification_date: modification_date,
        attr.ema_omar_condition: []
    }

    # When a comp header has been found, sections split on eu number should be found instead.
    has_comp = False
    # When a final comp has been found, no other comps should be parsed.
    has_final = False

    # Loop through all the sections of the xml body to parse all the attributes
    for section in xml_body:

        # Find comp position sections and scrape attributes from it.
        if xml_utils.section_contains_header_substring_set_all(["comp", "adopted", "on"], section) \
                and not xml_utils.section_is_table_of_contents(section):

            has_comp = True

            attributes = get_attributes(section, False)

            if attributes:
                omar_attributes[attr.ema_omar_condition].append(attributes)

        # Occasionally a file appears that has a different structure, this is used to handle one of those.
        if xml_utils.section_contains_header_substring_set(["eu/"], section) \
                and not xml_utils.section_is_table_of_contents(section) \
                and has_comp:

            attributes = get_attributes(section, has_comp)

            if attributes:
                omar_attributes[attr.ema_omar_condition].append(attributes)

    for dict in omar_attributes[attr.ema_omar_condition]:
        dict[attr.ema_report_date] = report_date

    medicine_struct.omars.append(omar_attributes)

    # When no conditions have been found it will be logged.
    if len(attr.ema_omar_condition) == 0:
        log.warning("OMAR PARSER: failed to parse condition from " + pdf_file)

    return medicine_struct


def get_report_date(xml_body: ET.Element, pdf_file: str) -> datetime.datetime:
    section = xml_utils.get_body_section_by_index(0, xml_body)
    header = xml_utils.get_section_header(section)

    date_string = re.findall(r"(\d{1,2}\s[a-z]+\s\d{4})", header)

    if len(date_string) > 0:
        return helper.get_date(date_string[0])
    else:
        log.warning("OMAR PARSER: failed to parse report date from " + pdf_file)
        return helper.get_date('')


def get_attributes(section: ET.Element, eu_od_flag: bool) -> dict[str, str]:
    """
    This function returns the dictionary with all the parsed attributes in it.
    Args:
        section (ET.Element): Section (ET.Element): This is the section obtained with the xml converter.
        eu_od_flag (bool): This boolean represents the presence of a comp section.
    Returns:
        dict[str, str]: Return a dictionary with the parsed attributes.
    """
    section_string = xml_utils.section_append_paragraphs(section)

    if not section_string:
        return {}

    bullet_points = section_string.split("•")

    alternative_treatments = get_alternative_treatments(bullet_points)
    omar_attributes = {
        attr.eu_od_number: get_eu_od_number(section, eu_od_flag),
        attr.eu_od_prevalence: get_prevalence(bullet_points),
        attr.eu_od_alt_treatment: alternative_treatments,
        attr.eu_od_sig_benefit: get_significant_benefit(bullet_points, alternative_treatments)
    }

    return omar_attributes


def get_eu_od_number(section: ET.Element, eu_od_flag: bool) -> str:
    """
    This function finds the orphan designation number that belongs to a condition.
    Args:
        section (ET.Element): This is the section obtained with the xml converter.
        eu_od_flag (bool): This boolean represents the presence of a comp section.
    Returns:
        str: Returns an eu orphan designation number.
    """
    header = xml_utils.get_section_header(section)

    if eu_od_flag:
        return header

    section_string = xml_utils.section_append_paragraphs(section)

    eu_od_number = re.findall(r"eu/\d+/\d+/\d+", section_string)

    if len(eu_od_number) > 0:
        return eu_od_number[0]
    else:
        return values.not_found


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


def get_significant_benefit(bullet_points: list[str], alternative_treatment: str) -> str:
    """
    This function finds the piece of text that supports the reason for the orphan medicine to be
    of significant benefit.
    Args:
        bullet_points (list[str]): These are all the bullet points from the appropriate section.
        alternative_treatment (str): The result of the get_alternative_treatment function
    Returns:
        str: Returns the appropriate string, depending on what was found in the file.
    """
    # The sentence required for this will be found based on this matching key.
    # Adding the start of the sentence to this list will allow the function to find the sentence.
    matching_key = [
        "the sponsor",
        "this is based on",
        "it was demonstrated",
        "based on",
        "a post-hoc",
        "significant benefit",
        "when the product"
    ]

    if alternative_treatment == "No Significant Benefit":
        return "No Significant Benefit"

    # Loop through all the bullet points and if a paragraph contains certain words, it will
    # look for a sentence that explains it.
    for b in bullet_points:
        b = re.sub(r'\s+', ' ', b).lstrip(" ")

        if ("no satisfactory method" in b) or \
                ("no satisfactory treatment" in b) or \
                ("significant benefit" in b):

            key_suffixed = [s + ".*?\." for s in matching_key]

            joined_regex = "|".join(key_suffixed)

            pattern = r"(?<=\. )(" + joined_regex + r")"

            result = re.findall(pattern, b)

            if len(result) > 0:
                return result[0]

    return values.not_found
