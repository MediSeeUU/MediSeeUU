# EPAR parsers
import re
import pdf_helper
import helper as h
import xml_parsing_utils as xpu
import xml.etree.ElementTree as ET
import os.path as path

date_pattern: str = r'\d{1,2} \w+ \d{4}'
procedure_info = 'information on the procedure'


def get_all(filename, xml_data):
    epar = ['filename:' + filename,
            'ema_procedure_start_initial:' + get_date(xml_data),
            'chmp_opinion_date:' + get_opinion_date(xml_data),
            'eu_legal_basis:' + get_legal_basis(xml_data)]
    return epar


def parse_file(filename, directory, medicine_struct):
    xml_tree = ET.parse(path.join(directory, filename))
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]
    medicine_struct.epars.append(get_all(filename, xml_body))
    return medicine_struct


# ema_procedure_start_initial
def get_date(xml):
    found = False
    regex_date = re.compile(date_pattern)
    regex_ema = re.compile(r'the application was received by the em\w+ on')
    regex_ema2 = re.compile(r'the procedure started on')
    for p in xpu.get_paragraphs_by_header('steps taken for the assessment', xml):
        if found and regex_date.search(p):
            return h.convert_months(re.search(date_pattern, p)[0])
        elif regex_ema.search(p) or regex_ema2.search(p):
            found = True
            if regex_date.search(p):
                return h.convert_months(re.search(date_pattern, p)[0])
    return 'no_date_found'


# chmp_opinion_date
def get_opinion_date(xml):
    for p in xpu.get_paragraphs_by_header('steps taken for the assessment', xml):
        if re.findall(date_pattern, p):
            return h.convert_months(re.findall(date_pattern, p)[-1])
    return 'no_chmp_found'


# eu_legal_basis
def get_legal_basis(xml):
    regex_legal = re.compile(r'article [^ ]+')
    found = False
    for p in xpu.get_paragraphs_by_header('steps taken for the assessment', xml):
        if re.findall(regex_legal, p):
            if found and re.search(regex_legal, p):
                return re.search(r'article [^ ]+', p)[0]
            elif 'legal basis for' in p:
                found = True
    return 'none'


# eu_legal_basis
def table_get_prime(xml):
    return xml
