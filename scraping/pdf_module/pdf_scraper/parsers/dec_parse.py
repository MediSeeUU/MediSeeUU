# EC parser
import re
import os.path as path
import datetime
import fitz
import scraping.pdf_module.pdf_scraper.helper as helper
import scraping.pdf_module.pdf_scraper.pdf_helper as pdf_helper
import scraping.pdf_module.pdf_scraper.parsed_info_struct as PIS


# EC Decision document


# Given a pdf, returns one long string of text
def get_txt_from_pdf(pdf: fitz.Document) -> str:
    """Returns the plain text of a fitz pdf, removing all \\n that are present.

    Args:
    pdf (fitz.Document): The opened pdf document to extract text from

    Returns:
        txt (str): The plain text of a pdf document, without \\n
    """
    pdf_format = pdf_helper.get_text_format(pdf)
    txt = pdf_helper.format_to_string(pdf_format)
    return txt.replace('\n', '')


def parse_file(filename: str, directory: str, medicine_struct: PIS.parsed_info_struct) -> PIS.parsed_info_struct:
    """Opens a pdf and adds all respective attributes to the medicine_struct.

    Args:
        filename (str): filename of file to open
        directory (str): directory of file to open
        medicine_struct (PIS.parsed_info_struct): struct to add found attributes to

    Returns:
        medicine_struct (PIS.parsed_info_struct): input struct with new variables added
    """
    try:
        pdf = fitz.open(path.join(directory, filename))
        txt = get_txt_from_pdf(pdf)
        pdf.close()
    except fitz.fitz.FileDataError:
        print("EC - Could not open PDF: " + filename)
        return medicine_struct
    res = get_all(filename, txt)
    medicine_struct.decisions.append(res)
    pdf_helper.create_outputfile_dec(filename, res)
    return medicine_struct


# Given a dictionary, fills in all attributes for EC decisions
def get_all(filename: str, txt: str) -> dict:
    """based on filename finds all fitting attributes

    Args:
        filename (str): filename of opened pdf file
        txt (str): plain text of opened pdf file

    Returns:
        dict: filled filedata
    """
    # human use file attributes
    if '_h_' in filename:
        filedata = get_data_human_use(filename, txt)
        return filedata

    # orphan file attributes
    if '_o_' in filename:
        filedata = get_data_orphan(filename, txt)
        return filedata

    # if other file return data with everything 'Not parsed'
    return get_default_human_use(filename)


# The default values before starting a parse.
def get_default_human_use(filename: str) -> dict:
    """returns dictionary with default attribute values for human use

    Args:
        filename (str): filename of pdf

    Returns:
        dict: contains default value for every attribute
    """
    default = 'Not parsed'
    return {'filename': filename,
            'eu_aut_date': default,
            'eu_brand_name_initial': default,
            'active_substance': default,
            'eu_nas': default,
            'eu_atmp': default,
            'eu_od_initial': default,
            'eu_mah_initial': default,
            'eu_aut_type_initial': default,
            'status': 'Failure unknown reason'
            }


# The default values before starting a parse.
def get_default_orphan(filename: str) -> dict:
    """returns dictionary with default attribute values for orphan

    Args:
        filename (str): filename of pdf

    Returns:
        dict: contains default value for every attribute
    """
    default = 'Not parsed'
    return {'filename': filename,
            'eu_aut_date': default,
            'eu_brand_name_initial': default,
            'eu_od_initial': default,
            'eu_mah_initial': default,
            'eu_od_comp_date': default,
            'status': 'Failure unknown reason'
            }


def get_data_human_use(filename: str, txt: str) -> dict:
    """fills in each attribute in a dictionary for human use

    Args:
        filename (str): filename of pdf
        txt (str): plain txt of pdf

    Returns:
        dict: _description_
    """
    filedata = get_default_human_use(filename)
    date = dec_get_date(txt)
    filedata['eu_aut_date'] = date

    # if date was left blank return don't find date dependant attributes.
    if isinstance(date, str):
        date = dec_get_date('')

    filedata['eu_brand_name_initial'] = dec_get_bn(txt)
    filedata['active_substance'] = dec_get_as(txt)
    filedata['eu_nas'] = dec_get_nas(txt, date)
    filedata['eu_atmp'] = dec_get_atmp(txt, date)
    filedata['eu_od_initial'] = dec_get_od(txt, date)
    filedata['eu_mah_initial'] = dec_get_mah(txt)
    filedata['eu_aut_type_initial'] = dec_get_decision_type(txt, date)
    filedata['status'] = 'Parsed'
    return filedata


def get_data_orphan(filename: str, txt: str) -> dict:
    """fills in each attribute in a dictionary for orphan
    Args:
        filename (str): filename of pdf
        txt (str): plain txt of pdf

    Returns:
        dict: _description_
    """
    filedata = get_default_orphan(filename)
    date = dec_get_date(txt)
    filedata['eu_aut_date'] = date

    # if date was left blank return don't find date dependant attributes.
    if isinstance(date, str):
        date = dec_get_date('')
    filedata['eu_brand_name_initial'] = dec_get_bn(txt)
    filedata['eu_od_initial'] = dec_get_od(txt, date)
    filedata['eu_mah_initial'] = dec_get_mah(txt)
    filedata['eu_od_comp_date'] = dec_get_od_comp_date()
    filedata['status'] = 'Parsed'
    return filedata


# FUNCTIONS FOR EACH ATTRIBUTE


def dec_get_date(txt: str) -> str | datetime.datetime:
    """extracts date out of text

    Args:
        txt (str): text containing first page of decision document

    Returns:
        str: string indicating found date or if date is not found
        datetime.datetime: found date
    """
    txt = txt.lower()
    if re.split('of ', txt, 1):
        section = re.split('of ', txt, 1)[1]
        section = section[:17]
        if '...' in section or '(date)' in section or 'xxx' in section:
            return 'Date is blank'
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
                return 'Date is blank'
            return helper.get_date(section)

    return helper.get_date('')


def dec_get_bn(txt: str) -> str:
    """extracts brand name out of decision text

    Args:
        txt (str): plain decision pdf text

    Returns:
        str: found brand name or default value
    """
    # returns a section containing just the brand name (and potentially the active substance)
    section = get_name_section(txt)

    # use advanced regex to find brand name
    brand_name_section = re.search(r'"(\w+[\s\w®/.,"]*)\s?[-–]\s?\w+.*"', section)

    if brand_name_section:
        return brand_name_section.group(0)

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

    # for orphan structure
    if len(txt.split('relating to the designation of medicinal product')) > 1:
        res = txt.split('relating to the designation of medicinal product')[1]
        if res.split('as an orphan medicinal'):
            res = res.split('as an orphan medicinal')[0]
            res = res.replace('"', '')
            res = res.replace('“', '')
            res = res.replace('”', '')
            res.strip()
            return res

    return 'Brand name Not Found'


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

    return 'Active Substance Not Found'


def dec_get_decision_type(txt: str, date: datetime.datetime) -> str:
    """extracts decision type out of decision text

    Args:
        txt (str): plain decision pdf text
        date (datetime.datetime): decision date of pdf

    Returns:
        str: found type or default value
    """
    # check if there can be a CMA.
    if date < datetime.datetime(2006, 1, 1):
        return "CMA not available before 2006"

    exceptional = re.search(r"article\s+14\W8", txt.lower())  # exceptional: Article 14(8) or alt. (e.g. Article 14.8)
    # conditional
    if "507/2006" in txt or "conditional marketing authorisation" in txt.lower():
        return "conditional"

    # exceptional
    elif "exceptional circumstances" in txt.lower() or exceptional is not None:
        return "exceptional"
    else:
        return "CMA Not Found"


def dec_get_mah(txt: str) -> str:
    """extracts marketholder out of decision text

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
            return 'MAH Not Found'


def dec_get_od(txt: str, date: datetime.datetime) -> str:
    """extracts orphan designation out of decision text

    Args:
        txt (str): plain decision pdf text
        date (datetime.datetime): decision date of pdf

    Returns:
        str: found orphan designation or default value
    """
    # check if there can be a NAS.
    if date < datetime.datetime(2000, 4, 28):
        return "NA before 2000"

    if 'orphan medicinal product' in txt.lower():
        txt = txt.lower().split('orphan medicinal product', 1)[1]
        if 'has adopted this decision' in txt.lower():
            return 'adopted'
        return 'appointed'
    return 'OD Not Found'


def dec_get_atmp(txt: str, date: datetime.datetime) -> str | bool:
    """extracts atmp out of decision text

    Args:
        txt (str): plain decision pdf text
        date (datetime.datetime): decision date of pdf

    Returns:
        str: found atmp or default value
    """
    # check if there can be a ATMP.
    if date < datetime.datetime(2007, 12, 30):
        return "NA before 2012"

    regulation = "Regulation (EC) No 1394/2007"
    fn_idx = txt.find("regulation as last amended by")  # sometimes regulation is mentioned in footnote
    footnote = txt[fn_idx:fn_idx + 70]  # select the sentence if the regulation is mentioned in the footnote
    txt = txt.replace(footnote, "")  # remove the footnote with the regulation from the text
    if regulation.lower() in txt.lower():
        return True
    else:
        return False


def dec_get_nas(txt, date) -> str | bool:
    """extracts NAS out of decision text

    Args:
        txt (str): plain decision pdf text
        date (datetime.datetime): decision date of pdf

    Returns:
        str: NAS not relevant
        bool: found result
    """
    # check if there can be a NAS.
    if date < datetime.datetime(2012, 1, 1):
        return "NAS before 2012"

    if "committee for medicinal products for human use" in txt.lower() and "a new active substance" in txt.lower():
        return True
    return False


def dec_get_od_comp_date() -> datetime.datetime:
    """gives default date value

    Returns:
        str: default date of get_date
    """
    return helper.get_date('')


# HELPERS
# helper function for finding brand name and active substance.
def get_name_section(txt: str) -> str:
    """finds section of decision document containing brand name and active substance

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
