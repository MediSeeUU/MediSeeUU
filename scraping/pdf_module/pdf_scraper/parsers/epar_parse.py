# EPAR parser
import re
import scraping.pdf_module.pdf_scraper.helper as helper
import scraping.pdf_module.pdf_scraper.xml_parsing_utils as xpu
import xml.etree.ElementTree as ET
import scraping.pdf_module.pdf_scraper.parsed_info_struct as PIS
import os.path as path
from typing import Union

date_pattern: str = r"\d{1,2} \w+ \d{4}"  # DD/MONTH/YYYY
procedure_info: str = "information on the procedure"  # Header in EPAR files: Background information on the procedure


def get_all(filename: str, xml_data: ET.Element) -> dict:
    """
    Gets all attributes of the EPAR XML and returns them in a dictionary
    Args:
        filename (str): name of the XML file to be scraped
        xml_data (ET.Element): the contents of the XML file

    Returns:
        dict: Dictionary of all scraped attributes, named according to the bible
    """
    epar = {"filename": filename[:len(filename) - 4],  # removes extension
            "ema_procedure_start_initial": get_date(xml_data),
            "chmp_opinion_date": get_opinion_date(xml_data),
            "eu_legal_basis": get_legal_basis(xml_data),
            "eu_prime_initial": get_prime(xml_data),
            "ema_rapp": get_rapp(xml_data),
            "ema_corapp": get_corapp(xml_data)}
    return epar


def parse_file(filename: str, directory: str, medicine_struct: PIS.parsed_info_struct) -> PIS.parsed_info_struct:
    """
    Scrapes all attributes from the EPAR XML file after parsing it
    Args:
        filename (str): name of the XML file to be scraped
        directory (str): path of the directory containing the XML file
        medicine_struct (PIS.parsed_info_struct): the dictionary of all currently scraped attributes of this medicine

    Returns:
        PIS.parsed_info_struct: a more complete dictionary of scraped attributes,
        including the attributes of this XML file
    """
    filepath = path.join(directory, filename)
    try:
        xml_tree = ET.parse(filepath)
    except ET.ParseError:
        print("EPAR PARSER: failed to open XML file " + filepath)
        return medicine_struct
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]
    medicine_struct.epars.append(get_all(filename, xml_body))
    return medicine_struct


def get_date(xml: ET.Element) -> str:
    """
    Gets the attribute ema_procedure_start_initial
    The initial authorization date of the EMA
    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        str: the attribute ema_procedure_start_initial - a string of a date in DD/MM/YYYY format
    """
    found = False
    regex_date = re.compile(date_pattern)
    regex_ema = re.compile(r"the application was received by the em\w+ on")
    regex_ema2 = re.compile(r"the procedure started on")
    for p in xpu.get_paragraphs_by_header("steps taken for the assessment", xml):
        if found and regex_date.search(p):
            return helper.convert_months(re.search(date_pattern, p)[0])
        elif regex_ema.search(p) or regex_ema2.search(p):
            found = True
            if regex_date.search(p):
                return helper.convert_months(re.search(date_pattern, p)[0])
    return "no_date_found"


def get_opinion_date(xml: ET.Element) -> str:
    """
    Gets the attribute chmp_opinion_date
    The date of the CHMP opinion on the medicine
    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        str: the attribute chmp_opinion_date - a string of a date in DD/MM/YYYY format
    """
    for p in xpu.get_paragraphs_by_header("steps taken for the assessment", xml):
        if re.findall(date_pattern, p):
            date = helper.convert_months(re.findall(date_pattern, p)[-1])
            # Date contains emea instead of month, returns not found
            # TODO: Find correct date when emea is given
            if re.search(r"emea", date):
                return "no_chmp_found"
            return date
    return "no_chmp_found"


def get_legal_basis(xml: ET.Element) -> [str]:
    """
    Gets the attribute eu_legal_basis
    All legal articles relevant to the medicine
    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        str: the attribute eu_legal_basis - multiple articles of the form "Article X.X"
    """
    regex_legal = r"article [\s\S]+?(?=[a-z]{2,90})"
    found = False
    for p in xpu.get_paragraphs_by_header("legal basis for", xml):
        if re.findall(regex_legal, p):
            return helper.convert_articles(re.findall(regex_legal, p))
    for p in xpu.get_paragraphs_by_header("submission of the dossier", xml):
        if found and re.findall(regex_legal, p):
            return helper.convert_articles(re.findall(regex_legal, p))
        elif "legal basis for" in p:
            found = True

    return "no_legal_basis"


def get_prime(xml: ET.Element) -> str:
    """
    Gets the attribute eu_prime_initial
    Whether the medicine is a priority medicine (PRIME)
    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        str: the attribute eu_prime_initial - "yes" or "no"
    """
    for p in xpu.get_paragraphs_by_header("submission of the dossier", xml):
        if re.findall(r" prime ", p):
            return "yes"
        if re.findall(r"priority medicine", p):
            return "yes"
    return "no"


def get_rapp(xml: ET.Element) -> str:
    """
    Gets the attribute ema_rapp
    The main rapporteur of the document, usually found after "rapporteur:"
    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        str: the attribute ema_rapp - the name of the main rapporteur or "no_rapporteur"
    """
    found = False
    rapporteur = ""
    for elem in xml.iter():
        txt = str(elem.text)
        # Find rapporteur between "rapporteur:" and "co-rapporteur"
        if find_rapp_between_rapp_and_corapp(txt) is not None:
            return find_rapp_between_rapp_and_corapp(txt)
        # Find rapporteur after "rapporteur: " and before "\n"
        regex_str_2 = r"rapporteur:[\s\w\.]+?\n"
        if re.findall(regex_str_2, txt):
            temp_rapp = get_rapp_after(regex_str_2, txt, 12)
            if temp_rapp:
                return temp_rapp
        # Find rapporteur after "rapporteur appointed by the chmp was"
        regex_str_3 = r"rapporteur appointed by the chmp was[\s\S]+"
        if re.findall(regex_str_3, txt):
            temp_rapp = get_rapp_after(regex_str_3, txt, 37)
            if temp_rapp:
                return temp_rapp
        # Find rapporteur after "rapporteur:" with found boolean to get rapporteur in new section
        if found:
            # Combine first part of rapporteur like "dr." with next part of rapporteur
            rapporteur += txt.strip().replace("\n", "")
            if len(rapporteur) >= 4:
                found = False
                return rapporteur
        # Find rapporteur after "rapporteur:"
        regex_str_4 = r"rapporteur:[\s\w\.]+"
        if re.search(regex_str_4, txt) and not found:
            rapporteur = get_rapp_after(regex_str_4, txt, 12)
            if len(rapporteur) < 4:
                found = True
            else:
                return rapporteur

    return "no_rapporteur"


def find_rapp_between_rapp_and_corapp(txt: str) -> Union[str, None]:
    """
    A supporting function for finding the rapporteur of the document that
    finds the rapporteur in a certain section in some cases (other cases are processed in the main function)
    Args:
        txt (str): a section of the xml document

    Returns:
        str or None: the attribute ema_rapp - the name of the main rapporteur or None if no rapporteur is found
    """
    regex_str_1 = r"rapporteur:[\s\S]+?(co-rapporteur|corapporteur)"
    if re.findall(regex_str_1, txt):
        rapporteur = re.search(regex_str_1, txt)[0][12:]
        rapporteur = rapporteur[:len(rapporteur) - 14]
        rapporteur = clean_rapporteur(rapporteur)
        return rapporteur


def get_rapp_after(regex_str: str, txt: str, from_char: int) -> str:
    """
    A supporting function for finding the (co-)rapporteur of the document that
    finds the (co-)rapporteur in a certain section using a given regex string.

    Args:
        regex_str (str): The regex string to search for in the section (txt)
        txt (str): a section of the xml document
        from_char (int): The number of characters to remove from the head of the string

    Returns:
        str: the attribute ema_rapp or ema_corapp - the name of the (co-)rapporteur
    """
    rapporteur = re.search(regex_str, txt)[0][from_char:].replace(":", "")
    rapporteur = clean_rapporteur(rapporteur)
    return rapporteur


def clean_rapporteur(rapporteur: str) -> str:
    """
    From a string containing the rapporteur, as well as spaces, enters, and other text,
    this function tries to remove all whitespace and trailing irrelevant text from the rapporteur string
    Args:
        rapporteur (str): the uncleaned string with whitespace and trailing text

    Returns:
        (str): the cleaned string containing only the rapporteur

    """
    rapporteur = rapporteur.strip().replace("\n", "").replace("rapporteur:", "")
    # stop when "the application was" or "the applicant submitted" or "the rapporteur appointed" is found
    if re.search("(the application was|the applicant submitted|the rapporteur appointed)", rapporteur):
        rapporteur = re.search(r"[\s\S]+?(the application was|the applicant submi|the rapporteur appo)", rapporteur)[0]
        rapporteur = rapporteur[:len(rapporteur) - 20].strip()
    # stop when "•" or "" is found
    if re.search("[•|]", rapporteur):
        rapporteur = re.search(r"[\s\S]+?[•|]", rapporteur)[0]
        rapporteur = rapporteur[:len(rapporteur) - 2].strip()
    # take the first part of rapporteur when two spaces are found
    if "  " in rapporteur:
        rapporteur = rapporteur.split("  ")[0].strip()
    return rapporteur


def get_corapp(xml: ET.Element) -> str:
    """
    Gets the attribute ema_corapp
    The co-rapporteur of the document, usually found after "co-rapporteur:"
    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        str: the attribute ema_corapp - the name of the co-rapporteur or "no_co-rapporteur"
    """
    found = False
    corapporteur = ""
    for elem in xml.iter():
        txt = str(elem.text)
        # Find co-rapporteur after "co-rapporteur:" and before "\n"
        regex_str_1 = r"co-rapporteur:[\s\w]+?\n"
        if re.findall(regex_str_1, txt):
            temp_corapp = get_rapp_after(regex_str_1, txt, 15)
            if temp_corapp:
                return temp_corapp

            # Find corapporteur after "co-rapporteur:" with found boolean to get corapp in new section
            if found:
                # Combine first part of corapp like "dr." with next part of corapporteur
                corapporteur += txt.strip().replace("\n", "")
                if len(corapporteur) >= 4:
                    found = False
                    return corapporteur
            # Find co-rapporteur after "co-rapporteur:"
            regex_str_2 = r"co-rapporteur:[\s\w\.]+"
            if re.search(regex_str_2, txt) and not found:
                corapporteur = get_rapp_after(regex_str_2, txt, 15)
                if len(corapporteur) < 4:
                    found = True
                else:
                    return corapporteur
    return "no_co-rapporteur"
