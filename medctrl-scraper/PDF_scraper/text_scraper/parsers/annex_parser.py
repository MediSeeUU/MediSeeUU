import pdf_xml_converter as xmlc
import xml.etree.ElementTree as ET
import parsed_info_struct as PIS
import xml_parsing_utils as Utils
import annex_parsing_functions as APF
import PDFhelper as ph


def parse_smpc_file(filepath: str):
    xmlc.convert_pdf_to_xml(filepath, filepath + ".xml", False)
    xml_tree = ET.parse(filepath + ".xml")
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]

    for section in xml_body:
        section_header = section[0]
        print(section_header.text)

        if Utils.section_contains_header_number("1.1", section):
            string = APF.scrape_medicine_name()


#testing
#parse_smpc_file("../EC decision parser Vincent/annexs/anx_156445_en.pdf")