# EC parser
import re
import os.path as path
import datetime
import fitz
from scraping.utilities.pdf import helper as helper
from scraping.utilities.pdf import pdf_helper as pdf_helper
import scraping.pdf_parser.parsed_info_struct as PIS
import logging
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.attribute_values as attribute_values

log = logging.getLogger("pdf_parser")


def parse_file(filename: str, directory: str, medicine_struct: PIS.ParsedInfoStruct) -> PIS.ParsedInfoStruct:
    """Opens a pdf and adds all respective attributes to the medicine_struct.

    Args:
        filename (str): filename of file to open
        directory (str): directory of file to open
        medicine_struct (PIS.ParsedInfoStruct): struct to add found attributes to

    Returns:
        medicine_struct (PIS.parsed_info_struct): input struct with new variables added
    """
    try:
        pdf = fitz.open(path.join(directory, filename))
        txt = pdf_helper.get_text_str(pdf)
        pdf.close()
    except fitz.fitz.FileDataError:
        log.warning("EC - Could not open PDF: " + filename)
        return medicine_struct
    res = get_data(filename, txt)
    medicine_struct.decisions.append(res)
    #  TODO: remove this, used for debugging. Uncomment for usage
    # if '_0' in filename:
    #     pdf_helper.create_outputfile_dec(filename, res)
    return medicine_struct


# The default values before starting a parse.
def get_default_dict(filename: str) -> dict:
    """returns dictionary with default attribute values, based on type

    Args:
        filename (str): filename of pdf

    Returns:
        dict: contains default value for every attribute
    """
    default = 'Not parsed'

    # keys for human use
    if '_h_' in filename:
        dic = dict.fromkeys([attr.pdf_file,
                             attr.eu_aut_date,
                             attr.eu_brand_name_initial,
                             attr.eu_brand_name_current,
                             attr.active_substance,
                             attr.eu_nas,
                             attr.eu_atmp,
                             attr.eu_od_initial,
                             attr.eu_mah_initial,
                             attr.eu_aut_type_initial,
                             attr.eu_aut_type_current],
                            default)

    # keys for orphan
    elif '_o_' in filename:
        dic = dict.fromkeys([attr.pdf_file,
                             attr.eu_aut_date,
                             attr.eu_brand_name_initial,
                             attr.eu_brand_name_current,
                             attr.eu_od_initial,
                             attr.eu_mah_initial,
                             attr.eu_mah_current,
                             attr.eu_od_comp_date],
                            default)

    # invalid name, only returns name and failure
    else:
        dic = {}
    dic[attr.pdf_file] = filename
    return dic


def get_data(filename: str, txt: str) -> dict:
    """fills in each attribute in a dictionary, based on type

    Args:
        filename (str): filename of pdf
        txt (str): plain txt of pdf

    Returns:
        dict: filled dictionary with parsed results
    """
    filedata = get_default_dict(filename)
    date = dec_get_date(txt)
    filedata[attr.eu_aut_date] = date

    # if date was left blank use default date to not find date dependent attributes.
    if isinstance(date, str):
        date = attribute_values.date_not_found

    if '_h_' in filename:
        filedata[attr.eu_brand_name_initial] = dec_get_bn(txt)
        filedata[attr.active_substance] = dec_get_as(txt)
        filedata[attr.eu_nas] = dec_get_nas(txt, date)
        filedata[attr.eu_atmp] = dec_get_atmp(txt, date)
        if '_0' in filename:
            filedata[attr.eu_od_initial] = dec_get_od(txt, date)
            filedata[attr.eu_mah_initial] = dec_get_mah(txt)
            filedata[attr.eu_aut_type_initial] = dec_get_decision_type(txt, date)
        else:
            filedata[attr.eu_mah_current] = dec_get_mah(txt)
            filedata[attr.eu_aut_type_current] = dec_get_decision_type(txt, date)
        return filedata

    elif '_o_' in filename:
        filedata[attr.eu_brand_name_initial] = dec_get_bn(txt, True)
        filedata[attr.eu_od_comp_date] = dec_get_od_comp_date(txt)
        if '_0' in filename:
            filedata[attr.eu_od_initial] = dec_get_od(txt, date)
            filedata[attr.eu_mah_initial] = dec_get_mah(txt)
        else:
            filedata[attr.eu_mah_current] = dec_get_mah(txt)
        return filedata

    else:
        return filedata


# FUNCTIONS FOR EACH ATTRIBUTE


def dec_get_date(txt: str) -> str | datetime.date:
    """
    Extracts date out of text

    Args:
        txt (str): text containing first page of decision document

    Returns:
        str: string indicating found date or if date is not found
        datetime.date: found date
    """
    txt = txt.lower()
    if len(re.split('of ', txt, 1)) > 1:
        section = re.split('of ', txt, 1)[1]
        section = section[:17]
        if '...' in section or '(date)' in section or 'xxx' in section:
            return attribute_values.eu_aut_date_blank
        if '/' in section:
            section = section.replace('/', '-')

        # check if there are digits on first page
        if bool(re.search(r'\d', section)):
            return helper.get_date(section)
        # there are few cases where date on first page is missing
        # retry on second page before giving up.
        if len(re.split('commission decision', txt.lower())) > 2:
            next_page = re.split('commission decision', txt.lower())[2]
            section = re.split('of ', next_page, 1)[1]
            section = section[:17]
            if '...' in section or '(date)' in section or 'xxx' in section:
                return attribute_values.eu_aut_date_blank
            return helper.get_date(section)

    return helper.get_date('')


def dec_get_bn(txt: str, orphan: bool = False) -> str:
    """
    Extracts brand name out of non-orphan decision text

    Args:
        txt (str): plain decision pdf text
        orphan (bool): to add extra check for orphan structure

    Returns:
        str: found brand name or default value
    """
    # returns a section containing just the brand name (and potentially the active substance)
    section = get_name_section(txt)

    # use advanced regex to find brand name
    brand_name_section = re.search(r'"(\w+[\s\w®/.,"]*)\s?[-–]\s?\w+.*"', section)

    # check if regex found name
    if brand_name_section:
        return brand_name_section.group(0)

    # manually try to find name
    if section != '':
        # takes everything before split operator, to remove active substance.
        if ' -' in section:
            res = section.split(' -')[:-1]
            res = ''.join(res)
            return res.strip()
        if '- ' in section:
            res = section.split('- ')[:-1]
            res = ''.join(res)
            return res.strip()
        if ' –' in section:
            res = section.split(' –')[:-1]
            res = ''.join(res)
            return res.strip()
        # no active substance, so return whole name
        return section

    if orphan:
        # for orphan structure
        if len(txt.split('relating to the designation of medicinal product')) > 1:
            res = txt.split('relating to the designation of medicinal product', 1)[1]
            if 'as an' in res:
                res = res.split('as an', 1)[0]
            if 'as  an' in res:
                res = res.split('as  an', 1)[0]
            res = res.replace('"', '')
            res = res.replace('“', '')
            res = res.replace('”', '')
            return res.strip()

    return attribute_values.not_found


def dec_get_as(txt: str) -> str:
    """extracts active substance out of decision text

    Args:
        txt (str): plain decision pdf text

    Returns:
        str: found substance or default value
    """
    # returns a section containing just the brand name (and potentially the active substance)
    section = get_name_section(txt)
    if section != '' and section.split('- '):
        # takes last element after split operator, to remove brand name.
        if '- ' in section:
            return section.split('- ')[-1].strip()
        if '– ' in section:
            return section.split('– ')[-1].strip()

    return attribute_values.not_found


def dec_get_decision_type(txt: str, date: datetime.date) -> str:
    """
    Extracts decision type out of decision text

    Args:
        txt (str): plain decision pdf text
        date (datetime.date): decision date of pdf

    Returns:
        str: found type or default value
    """
    # check if there can be a CMA.
    if date != attribute_values.date_not_found:
        if date < datetime.date(2006, 1, 1):
            return attribute_values.NA_before

    exceptional = re.search(r"article\s+14\W8", txt.lower())  # exceptional: Article 14(8) or alt. (e.g. Article 14.8)
    # conditional
    if "507/2006" in txt or "conditional marketing authorisation" in txt.lower():
        return attribute_values.aut_type_conditional

    # exceptional
    elif "exceptional circumstances" in txt.lower() or exceptional is not None:
        return attribute_values.aut_type_exceptional
    else:
        return attribute_values.not_found


def dec_get_mah(txt: str) -> str:
    """
    Extracts marketholder out of decision text

    Args:
        txt (str): plain decision pdf text

    Returns:
        str: found marketholder or default value
    """
    mah_regex = r"(( the notification submitted)|( the applicatio\w+ submitted)|( the application\(s\) submitted))"
    if len(re.split(mah_regex, txt)) > 5:
        # get text after one of the following indicators.
        mah_line = re.split(mah_regex, txt)[5]

        # gets part after submitted by line
        mah = mah_line.split(" by ", 1)[1]

        # clean potential stop words.
        # remove part after MAH
        mah = re.split(r'( on )|( under )|( (the marketing authorisation holder))', mah, 1)[0]

        # remove comma if there is a comma at the end.
        if mah[-1] == ',':
            mah = mah[:-1]
        return mah.strip()
    else:
        # read from bottom of final page
        if len(txt.split('This Decision is addressed to ', 1)) > 1:
            # get text after one of the following indicators.
            mah_line = txt.split('This Decision is addressed to ', 1)[1]

            # gets part after submitted by line
            mah = mah_line.split(", ", 1)[0]

            return mah.strip()
        else:
            return attribute_values.not_found


def dec_get_od(txt: str, date: datetime.date) -> str:
    """
    Extracts orphan designation out of decision text

    Args:
        txt (str): plain decision pdf text
        date (datetime.date): decision date of pdf

    Returns:
        str: found orphan designation or default value
    """
    # check if there can be a NAS.
    if date != attribute_values.date_not_found:
        if date < datetime.date(2000, 4, 28):
            return attribute_values.NA_before

    if 'orphan medicinal product' in txt.lower():
        txt = txt.lower().split('orphan medicinal product', 1)[1]
        if 'has adopted this decision' in txt.lower():
            return attribute_values.eu_od_type_adopted
        return attribute_values.eu_od_type_appointed
    return attribute_values.not_found


def dec_get_atmp(txt: str, date: datetime.date) -> str | bool:
    """
    Extracts ATMP out of decision text

    Args:
        txt (str): plain decision pdf text
        date (datetime.date): decision date of pdf

    Returns:
        str: found ATMP or default value
        bool: found result
    """
    # check if there can be a ATMP.
    if date != attribute_values.date_not_found:
        if date < datetime.date(2007, 12, 30):
            return attribute_values.NA_before

    regulation = "Regulation (EC) No 1394/2007"
    fn_idx = txt.find("regulation as last amended by")  # sometimes regulation is mentioned in footnote
    footnote = txt[fn_idx:fn_idx + 70]  # select the sentence if the regulation is mentioned in the footnote
    txt = txt.replace(footnote, "")  # remove the footnote with the regulation from the text
    if regulation.lower() in txt.lower():
        return True
    else:
        return False


def dec_get_nas(txt, date) -> str | bool:
    """
    Extracts NAS out of decision text

    Args:
        txt (str): plain decision pdf text
        date (datetime.date): decision date of pdf

    Returns:
        str: NAS not relevant
        bool: found result
    """
    # check if there can be a NAS.
    if date != attribute_values.date_not_found:
        if date < datetime.date(2012, 1, 1):
            return attribute_values.NA_before

    if "committee for medicinal products for human use" in txt.lower() and "a new active substance" in txt.lower():
        return True
    return False


def dec_get_od_comp_date(txt) -> datetime.date:
    """
    Gives date of orphan comp from decision files.

    Args:
        txt (str): plain decision pdf text

    Returns:
        datetime.date: date found
    """
    keyword1 = 'opinion'
    keyword2 = 'Committee for Orphan Medicinal Products'.lower()

    txt = txt.lower()
    if keyword1 in txt and keyword2 in txt:
        # get section between keywords
        section = txt.split(keyword1, 1)[1]
        section = section.split(keyword2, 1)[0]

        # get section containing the date:
        if 'drawn' in section:
            date_txt = section.split('on', 1)[1]
            date_txt = date_txt.split(',', 1)[0]
            date_txt = date_txt.split('by the', 1)[0]
            return helper.get_date(date_txt.strip())
    return helper.get_date('')


# HELPERS
# helper function for finding brand name and active substance.
def get_name_section(txt: str) -> str:
    """
    Finds section of decision document containing brand name and active substance

    Args:
        txt (str): plain decision pdf text

    Returns:
        str: found section
    """
    # to make sure no commas from pdf format itself, split at date.
    # try since this only works on default english documents.

    if 'of ' in txt:
        txt = txt.split('of ')
        txt = ' '.join(txt[1:])  # to remove part before date

    section = ''
    # try multiple quotation combinations
    if re.search('"([^"]*)"', txt):
        section = re.search('"([^"]*)"', txt)[0]
        section = section.replace('"', '')
    elif re.search('“(.+?)”', txt):
        section = re.search('“(.+?)”', txt)[0]
        section = section.replace('“', '')
        section = section.replace('”', '')
    elif re.search('“(.+?)"', txt):
        section = re.search('“(.+?)"', txt)[0]
        section = section.replace('“', '')
        section = section.replace('"', '')
    elif re.search('"(.+?)\'', txt):
        section = re.search('"(.+?)\'', txt)[0]
        section = section.replace('"', '')
        section = section.replace('\'', '')

    if section is None:
        section = ''
    return section
