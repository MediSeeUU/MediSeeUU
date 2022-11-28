# EPAR parser
import re
import scraping.file_parser.pdf_parser.helper as helper
import scraping.file_parser.xml_converter.xml_parsing_utils as xml_utils
import xml.etree.ElementTree as ET
import scraping.file_parser.pdf_parser.parsed_info_struct as pis
import scraping.file_parser.pdf_parser.pdf_helper as pdf_helper
import logging
import os.path as path

date_pattern: str = r"\d{1,2} \b(?!emea\b)\w+ \d{4}|\d{1,2}\w{2} \b(?!emea\b)\w+ \d{4}"  # DD/MONTH/YYYY
procedure_info: str = "information on the procedure"  # Header in EPAR files: Background information on the procedure
accelerated_assessment = "accelerated assessment"
steps_taken_assessment_str = "steps taken for the assessment"

log = logging.getLogger("pdf_parser")


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
            "ema_corapp": get_corapp(xml_data),
            "ema_reexamination": get_reexamination(xml_data),
            "eu_accel_assess_g": get_accelerated_assessment(xml_data)}
    return epar


def parse_file(filename: str, directory: str, medicine_struct: pis.ParsedInfoStruct) -> pis.ParsedInfoStruct:
    """
    Gets all attributes from the EPAR XML file after parsing it

    Args:
        filename (str): name of the XML file to be scraped
        directory (str): path of the directory containing the XML file
        medicine_struct (PIS.ParsedInfoStruct): the dictionary of all currently scraped attributes of this medicine

    Returns:
        PIS.ParsedInfoStruct: a more complete dictionary of scraped attributes,
        including the attributes of this XML file
    """
    filepath = path.join(directory, filename)
    try:
        xml_tree = ET.parse(filepath)
    except ET.ParseError:
        log.warning("EPAR PARSER: failed to open XML file " + filepath)
        return medicine_struct
    xml_root = xml_tree.getroot()
    xml_body = xml_root[1]
    res = get_all(filename, xml_body)
    medicine_struct.epars.append(res)
    pdf_helper.res_to_file('epar_results.txt', res, filename)
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
    regex_date = re.compile(date_pattern)
    regex_ema = re.compile(r"the application was received by the em\w+ on")
    regex_ema2 = re.compile(r"the procedure started on")
    count = -1
    found = False

    for elem in xml.iter():
        txt = elem.text
        if not txt:
            continue
        if count >= 0:
            count += 1
        if steps_taken_assessment_str in txt:
            count = 0
        if found and regex_date.search(txt) and count < 30:
            return helper.convert_months(re.search(date_pattern, txt)[0])
        if regex_ema.search(txt) or regex_ema2.search(txt):
            found = True
            if regex_date.search(txt):
                return helper.convert_months(re.search(date_pattern, txt)[0])
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
    not_easily_scrapeable = False
    for p in xml_utils.get_paragraphs_by_header(steps_taken_assessment_str, xml):
        if re.findall(date_pattern, p):
            date = helper.convert_months(re.findall(date_pattern, p)[-1])
            return date
        # Section is found and should always contain the CHMP opinion date
        not_easily_scrapeable = True
    # Look below rapporteur in steps taken for the assessment when not found by default method
    # This is needed as rapporteur is seen as a header when it is bold, causing text below to
    # not be a part of "steps taken for the assessment" anymore.
    right_section = False
    below_rapp = False
    date = ""
    for elem in xml.iter():
        txt = elem.text
        if not txt:
            continue
        if steps_taken_assessment_str in txt:
            right_section = True
        if right_section and "rapporteur" in txt:
            below_rapp = True
        if below_rapp and re.findall(date_pattern, txt):
            date = helper.convert_months(re.findall(date_pattern, txt)[-1])
        if below_rapp and ("scientific discussion" in txt and elem.tag == "header" or txt == "scientific discussion"):
            if date != "":
                return date
            else:
                return "not_easily_scrapeable"
    if date != "":
        return date
    elif not_easily_scrapeable:
        return "not_easily_scrapeable"
    return "no_chmp_found"


def get_legal_basis(xml: ET.Element) -> list[str]:
    """
    Gets the attribute eu_legal_basis
    All legal articles relevant to the medicine

    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        list[str]: the attribute eu_legal_basis - multiple articles of the form "Article X.X"
    """
    regex_legal = r"article .+?(?=[a-z]{2,90}|\n|$)"
    legal_basis_str = "legal basis for"
    found = False
    right_section = False
    legal_basis_exists = False
    count = 0

    for elem in xml.iter():
        txt = elem.text
        if not txt:
            continue
        if "submission of the dossier" in txt:
            right_section = True
        if legal_basis_str in txt:
            found = True
            legal_basis_exists = True
            count = 0
        # For when "legal basis for" appears in the table of contents, triggering found
        if count > 3:
            found = False
        if found:
            count += 1
            if not right_section:
                log.warning("EPAR PARSER: Legal basis found before \"submission of the dossier\"")
            # Get only text after "legal basis for" if this string is in txt
            if len(txt.split(legal_basis_str, 1)) > 1:
                txt = txt.split(legal_basis_str, 1)[1]
            articles = re.findall(regex_legal, txt[:75], re.DOTALL)
            articles2 = re.findall(regex_legal, txt, re.DOTALL)
            if articles:
                return helper.convert_articles(articles)
            # Search in longer text for first legal basis if legal_basis not found after 75 characters
            elif articles2:
                return helper.convert_articles([articles2[0]])

    if legal_basis_exists:
        return ["not_easily_scrapeable"]
    return ["no_legal_basis"]


def get_prime(xml: ET.Element) -> str:
    """
    Gets the attribute eu_prime_initial
    Whether the medicine is a priority medicine (PRIME)

    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        str: the attribute eu_prime_initial - "yes" or "no", "NA" if ema_procedure_start_initial before 01-03-2016
    """
    if check_date_before(xml, 1, 3, 2016):
        return "NA"
    for p in xml_utils.get_paragraphs_by_header("submission of the dossier", xml):
        if re.findall(r" prime ", p) and not re.findall(r"prime importance", p):
            return "yes"
        if re.findall(r"priority medicine", p):
            return "yes"
    return "no"


def check_date_before(xml: ET.Element, check_day: int, check_month: int, check_year: int) -> bool:
    """
        Checks whether the date ema_procedure_start_initial is earlier than the given date

        Args:
            xml (ET.Element): the contents of the XML file
            check_day (int): the day of the given date
            check_month (int): the month of the given date
            check_year (int): the year of the given date

        Returns:
            bool: True if scraped date is before given date, False otherwise
        """
    date = get_date(xml)
    if date != "no_date_found" and date != "not_easily_scrapeable" and len(date.split("/")) >= 3:
        day = int(''.join(filter(str.isdigit, date.split("/")[0])))
        month = int(date.split("/")[1])
        year = int(date.split("/")[2])
        if year < check_year:
            return True
        if year == check_year:
            if month < check_month:
                return True
            if month == check_month and day <= check_day:
                return True
    return False


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
        txt = elem.text
        if not txt:
            continue
        # Find rapporteur between "rapporteur:" and "co-rapporteur"
        if find_rapp_between_rapp_and_corapp(txt) is not None:
            return find_rapp_between_rapp_and_corapp(txt)
        # Find rapporteur after "rapporteur: " and before "\n"
        regex_str_2 = r"rapporteur:[\s\w\.]+?\n"
        if re.findall(regex_str_2, txt):
            temp_rapp = get_rapp_after(regex_str_2, txt, 12)
            if temp_rapp:
                return temp_rapp
        # Find rapporteur after "rapporteur:" with found boolean to get rapporteur in new section
        if found:
            # Combine first part of rapporteur like "dr." with next part of rapporteur
            txt = txt.strip().replace("\n", "")
            if txt:
                rapporteur += txt
                rapporteur = clean_rapporteur(rapporteur)
            if len(rapporteur) >= 4:
                return rapporteur
        # Find rapporteur after "rapporteur appointed by the chmp was"
        regex_str_3 = r"rapporteur appointed by the chmp was[\s\S]+"
        if re.findall(regex_str_3, txt):
            temp_rapp = get_rapp_after(regex_str_3, txt, 37)
            if temp_rapp != "rapporteur" and temp_rapp:
                return temp_rapp
        # Find rapporteur after "rapporteur:"
        regex_str_4 = r"rapporteur:[\s\w\.]*"
        if re.search(regex_str_4, txt) and not found:
            rapporteur = get_rapp_after(regex_str_4, txt, 12)
            if len(rapporteur) < 4:
                found = True
            else:
                return rapporteur
    for elem in xml.iter():
        txt = str(elem.text)
        if "rapporteur" in txt and "co-rapporteur" not in txt:
            return "not_easily_scrapeable"

    return "no_rapporteur"


def find_rapp_between_rapp_and_corapp(txt: str) -> str | None:
    """
    A supporting function for finding the rapporteur of the document that
    finds the rapporteur in a certain section in some cases (other cases are processed in the main function)

    Args:
        txt (str): a section of the xml document

    Returns:
        str | None: the attribute ema_rapp - the name of the main rapporteur or None if no rapporteur is found
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
        str: the cleaned string containing only the rapporteur

    """
    rapporteur = rapporteur.strip().replace("\n", "").replace("rapporteur:", "").replace(":", "").replace("/", "")
    # stop when one of certain strings is found
    stop_regex_str = r"[\s\S]*?(medicinal product n|the application was|the applicant submi|the rapporteur appo|chmp " \
                     r"assessment rep|the rapporteur circ|nthe prac rmp advic| chmp peer reviewer)"
    if re.search(stop_regex_str, rapporteur):
        rapporteur = re.search(stop_regex_str, rapporteur)[0]
        rapporteur = rapporteur[:len(rapporteur) - 20].strip()
    # stop when "•" or "" is found
    if re.search("[•|]", rapporteur):
        rapporteur = re.search(r"[\s\S]*?[•|]", rapporteur)[0]
        rapporteur = rapporteur[:len(rapporteur) - 2].strip()
    # take the first part of rapporteur when two spaces are found
    if "  " in rapporteur:
        rapporteur = rapporteur.split("  ")[0].strip()
    if rapporteur == "None":
        return ''
    return rapporteur.strip()


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
        regex_str_1 = r"co-rapporteur:[\s\w\.]+?\n"
        if re.findall(regex_str_1, txt):
            temp_corapp = get_rapp_after(regex_str_1, txt, 15)
            if temp_corapp:
                return temp_corapp

        # Find corapporteur after "co-rapporteur:" with found boolean to get corapp in new section
        if found:
            # Combine first part of corapp like "dr." with next part of corapporteur
            txt = txt.replace("\n", "").strip()
            if txt:
                corapporteur += txt
                corapporteur = clean_rapporteur(corapporteur)
                if corapporteur == "n" or "n/a" in corapporteur:
                    return "no_co-rapporteur"
            if len(corapporteur) >= 4:
                return corapporteur
        # Find co-rapporteur after "co-rapporteur:"
        regex_str_2 = r"co-rapporteur:[\s\w\.]*"
        if re.search(regex_str_2, txt):
            corapporteur = get_rapp_after(regex_str_2, txt, 15)
            if corapporteur == "n" or "n/a" in corapporteur:
                return "no_co-rapporteur"
            if len(corapporteur) < 4:
                found = True
            else:
                return corapporteur
        # Find co-rapporteur after "co-rapporteur"
        if "co-rapporteur" == txt or "corapporteur" == txt:
            found = True
    for elem in xml.iter():
        txt = str(elem.text)
        if "co-rapporteur" in txt or "corraporteur" in txt:
            return "not_easily_scrapeable"
    return "no_co-rapporteur"


def get_reexamination(xml: ET.Element) -> str:
    """
    Gets the attribute ema_reexamination
    Whether the word reexamination/re-examination exists

    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        str: the attribute ema_reexamination - "yes" or "no"
    """
    for elem in xml.iter():
        txt = str(elem.text)
        if "reexamination" in txt:
            return "yes"
        if "re-examination" in txt:
            return "yes"
    return "no"


def get_accelerated_assessment(xml: ET.Element) -> str:
    """
    Gets the attribute eu_accel_assess_g
    Check whether the word "accelerated assessment" is in text and
    "agreed" is close by and "not agreed" is not close by

    Args:
        xml (ET.Element): the contents of the XML file

    Returns:
        str: the attribute eu_accel_assess_g - "yes" or "no", "NA" if ema_procedure_start_initial before 20-05-2004
    """
    if check_date_before(xml, 20, 5, 2004):
        return "NA"
    found = False
    for elem in xml.iter():
        txt = str(elem.text)
        if accelerated_assessment in txt:
            found = True
    if not found:
        return "no"

    text_elements = 20
    # Check whether the word "agreed" is at most 20 text elements before "accelerated assessment"
    found_before = agreed_before_accelerated_assessment(xml, text_elements)
    # Check whether the word "agreed" is at most 20 text elements after "accelerated assessment"
    found_after = agreed_after_accelerated_assessment(xml, text_elements)

    if found_before:
        return found_before
    if found_after:
        return found_after
    return "no"


def agreed_before_accelerated_assessment(xml: ET.Element, text_elements: int) -> str:
    """
    Checks whether the word "agreed" is at most 20 text elements before "accelerated assessment"
    Returns None when "agreed" is not close to "accelerated assessment"

    Args:
        xml (ET.Element): the contents of the XML file
        text_elements (int): the maximum number of text elements to be considered close by

    Returns:
        str: the attribute eu_accel_assess_g - "yes" or "no"
        None: no conclusive evidence was found
    """
    counter = -1
    for elem in xml.iter():
        txt = str(elem.text)
        if counter != -1:
            counter += 1
            if accelerated_assessment in txt and counter <= text_elements:
                return "yes"
        if "agreed" in txt:
            # Return no if accelerated assessment is not agreed
            if "not agreed" in txt:
                return "no"
            # Start counter
            counter = 0


def agreed_after_accelerated_assessment(xml: ET.Element, text_elements: int) -> str:
    """
    Checks whether the word "agreed" is at most 20 text elements after "accelerated assessment"
    Returns None when "agreed" is not close to "accelerated assessment"

    Args:
        xml (ET.Element): the contents of the XML file
        text_elements (int): the maximum number of text elements to be considered close by

    Returns:
        str: the attribute eu_accel_assess_g - "yes" or "no"
        None: no conclusive evidence was found
    """
    counter = -1
    for elem in xml.iter():
        txt = str(elem.text)
        if counter != -1:
            counter += 1
            if "agreed" in txt and counter <= text_elements:
                # Return no if accelerated assessment is not agreed
                if "not agreed" in txt:
                    return "no"
                return "yes"
        if accelerated_assessment in txt:
            # Start counter
            counter = 0
