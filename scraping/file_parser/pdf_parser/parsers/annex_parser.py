import scraping.file_parser.xml_converter.__main__ as xml_converter
import xml.etree.ElementTree as ET
import scraping.file_parser.xml_converter.xml_parsing_utils as xml_utils
import scraping.file_parser.pdf_parser.parsed_info_struct as pis
import scraping.file_parser.pdf_parser.pdf_helper as pdf_helper
import scraping.logger as logger
import scraping.definitions.attributes as attr
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
        log.warning("ANNEX PARSER: failed to open xml file " + filepath)
        return medicine_struct

    if medicine_struct is None:
        log.warning("ANNEX PARSER: medicine_struct is none at " + filepath)
        return

    xml_root = xml_tree.getroot()
    xml_header = xml_root[0]
    xml_body = xml_root[1]

    is_initial_file = xml_utils.file_is_initial(xml_header)
    creation_date = xml_utils.file_get_creation_date(xml_header)
    modification_date = xml_utils.file_get_modification_date(xml_header)

    # create annex attribute dictionary with default values
    annex_attributes: dict[str, str] = {"pdf_file": xml_utils.file_get_name_pdf(xml_header),
                                        "xml_file": os.path.basename(filepath),
                                        "is_initial": is_initial_file,
                                        "creation_date": creation_date,
                                        "modification_date": modification_date}

    # add default attribute values for initial authorization annexes
    if is_initial_file:
        annex_attributes[attr.initial_type_of_eu_authorization] = "standard"
        annex_attributes[attr.eu_type_of_medicine] = "small molecule"

    # loop through sections and parse section if conditions met
    for section in xml_body:
        # scrape attributes specific to authorization annexes
        if is_initial_file:
            # initial type of eu authorization
            # override default value of "standard" if "specific obligation" is present anywhere in text
            if xml_utils.section_contains_substring("specific obligation", section) and \
                    annex_attributes[attr.initial_type_of_eu_authorization] != "conditional":
                annex_attributes[attr.initial_type_of_eu_authorization] = "exceptional or conditional"

            # definitely conditional if "conditional approval" anywhere in text
            if xml_utils.section_contains_substring("conditional approval", section):
                annex_attributes[attr.initial_type_of_eu_authorization] = "conditional"

            # EU type of medicine
            # override default value of "small molecule" if traceability header is present
            if xml_utils.section_contains_substring("traceability", section):
                annex_attributes[attr.eu_type_of_medicine] = "biologicals"

        # TODO: to add attributes, initial EU conditions and current EU conditions, 50 and 51 in bible

    medicine_struct.annexes.append(annex_attributes)
    filename = xml_utils.file_get_name_pdf(xml_header)
    if '_0' in filename:
        pdf_helper.create_outputfile(filename, 'annex_results.txt', annex_attributes)
    return medicine_struct
