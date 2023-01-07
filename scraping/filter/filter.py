import json
import logging
import multiprocessing
import os
import re

import fitz
from joblib import Parallel, delayed
from tqdm import tqdm

from scraping.utilities.definitions import attribute_values as values, attributes
from scraping.utilities.io import safe_io
from scraping.utilities.log import log_tools

wrong_doctype_str = "@wrong_doctype"
cpu_count: int = multiprocessing.cpu_count()
log = logging.getLogger("filter")


def filter_all_pdfs(directory: str, folders: list[str] = None):
    """
    Go through all PDF files in the directory and remove incorrect PDF files
    Saves the names of the filtered PDF files with the error type [corrupt, html, unknown, wrong_doctype]

    Args:
        directory (str): folder with all medicine folders to filter
        folders (list[str]): list of eu numbers to filter, filter all when empty
    """
    log.info("Filtering PDF files...")
    data_path = directory.split("active_withdrawn")[0]
    log_path = log_tools.get_log_path("filter.txt", data_path)
    f = open(log_path, 'w', encoding="utf-8")  # open/clean output file
    if folders:
        med_folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))
                       and folder in ''.join(folders)]
    else:
        med_folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    all_data = Parallel(n_jobs=cpu_count)(
        delayed(filter_folder)(os.path.join(directory, folder), directory) for folder in
        tqdm(med_folders))

    # Write the error of each PDF file to the output file
    # Each line in filter.txt: filename@error_type
    for pdfdata in all_data:
        f.writelines(pdfdata)

    f.close()  # close output file.
    log.info('Done filtering files')


def filter_folder(folder: str, directory: str) -> [str]:
    """
    Filters a medicine folder containing PDF files

    Args:
        folder (str): name of the folder to filter
        directory (str): folder with all medicine folders to filter

    Returns:
        [str]: PDF names with error types for the folder
    """
    all_data = []
    if not os.path.isdir(folder):
        return all_data
    for filename in os.listdir(folder):
        if '.pdf' in filename:
            data = filter_pdf(filename, folder, directory)
            if data:
                all_data.append(data + '\n')
    return all_data


def check_for_no_text(pdf: fitz.Document) -> bool:
    """
    Args:
        pdf (fitz.Document): PDF file to check whether it is text-free

    Returns:
        bool: True if pdf is text-free, False otherwise
    """
    for page in pdf:
        dict_ = page.get_text("dict")
        blocks = dict_["blocks"]
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                for span in spans:
                    data = span['spans']
                    for lines in data:
                        text = lines['text']
                        if len(text) > 0:
                            return False
    return True


def filter_pdf(filename: str, data_dir: str, directory: str) -> str:
    """
    Checks whether the PDF is readable, or gives an error
    Deletes PDF files with an error and returns the filename as well as the error in a string

    Args:
        filename (str): The name of the PDF file
        data_dir (str): The directory where the PDF is stored
        directory (str): folder with all medicine folders to filter

    Returns:
        str: filename@error_type
    """
    file_path = os.path.join(data_dir, filename)

    # check if file is readable
    try:
        pdf = fitz.open(file_path)
        # when readable check if its type matches

        if check_readable(pdf):
            return file_type_check(filename, file_path, pdf, directory)

        # file not readable
        else:
            pdf.close()
            safe_remove(file_path)
            return error_line(filename, '@corrupt', directory)

    # could not parse
    except fitz.fitz.FileDataError:
        # check if html
        first_line = get_utf8_line(file_path)
        if 'html' in first_line.lower():
            safe_remove(file_path)
            return error_line(filename, '@html', directory)

        # PDF is not HTML, but can't be opened
        safe_remove(file_path)
        return error_line(filename, '@corrupt', directory)


def error_line(filename: str, error: str, directory: str) -> str:
    """
    Gives the error line to be written to filter.txt

    Args:
        filename (str): The name of the PDF file
        error (str): The error message of the PDF file
        directory (str): folder with all medicine folders to filter

    Returns:
        str: filename@url@error_type OR filename@url@error_type@product_number@brand_name for decision files
    """
    url = get_url(filename, directory)
    if "dec" in filename:
        eu_num = filename[:11].replace("-", "/")
        brand_name = get_brand_name(filename, directory)
        return f"{filename}{error}@{eu_num}@{brand_name}@{url}"
    return f"{filename}{error}@{url}"


def get_brand_name(filename: str, directory: str) -> str:
    """
    Args:
        filename (str): The name of the PDF file
        directory (str): folder with all medicine folders to filter

    Returns:
        str: Brand name of the EC decision file
    """
    eu_num = filename.split('_')[0]
    try:
        with open(f'{directory}/{eu_num}/{eu_num}_webdata.json') as pdf_json:
            web_attributes = json.load(pdf_json)
            return web_attributes['eu_brand_name_current']
    except FileNotFoundError as e:
        log.warning(f"Filter: Webdata JSON not found for {eu_num}. Error: {e}")
        return values.webdata_not_found


def get_url(filename: str, directory: str) -> str:
    """
    Retrieve the URL for a given filename
    Args:
        filename (str): The name of the PDF file
        directory (str): folder with all medicine folders to filter

    Returns:
        str: url of the filename
    """
    eu_num = filename.split('_')[0]
    # Get upper directory of data directory
    scraping_dir = directory.split('data')[0]
    # When testing, remove test_ from path
    scraping_dir = scraping_dir.split('test_')[0]
    # Add scraping to path
    scraping_dir = scraping_dir + "scraping"
    try:
        # JSON is in scraping directory/web_scraper/JSON
        json_path = f"{scraping_dir}/web_scraper/JSON/"
        # If file is run from webscraper locally:
        with open(f'{json_path}urls.json') as urls_json:
            try:
                urls = json.load(urls_json)
            except json.JSONDecodeError as e:
                log.warning(f"Filter: Cannot open urls.json. Error: {e}")
                return "cannot_open_urls_json"
            try:
                if 'dec' in filename:
                    num = filename.split('_')[-1]
                    num = int(num[:len(num) - 4])
                    return urls[eu_num]['aut_url'][num]
                if 'anx' in filename:
                    num = filename.split('_')[-1]
                    num = int(num[:len(num) - 4])
                    return urls[eu_num]['smpc_url'][num]
                if 'procedural-steps-taken-authorisation' in filename:
                    return urls[eu_num]['epar_url']
                if 'public-assessment-report' in filename:
                    return urls[eu_num]['epar_url']
                if 'scientific-discussion' in filename:
                    return urls[eu_num]['epar_url']
                if 'other' in filename:
                    num = filename.split('_')[-1]
                    num = int(num[:len(num) - 4])
                    return urls[eu_num][attributes.other_ema_urls][num][0]
            except KeyError as e:
                log.warning(f"Filter: KeyError in urls.json. Error: {e}")
                return values.url_not_found
    except FileNotFoundError as e:
        log.warning(f"Filter: Cannot find urls.json. Error: {e}")
        return "urls_json_not_found"
    return "file_type_not_recognized"


def get_utf8_line(file_path: str) -> str:
    """
    Gets the first line of the file

    Args:
        file_path (str): Path of the file to read

    Returns:
        str: first line of the file
    """
    try:
        f2 = open(str(file_path), 'r', encoding="utf8")
        first_line = f2.readline()
        f2.close()  # close opened file
        return first_line
    except FileNotFoundError:
        log.error(f"Can't open file: file_not_found @ {file_path}")
        return "file_not_found"
    except UnicodeDecodeError:
        log.error(f"UnicodeDecodeError while decoding the first line in {file_path}")
        return "decode_error"


def safe_remove(file_path: str):
    """
    Args:
        file_path (str): Path of the file to remove
    """
    try:
        log.info(f"Filter: Removed {file_path}")
        safe_io.delete_file(file_path)
    except FileNotFoundError:
        log.error(f"Can't remove file: file_not_found @ {file_path}")


def check_readable(pdf: fitz.Document) -> bool:
    """
    Args:
        pdf (fitz.Document): PDF file to check

    Returns:
        bool: True if the PDF file is readable
    """
    # Check if PDF is readable
    no_text = check_for_no_text(pdf)
    # Text is not readable
    if no_text:
        return False
    # Text is readable
    return True


def check_decision(filename: str, file_path: str, pdf: fitz.Document, directory: str) -> str:
    """
    Check if the file is a decision file

    Args:
        filename (str): filename of the supposed decision file
        file_path (str): path to the decision file
        pdf (fitz.Document): PDF file to check
        directory (str): folder with all medicine folders to filter

    Returns:
        str: "@wrong_doctype" if the file is not a decision file, otherwise empty string
    """
    # gets text of first page
    first_page = pdf[0]
    txt = first_page.get_text()
    # checks if it is a decision file
    if re.search(r'commission \w*\s?decision', txt.lower()):
        pdf.close()
        return ''
    else:
        # try second page
        second_page = pdf[1]
        txt = second_page.get_text()
        if re.search(r'commission \w*\s?decision', txt.lower()):
            pdf.close()
            return ''
    pdf.close()
    safe_remove(file_path)
    return error_line(filename, wrong_doctype_str, directory)


def check_annex(filename: str, file_path: str, pdf: fitz.Document, directory: str) -> str:
    """
    Checks if it is an annex file

    Args:
        filename (str): filename of supposed annex file to check
        file_path (str): path of annex file to check
        pdf (fitz.Document): pdf of annex file to check
        directory (str): folder with all medicine folders to filter

    Returns:
        str: @wrong_doctype if it is an annex file, empty string otherwise
    """
    # gets text of first page
    first_page = pdf[0]
    txt = first_page.get_text()

    # checks if first page of initial annex file contains "implemented by the member states", if so, filters it
    if "implemented by the member states" in txt.lower() and "anx_0" in filename:
        pdf.close()
        safe_remove(file_path)
        return error_line(filename, wrong_doctype_str, directory)

    # checks if the first page is characteristic on an annex file
    return check_pdf_type(file_path, filename, pdf, ['annex', 'name of the medicinal product',
                                                     'summary of product characteristics'], directory)


def check_procedural(filename: str, file_path: str, pdf: fitz.Document, directory: str) -> str:
    """
    Check if it is a procedural steps file (from EPAR)

    Args:
        filename (str): filename of supposed procedural steps pdf to check
        file_path (str): path to the file to check
        pdf (fitz.Document): pdf to check
        directory (str): folder with all medicine folders to filter

    Returns:
        str: @wrong_doctype if it is a procedural steps file, empty string otherwise
    """
    return check_pdf_type(file_path, filename, pdf, ['background information'], directory)


def check_epar(filename: str, file_path: str, pdf: fitz.Document, directory: str) -> str:
    """
    Check if it is an EPAR file

    Args:
        filename (str): filename of the supposed EPAR file to check
        file_path (str): path to the EPAR file
        pdf (fitz.Document): PDF file to check
        directory (str): folder with all medicine folders to filter

    Returns:
        str: @wrong_doctype if it is an EPAR file, empty string otherwise
    """
    return check_pdf_type(file_path, filename, pdf, ['assessment report'], directory)


def check_scientific(filename: str, file_path: str, pdf: fitz.Document, directory: str) -> str:
    """
    Check if it is a scientific discussion file

    Args:
        filename (str): filename of the supposed scientific discussion file to check
        file_path (str): path to the scientific discussion file
        pdf (fitz.Document): PDF file to check
        directory (str): folder with all medicine folders to filter

    Returns:
        str: @wrong_doctype if it is a scientific discussion file, empty string otherwise
    """
    return check_pdf_type(file_path, filename, pdf, ['scientific discussion'], directory)


def check_pdf_type(file_path: str, filename: str, pdf: fitz.Document, texts: [str], directory: str) -> str:
    """
    Check if the file is of the correct type - helper function

    Args:
        filename (str): filename of the file to check
        file_path (str): path to the file
        pdf (fitz.Document): PDF file to check
        texts (list): check if any of these strings is in PDF
        directory (str): folder with all medicine folders to filter

    Returns:
        str: @wrong_doctype if the file has the wrong type, empty string otherwise
    """
    # gets text of first page
    first_page = pdf[0]
    txt = first_page.get_text()

    # checks if the PDF is of the right type
    for text in texts:
        if text in txt.lower():
            pdf.close()
            return ""
    pdf.close()
    safe_remove(file_path)
    return error_line(filename, wrong_doctype_str, directory)


def file_type_check(filename: str, file_path: str, pdf: fitz.Document, directory: str) -> str:
    """
    Checks if any PDF file is of the right type

    Args:
        filename (str): name of the PDF file
        file_path (str): path of the PDF file
        pdf (fitz.Document): PDF document
        directory (str): folder with all medicine folders to filter

    Returns:
        str: @wrong_doctype if the file has the wrong type, empty string otherwise
    """
    if 'dec' in filename:
        return check_decision(filename, file_path, pdf, directory)
    if 'anx' in filename:
        return check_annex(filename, file_path, pdf, directory)
    if 'procedural-steps-taken-authorisation' in filename:
        return check_procedural(filename, file_path, pdf, directory)
    if 'public-assessment-report' in filename:
        return check_epar(filename, file_path, pdf, directory)
    if 'scientific-discussion' in filename:
        return check_scientific(filename, file_path, pdf, directory)
    # TODO: Add OMAR check once available
    else:
        return ''


# filter_all_pdfs("../../data/active_withdrawn")
