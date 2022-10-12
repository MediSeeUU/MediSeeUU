# EPAR parsers
import re
import pdf_helper
import helper
import xml_parsing_utils as xpu
import xml.etree.ElementTree as ET

date_pattern: str = r'\d{1,2} \w+ \d{4}'
procedure_info = 'information on the procedure'


def get_all(filedata, xml_data):
    filedata.ema_procedure_start_initial = get_date(xml_data)
    #filedata.chmp_opinion_date = get_opinion_date(xml_data)
    #filedata.eu_legal_basis = get_legal_basis(xml_data)
    return filedata


def parse_file(file_path, medicine_struct):
    print(file_path)
    xml_tree = ET.parse(file_path)
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]
    medicine_struct.epars = get_all(medicine_struct, xml_body)
    return medicine_struct


# ema_procedure_start_initial
def get_date(xml):
    found = False
    regex_date = re.compile(date_pattern)
    regex_ema = re.compile(r'the application was received by the em\w+ on')
    for section in xml:
        if xpu.section_contains_header_number('1', section[0]):
            for p in section:
                print (p.text)
            # if found and regex_date.search(section):
            #     return re.search(date_pattern, section)[0]
            # elif regex_ema.search(section):
            #     found = True
            #     if regex_date.search(section):
            #         return re.search(date_pattern, section)[0]
    return ''


# chmp_opinion_date
def get_opinion_date(xml):
    section = xml['background']['main_text']
    list_size = len(section)
    regex_date = re.compile(date_pattern)
    for i in range(list_size):
        if regex_date.search(section[list_size - i - 1]):
            return re.search(date_pattern, section[list_size - i - 1])[0]
    return ''


# eu_legal_basis
def get_legal_basis(xml: object) -> object:
    section = xml['background']['main_text']
    found = False
    regex_legal = re.compile(r'article [^ ]+')
    for txt in section:
        if found and regex_legal.search(txt):
            return re.search(r'article [^ ]+', txt)[0]
        elif 'legal basis for' in txt:
            found = True
    return 'none'


# eu_legal_basis
def table_get_prime(xml):
    return xml
