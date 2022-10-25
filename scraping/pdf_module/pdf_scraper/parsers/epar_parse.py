# EPAR parser
import re
import scraping.pdf_module.pdf_scraper.helper as h
import scraping.pdf_module.pdf_scraper.xml_parsing_utils as xpu
import xml.etree.ElementTree as ET
import scraping.pdf_module.pdf_scraper.parsed_info_struct as PIS
import os.path as path

date_pattern: str = r"\d{1,2} \w+ \d{4}"  # DD/MONTH/YYYY
procedure_info: str = "information on the procedure"  # Header in EPAR files: Background information on the procedure


# Gets all attributes of the XML and returns them in a dictionary
def get_all(filename: str, xml_data: ET.Element) -> dict:
    epar = {"filename": filename[:len(filename) - 4],  # removes extension
            "ema_procedure_start_initial": get_date(xml_data),
            "chmp_opinion_date": get_opinion_date(xml_data),
            "eu_legal_basis": get_legal_basis(xml_data),
            "eu_prime_initial": get_prime(xml_data),
            "ema_rapp": get_rapp(xml_data),
            "ema_corapp": get_corapp(xml_data)}
    return epar


# Scrapes all attributes from the XML file after parsing it
def parse_file(filename: str, directory: str, medicine_struct: PIS.parsed_info_struct) -> PIS.parsed_info_struct:
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
# The initial authorization of the EMA
def get_date(xml: ET.Element) -> str:
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
# The date of the CHMP opinion on the medicine
def get_opinion_date(xml: ET.Element) -> str:
    for p in xpu.get_paragraphs_by_header("steps taken for the assessment", xml):
        if re.findall(date_pattern, p):
            date = h.convert_months(re.findall(date_pattern, p)[-1])
            return date
    return "no_chmp_found"


# eu_legal_basis
# All legal articles relevant to the medicine
def get_legal_basis(xml: ET.Element) -> str:
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
# Whether the medicine is a priority medicine (PRIME)
def get_prime(xml: ET.Element) -> str:
    for p in xpu.get_paragraphs_by_header("submission of the dossier", xml):
        if re.findall(r" prime ", p):
            return "yes"
        if re.findall(r"priority medicine", p):
            return "yes"
    return "no"


# ema_rapp
# The main rapporteur
def get_rapp(xml: ET.Element) -> str:
    found = False
    rapporteur = ""
    for elem in xml.iter():
        txt = str(elem.text)
        # Find rapporteur between "rapporteur:" and "co-rapporteur"
        if find_rapp_1(txt) is not None:
            return find_rapp_1(txt)
        # Find rapporteur after "rapporteur: " and before "\n"
        regex_str_2 = r"rapporteur: [\s\w]+?\n"
        if re.findall(regex_str_2, txt):
            return get_rapp_after(regex_str_2, txt, 12)
        # Find rapporteur after "rapporteur appointed by the chmp was"
        regex_str_3 = r"rapporteur appointed by the chmp was[\s\S]+"
        if re.findall(regex_str_3, txt):
            return get_rapp_after(regex_str_3, txt, 37)
        # Find rapporteur after "rapporteur:"
        regex_str_4 = r"rapporteur:[\s\w]*"
        if re.search(regex_str_4, txt):
            rapporteur = get_rapp_after(regex_str_4, txt, 12)
            # Combine first part of rapporteur like "dr." with next part of rapporteur
            if len(rapporteur) < 4:
                found = True
            else:
                return get_rapp_after(regex_str_4, txt, 12)
        # Find rapporteur after "rapporteur:" with found boolean to get rapporteur in new section
        if found:
            found = False
            rapporteur += txt.strip().replace("\n", "")
            return rapporteur

    return "no_rapporteur"


def find_rapp_1(txt: str) -> str:
    regex_str_1 = r"rapporteur:[\s\S]*?(co-rapporteur|corapporteur)"
    if re.findall(regex_str_1, txt):
        rapporteur = re.search(regex_str_1, txt)[0][12:]
        rapporteur = rapporteur[:len(rapporteur) - 14]
        # stop when "•" or "" is found
        if re.search("[•|]", rapporteur):
            rapporteur = re.search(r"[\s\S]+?[•|]", rapporteur)[0]
            rapporteur = rapporteur[:len(rapporteur) - 2]
        # stop when "the application was" or "the applicant submitted" is found
        if re.search("(the application was|the applicant submitted)", rapporteur):
            rapporteur = re.search(r"[\s\S]+?(the application was|the applicant submi)", rapporteur)[0]
            rapporteur = rapporteur[:len(rapporteur) - 20]
        rapporteur = rapporteur.strip().replace("\n", "")
        return rapporteur


def get_rapp_after(regex_str: str, txt: str, from_char: int) -> str:
    rapporteur = re.search(regex_str, txt)[0][from_char:]
    # stop when "the application was" or "the applicant submitted" is found
    if re.search("(the application was|the applicant submitted)", rapporteur):
        rapporteur = re.search(r"[\s\S]+?(the application was|the applicant submi)", rapporteur)[0]
        rapporteur = rapporteur[:len(rapporteur) - 20]
    rapporteur = rapporteur.strip().replace("\n", "")
    return rapporteur


# ema_corapp
# The co-rapporteur
def get_corapp(xml: ET.Element) -> str:
    found = False
    corapporteur = ""
    for elem in xml.iter():
        txt = str(elem.text)
        # Find co-rapporteur after "co-rapporteur:" and before "\n"
        regex_str_1 = r"co-rapporteur:[\s\w]+?\n"
        if re.findall(regex_str_1, txt):
            return get_rapp_after(regex_str_1, txt, 15)
        # Find co-rapporteur after "co-rapporteur:"
        regex_str_2 = r"co-rapporteur:[\s\w]*"
        if re.findall(regex_str_2, txt):
            corapporteur = get_rapp_after(regex_str_2, txt, 15)
            # Combine first part of co-rapporteur like "dr." with next part of co-rapporteur
            if len(corapporteur) < 4:
                found = True
            else:
                return get_rapp_after(regex_str_2, txt, 15)
        # Find rapporteur after "rapporteur:" with found boolean to get rapporteur in new section
        if found:
            found = False
            corapporteur += txt.strip().replace("\n", "")
            return corapporteur
    return "no_co-rapporteur"
