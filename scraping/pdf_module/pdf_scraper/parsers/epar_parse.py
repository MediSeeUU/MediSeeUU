# EPAR parser
import re
import helper as h
import xml_parsing_utils as xpu
import xml.etree.ElementTree as ET
import parsed_info_struct as PIS
import os.path as path

date_pattern: str = r"\d{1,2} \w+ \d{4}"
procedure_info: str = "information on the procedure"


def get_all(filename: str, xml_data: ET.Element):
    epar = {"filename": filename[:len(filename) - 4],  # remove extension
            "ema_procedure_start_initial": get_date(xml_data),
            "chmp_opinion_date": get_opinion_date(xml_data),
            "eu_legal_basis": get_legal_basis(xml_data),
            "eu_prime_initial": get_prime(xml_data),
            "ema_rapp": get_rapp(xml_data),
            "ema_corapp": get_corapp(xml_data)}
    return epar


def parse_file(filename: str, directory: str, medicine_struct: PIS.parsed_info_struct):
    filepath = path.join(directory, filename)
    try:
        xml_tree = ET.parse(filepath)
    except:
        print("EPAR PARSER: failed to open XML file " + filepath)
        return medicine_struct
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]
    medicine_struct.epars.append(get_all(filename, xml_body))
    return medicine_struct


# ema_procedure_start_initial
def get_date(xml: ET.Element):
    found = False
    regex_date = re.compile(date_pattern)
    regex_ema = re.compile(r"the application was received by the em\w+ on")
    regex_ema2 = re.compile(r"the procedure started on")
    for p in xpu.get_paragraphs_by_header("steps taken for the assessment", xml):
        if found and regex_date.search(p):
            return h.convert_months(re.search(date_pattern, p)[0])
        elif regex_ema.search(p) or regex_ema2.search(p):
            found = True
            if regex_date.search(p):
                return h.convert_months(re.search(date_pattern, p)[0])
    return "no_date_found"


# chmp_opinion_date
def get_opinion_date(xml: ET.Element):
    for p in xpu.get_paragraphs_by_header("steps taken for the assessment", xml):
        if re.findall(date_pattern, p):
            date = h.convert_months(re.findall(date_pattern, p)[-1])
            return date
    return "no_chmp_found"


# eu_legal_basis
def get_legal_basis(xml: ET.Element):
    regex_legal = r"article [^ ]+"
    found = False
    for p in xpu.get_paragraphs_by_header("legal basis for", xml):
        if re.findall(regex_legal, p):
            return h.convert_articles(list(re.findall(regex_legal, p)))
    for p in xpu.get_paragraphs_by_header("submission of the dossier", xml):
        if found and re.findall(regex_legal, p):
            return h.convert_articles(list(re.findall(regex_legal, p)))
        elif "legal basis for" in p:
            found = True
    return "no_legal_basis"


# eu_prime_initial
def get_prime(xml: ET.Element):
    for p in xpu.get_paragraphs_by_header("submission of the dossier", xml):
        if re.findall(r" prime ", p):
            return "yes"
        if re.findall(r"priority medicine", p):
            return "yes"
    return "no"


# ema_rapp
def get_rapp(xml: ET.Element):
    for p in xpu.get_paragraphs_by_header("steps taken for the assessment", xml):
        if re.findall(r"rapporteur:[\w\s]+ co-rapporteur:", p):
            rapporteur = re.search(r"rapporteur:[\w\s]+ co-rapporteur:", p)[0][12:]
            return rapporteur.strip()[:len(rapporteur) - 16]
        if re.findall(r"rapporteur:[\w\s]+ \\n", p):
            rapporteur = re.search(r"rapporteur:[\w\s]+\\n", p)[0][12:]
            return rapporteur.strip()
        if re.findall(r"rapporteur:[\w\s]+", p):
            rapporteur = re.search(r"rapporteur:[\w\s]+", p)[0][12:]
            return rapporteur.strip()
    return "no_rapporteur"


# ema_corapp
def get_corapp(xml: ET.Element):
    for p in xpu.get_paragraphs_by_header("steps taken for the assessment", xml):
        if re.findall(r"co-rapporteur: (.*?) \\n", p):
            rapporteur = re.search(r"co-rapporteur: (.*?)\\n", p)[0][15:]
            return rapporteur.replace("\\n", "").rstrip()
    for p in xpu.get_paragraphs_by_header("steps taken for the assessment", xml):
        if re.findall(r"co-rapporteur: (.)+", p):
            rapporteur = re.search(r"co-rapporteur: (.)+", p)[0][15:]
            return rapporteur.replace("\\n", "").rstrip()
    return "no_co-rapporteur"
