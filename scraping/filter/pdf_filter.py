from joblib import Parallel, delayed
import fitz
import os
import re

"""
This program scans all PDF files in the given directory.
Sometimes, the content of a PDF file is not correct.
This program therefore creates a log file (filter.txt) that saves the actual type of each erroneous PDF file:
An image, a HTML webpage, or a corrupt PDF in other cases.

This file can be used by the webscraper to check for corrupt PDF files,
as this allows the web scraper to try to scrape these files again.

The other non-PDF files will be scraped during the next automatic web scraper run. (I.E. Next week)
"""


def filter_all_pdfs(directory: str):
    """
    Go through all PDF files in the directory and remove incorrect PDF files
    Saves the names of the filtered PDF files with the error type [corrupt, html, unknown, wrong_doctype]
    
    Args:
        directory (str): folder with all medicine folders to filter

    Returns:
        None

    """
    print(f'Filtering all PDF files...')
    f = open('filter.txt', 'w', encoding="utf-8")  # open/clean output file
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
        (bool): True if pdf is text-free, False otherwise

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
        (str): filename@error_type

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
            os.remove(file_path)
            return filename + '@corrupt'
    # could not parse
    except fitz.fitz.FileDataError:
        # check if html
        first_line = get_utf8_line(file_path)
        if 'html' in first_line.lower():
            os.remove(file_path)
            return filename + '@html'

        # check if PDF was corrupt
        if corrupt:
            os.remove(file_path)
            return filename + '@corrupt'
        # other parse error (uses default 'Failure unknown reason')
        else:
            os.remove(file_path)
            return filename + '@unknown'


def get_utf8_line(file_path: str) -> str:
    """
    Gets the first line of the file
    Args:
        file_path (str): Path of the file to read

    Returns:
        (str): first line of the file

    """
    f2 = open(str(file_path), 'r', encoding="utf8")
    first_line = f2.readline()
    f2.close()  # close opened file
    return first_line


def check_readable(pdf: fitz.Document) -> bool:
    """
    Args:
        pdf (fitz.Document): PDF file to check

    Returns:
        (bool): True if the PDF file is readable
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
        (str): "@wrong_doctype" if the file is not a decision file, otherwise empty string
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
    os.remove(file_path)
    return filename + '@wrong_doctype'


def check_annex(filename: str, file_path: str, pdf: fitz.Document) -> str:
    """
    Checks if it is an annex file
    Args:
        filename (str): filename of supposed annex file to check
        file_path (str): path of annex file to check
        pdf (fitz.Document): pdf of annex file to check

    Returns:
        (str): @wrong_doctype if it is an annex file, empty string otherwise
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
        (str): @wrong_doctype if it is a procedural steps file, empty string otherwise
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
        (str): @wrong_doctype if it is an EPAR file, empty string otherwise
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
        (str): @wrong_doctype if it is a scientific discussion file, empty string otherwise
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
        (str): @wrong_doctype if the file has the wrong type, empty string otherwise
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
    os.remove(file_path)
    return filename + '@wrong_doctype'


def file_type_check(filename: str, file_path: str, pdf: fitz.Document) -> str:
    """
    Checks if any PDF file is of the right type
    Args:
        filename (str): name of the PDF file
        file_path (str): path of the PDF file
        pdf (fitz.Document): PDF document

    Returns:
        (str): @wrong_doctype if the file has the wrong type, empty string otherwise
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

# TODO: fix the path to the data folder
# filter_all_pdfs("../../data")