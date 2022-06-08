# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from loguru import logger
import re
import requests
import os
import glob

eurls = {
    "prac_list": "https://www.ema.europa.eu/en/committees/prac/prac-agendas-minutes-highlights",
    "prac_minutes": "https://www.ema.europa.eu/documents/minutes/minutes-prac-meeting-",
    "prac_draft_agenda": "https://www.ema.europa.eu/documents/agenda/agenda-prac-draft-agenda-meeting-",
    "assessment_report": "https://www.ema.europa.eu/documents/assessment-report/",
    "validation_report": "https://www.ema.europa.eu/documents/variation-report/",
    "procedures_after_authorization": "https://www.ema.europa.eu/documents/procedural-steps-after/",
    "scientific_conclusions": "https://www.ema.europa.eu/documents/scientific-conclusion/",
    "ec_base": "https://ec.europa.eu/health/documents/community-register/",
    "ec_active": [
        "active",
        "http://ec.europa.eu/health/documents/community-register/html/reg_hum_act.htm",
        "https://ec.europa.eu/health/documents/community-register/html/h"
    ],
    "ec_withdrawn": [
        "withdrawn",
        "http://ec.europa.eu/health/documents/community-register/html/reg_hum_nact.htm",
        "https://ec.europa.eu/health/documents/community-register/html/h"
    ],
    "ec_refused": [
        "refused",
        "http://ec.europa.eu/health/documents/community-register/html/reg_hum_refus.htm",
        "https://ec.europa.eu/health/documents/community-register/html/ho"
    ],
}

ec_colnames = [
    "emanumber",
    "emanumber_abb",
    "emanumber_confidence",
    "emanumber_doublecheck",
    "eunumber",
    "eunumber_abb",
    "name",
    "company",
    "group",
    "url",
    "emalink",
    "activesubstance",
    "authorisationprocedure",
    "authorisationdate",
    "auth_url",
    'smpc_url',
    "recentprocedure",
    "atccode",
    "atcname",
    'decision_type (EC)',
]

roman_numbers = {
    "I": "1",
    "II": "2",
    "III": "3",
    "IV": "4",
    "V": "5",
    "VI": "6",
    "VII": "7",
    "VIII": "8",
    "IX": "9",
    "X": "10",
    "XI": "11",
    "XII": "12"
}

months = {
    "January": "1",
    "February": "2",
    "March": "3",
    "April": "4",
    "May": "5",
    "June": "6",
    "July": "7",
    "August": "8",
    "September": "9",
    "October": "10",
    "November": "11",
    "December": "12"
}

lbases = [
        "article 4.8",
        "article 4(8)"
        "article 4.8(1)",
        "article 4.8(2)",
        "article 4.8(3)",
        "article 8.3",
        "article 8(3)",
        "article 10.1",
        "article 10(1)",
        "article 10.2",
        "article 10(2)",
        "article 10.3",
        "article 10(3)",
        "article 10.4",
        "article 10(4)",
        "article 10a",
        "article 10(a)",
        "article 10b",
        "article 10(b)",
        "article 10c",
        "article 10(c)"
    ]


def read_filenames(directory_path: str):
    """ Give the path to a directory and it will give you the filenames and paths of all PDFs in that directory

    Parameters
    ----------
    directory_path: Absolute or relative path to directory containing PDFs

    Returns
    -------
    names: list of the names of the PDF files
    files: list of paths to the PDFs
    """
    logger.info(f"reading filenames in directory '{directory_path}'..")
    files = glob.glob(f"{directory_path}/*.pdf")
    names = [os.path.basename(x) for x in files]  # get filenames from filepaths
    logger.info("done")
    return names, files


def convert_roman_numbers(date: str):
    """ Converts the roman numbers (up to XII) to normal numbers

    Parameters
    ----------
    date: string pattern of the date

    Returns
    -------
    date: string pattern of the corrected date
    """

    # sort roman_numbers on length (big to small)
    # otherwise I is found in VII before VII is found in VII
    for k in sorted(roman_numbers, key=len, reverse=True):
        if k in date:
            date = date.replace(k, roman_numbers[k])
            break

    return date


def convert_months(date: str):
    for k in months.keys():
        if k in date:
            date = date.replace(f" {k} ", f"/{months[k]}/")
            break

    return date


def convert_to_yyyy(yy: str):
    twenty = try_block(re.search(r'([0-5]\d)', yy))
    if twenty is None:
        yyyy = "19" + yy
    else:
        yyyy = "20" + yy

    return yyyy


def try_block(research, idx: int = 0):
    """ Try-Except block to use for Regex searching

    Parameters
    ----------
    research: The result from a re.search() function (or other re functions)

    Returns
    -------
    match: The matched pattern
    """
    try:  # if a match is found the length of research is two: ["sentence", "match"]
        match = research[idx]
    except IndexError:  # if no match is found in the regex the length of research is one: ["sentence"]
        match = None
    except TypeError:  # if research[1] is None
        match = None
    except BaseException as e:  # catches all other exceptions and errors
        logger.info(f"Unexpected {e=}, {type(e)=}. Contact developers!")
        raise

    return match


def reset_eof(file_path: str, fixed_path: str):
    """ Adds EOF marker to the corrupt PDF file and saves as _fixed PDF file.

    Parameters
    ----------
    file_path: the path to the PDF file
    fixed_path: the path to the new & fixed PDF file

    Returns
    -------
    """

    EOF_MARKER = b'%%EOF'
    with open(file_path, 'rb') as f:
        contents = f.read()

        # check if EOF is somewhere else in the file
        if EOF_MARKER in contents:
            # we can remove the early %%EOF and put it at the end of the file
            contents = contents.replace(EOF_MARKER, b'')
            contents = contents + EOF_MARKER
        else:
            # Some files really don't have an EOF marker
            # In this case it helped to manually review the end of the file
            print(contents[-8:])  # see last characters at the end of the file
            # printed b'\n%%EO%E'
            contents = contents[:-6] + EOF_MARKER
        print(contents)
    with open(fixed_path, 'wb') as f:
        f.write(contents)


def isnan(value):
    try:
        import math
        return math.isnan(float(value))
    except (TypeError, ValueError):
        return False


def download_files(url: str, name: str, output_dir: str):
    """ Downloads and stores files

    Parameters
    ----------
    url: URL to the download file
    name: Name to give to the saved file (including file type, e.g. '.pdf')
    output_dir: Location where to save the file
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.debug(e)
        return
    with open(f'{output_dir}/{name}', 'wb') as f:
        f.write(r.content)
        f.close()
