# EPAR parser
import re
import xml_parsing_utils as xpu
import xml.etree.ElementTree as ET
import parsed_info_struct as PIS
import os.path as path


def get_all(filename: str, xml_data: ET.Element):
    omar = {"filename": filename[:len(filename) - 4]} # removes extension
    return omar


def parse_file(filename: str, directory: str, medicine_struct: PIS.parsed_info_struct):
    xml_tree = ET.parse(path.join(directory, filename))
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]
    medicine_struct.omars.append(get_all(filename, xml_body))
    return medicine_struct
