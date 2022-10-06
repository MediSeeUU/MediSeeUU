import pdf_xml_converter as xmlc
import xml.etree.ElementTree as ET
import parsed_info_struct as PIS
import xml_parsing_utils as Utils
import epar_parsing_functions as EPF
import PDFhelper as ph


def parse_epar_file(filepath: str):
    xmlc.convert_pdf_to_xml(filepath, filepath + ".xml", True)
    xml_tree = ET.parse(filepath + ".xml")
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]

    for section in xml_body:
        section_header = section[0]
        print(section_header.text)
    #print(xml_body)
        # if Utils.section_contains_header_number("1.1", section):
        # APF.scrape_medicine_name()


parse_epar_file("epars/h065_procedural_steps.pdf")
