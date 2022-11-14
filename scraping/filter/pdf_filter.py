from joblib import Parallel, delayed
import fitz
import os
import re
import json


def filter_all_pdfs(directory: str):
    """
    Go through all PDF files in the directory and remove incorrect PDF files
    Saves the names of the filtered PDF files with the error type [corrupt, html, unknown, wrong_doctype]

    Args:
        directory (str): folder with all medicine folders to filter
    """
    print(f'Filtering all PDF files...')
    f = open("filter.txt", 'w', encoding="utf-8")  # open/clean output file
    data_dir = directory
    all_data = Parallel(n_jobs=8)(
        delayed(filter_folder)(os.path.join(data_dir, folder)) for folder in
        os.listdir(data_dir))

    # Write the error of each PDF file to the output file
    # Each line in filter.txt: filename@error_type
    for pdfdata in all_data:
        f.writelines(pdfdata)

    f.close()  # close output file.
    print('Done filtering files')


def filter_folder(folder: str) -> [str]:
    """
    Filters a medicine folder containing PDF files

    Args:
        folder (str): name of the folder to filter

    Returns:
        [str]: PDF names with error types for the folder
    """
    all_data = []
    for filename in os.listdir(folder):
        if '.pdf' in filename:
            data = filter_pdf(filename, folder)
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


def filter_pdf(filename: str, data_dir: str) -> str:
    """
    Checks whether the PDF is readable, or gives an error
    Deletes PDF files with an error and returns the filename as well as the error in a string

    Args:
        filename (str): The name of the PDF file
        data_dir (str): The directory where the PDF is stored

    Returns:
        str: filename@error_type
    """
    corrupt = False
    file_path = os.path.join(data_dir, filename)

    # try to open
    try:
        fitz.open(file_path)  # open document
    except fitz.fitz.FileDataError:
        corrupt = True

    # check if file is readable
    try:
        pdf = fitz.open(file_path)
        # when readable check if its type matches
        if check_readable(pdf):
            return file_type_check(filename, file_path, pdf)

        # file not readable
        else:
            pdf.close()
            safe_remove(file_path)
            return error_line(filename, '@corrupt')
    # could not parse
    except fitz.fitz.FileDataError:
        # check if html
        first_line = get_utf8_line(file_path)
        if 'html' in first_line.lower():
            safe_remove(file_path)
            return error_line(filename, '@html')

        # check if PDF was corrupt
        if corrupt:
            safe_remove(file_path)
            return error_line(filename, '@corrupt')
        # other parse error (uses default 'Failure unknown reason')
        else:
            safe_remove(file_path)
            return error_line(filename, '@unknown')


def error_line(filename: str, error: str) -> str:
    """
    Gives the error line to be written to filter.txt

    Args:
        filename (str): The name of the PDF file
        error (str): The error message of the PDF file

    Returns:
        str: filename@url@error_type OR filename@url@error_type@product_number@brand_name for decision files
    """
    url = get_url(filename)
    if "dec" in filename:
        eu_num = filename[:11].replace("-", "/")
        brand_name = get_brand_name(filename)
        return f"{filename}{error}@{eu_num}@{brand_name}@{url}"
    return f"{filename}{error}@{url}"


def get_brand_name(filename: str) -> str:
    """
    Args:
        filename (str): The name of the PDF file

    Returns:
        str: Brand name of the EC decision file
    """
    eu_num = filename.split('_')[0]
    try:
        with open(f'../data/{eu_num}/{eu_num}_webdata.json') as pdf_json:
            web_attributes = json.load(pdf_json)
            return web_attributes['eu_brand_name_current']
    except FileNotFoundError:
        return "no_webdata_json_found"


def get_url(filename) -> str:
    """
    Retrieve the URL for a given filename
    Args:
        filename (str): The name of the PDF file

    Returns:
        str: url of the filename
    """
    eu_num = filename.split('_')[0]
    try:
        json_path = "web_scraper/"
        # If file is run from webscraper locally:
        if "web_scraper" in os.getcwd():
            json_path = ""
        with open(f'{json_path}JSON/urls.json') as urls_json:
            urls = json.load(urls_json)
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
            except KeyError:
                return "no_url_found"
    except FileNotFoundError:
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
        print("file_not_found")
        return "file_not_found"


def safe_remove(file_path: str):
    """
    Args:
        file_path (str): Path of the file to remove
    """
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print("Can't remove file: file_not_found")


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


def check_decision(filename: str, file_path: str, pdf: fitz.Document) -> str:
    """
    Check if the file is a decision file

    Args:
        filename (str): filename of the supposed decision file
        file_path (str): path to the decision file
        pdf (fitz.Document): PDF file to check

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
    return error_line(filename, '@wrong_doctype')


def check_annex(filename: str, file_path: str, pdf: fitz.Document) -> str:
    """
    Checks if it is an annex file

    Args:
        filename (str): filename of supposed annex file to check
        file_path (str): path of annex file to check
        pdf (fitz.Document): pdf of annex file to check

    Returns:
        str: @wrong_doctype if it is an annex file, empty string otherwise
    """
    return check_pdf_type(file_path, filename, pdf, ['annex', 'name of the medicinal product',
                                                     'summary of product characteristics'])


def check_procedural(filename: str, file_path: str, pdf: fitz.Document) -> str:
    """
    Check if it is a procedural steps file (from EPAR)

    Args:
        filename (str): filename of supposed procedural steps pdf to check
        file_path (str): path to the file to check
        pdf (fitz.Document): pdf to check

    Returns:
        str: @wrong_doctype if it is a procedural steps file, empty string otherwise
    """
    return check_pdf_type(file_path, filename, pdf, ['background information'])


def check_epar(filename: str, file_path: str, pdf: fitz.Document) -> str:
    """
    Check if it is an EPAR file

    Args:
        filename (str): filename of the supposed EPAR file to check
        file_path (str): path to the EPAR file
        pdf (fitz.Document): PDF file to check

    Returns:
        str: @wrong_doctype if it is an EPAR file, empty string otherwise
    """
    return check_pdf_type(file_path, filename, pdf, ['assessment report'])


def check_scientific(filename: str, file_path: str, pdf: fitz.Document) -> str:
    """
    Check if it is a scientific discussion file

    Args:
        filename (str): filename of the supposed scientific discussion file to check
        file_path (str): path to the scientific discussion file
        pdf (fitz.Document): PDF file to check

    Returns:
        str: @wrong_doctype if it is a scientific discussion file, empty string otherwise
    """
    return check_pdf_type(file_path, filename, pdf, ['scientific discussion'])


def check_pdf_type(file_path: str, filename: str, pdf: fitz.Document, texts: [str]) -> str:
    """
    Check if the file is of the correct type - helper function

    Args:
        filename (str): filename of the file to check
        file_path (str): path to the file
        pdf (fitz.Document): PDF file to check
        texts (list): check if any of these strings is in PDF

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
            return ''
    pdf.close()
    safe_remove(file_path)
    return error_line(filename, '@wrong_doctype')


def file_type_check(filename: str, file_path: str, pdf: fitz.Document) -> str:
    """
    Checks if any PDF file is of the right type

    Args:
        filename (str): name of the PDF file
        file_path (str): path of the PDF file
        pdf (fitz.Document): PDF document

    Returns:
        str: @wrong_doctype if the file has the wrong type, empty string otherwise
    """
    if 'dec' in filename:
        return check_decision(filename, file_path, pdf)
    if 'anx' in filename:
        return check_annex(filename, file_path, pdf)
    if 'procedural-steps-taken-authorisation' in filename:
        return check_procedural(filename, file_path, pdf)
    if 'public-assessment-report' in filename:
        return check_epar(filename, file_path, pdf)
    if 'scientific-discussion' in filename:
        return check_scientific(filename, file_path, pdf)
    # TODO: Add OMAR check once available
    else:
        return ''

# filter_all_pdfs("../../data")
