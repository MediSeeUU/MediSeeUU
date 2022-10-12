# EPAR parsers
import re
import pdf_helper
import helper
import xml_parsing_utils as xpu
import xml.etree.ElementTree as ET

date_pattern: str = r'\d{1,2} \w+ \d{4}'
procedure_info = 'information on the procedure'


def get_default(filename):
    default = 'Not parsed'
    return {'filename': filename,
            'ema_procedure_start_initial': default,
            'chmp_opinion_date': default,
            'eu_legal_basis': default
            }


def get_all(filedata, xml_data):
    filedata['ema_procedure_start_initial'] = get_date(xml_data)
    filedata['chmp_opinion_date'] = get_opinion_date(xml_data)
    filedata['eu_legal_basis'] = get_legal_basis(xml_data)
    return filedata


def parse_file(filename, medicine_struct):
    filedata = get_default(filename)
    xml_tree = ET.parse(filename)
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]
    filedata = get_all(filedata, xml_body)
    medicine_struct.epars = filedata
    return medicine_struct


# check if table front page is empty (indicating image/unreadable)
def unreadable(xml):
    return not xml['intro']['front_page']


# ema_procedure_start_initial
def get_date(xml):
    found = False
    section = xpu.section_contains_head_substring("background information on the procedure", xml)
    regex_date = re.compile(date_pattern)
    regex_ema = re.compile(r'the application was received by the em\w+ on')
    for txt in section:
        if found and regex_date.search(txt):
            return convert_month(re.search(date_pattern, txt)[0])
        elif regex_ema.search(txt):
            found = True
            if regex_date.search(txt):
                return convert_month(re.search(date_pattern, txt)[0])
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
