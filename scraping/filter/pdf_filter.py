from joblib import Parallel, delayed
import fitz
import os
import re


# This program scans all PDF files in the given directory.
# Sometimes, the content of a PDF file is not correct.
# This program therefore creates a log file (filter.txt) that saves the actual type of each erroneous PDF file:
# An image, a HTML webpage, or a corrupt PDF in other cases.

# This file can be used by the webscraper to check for corrupt PDF files,
# as this allows the web scraper to try to scrape these files again.

# The other non-PDF files will be scraped during the next automatic web scraper run. (I.E. Next week)

def filter_all_pdfs(directory: str):
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


def filter_folder(folder: str):
    all_data = []
    for filename in os.listdir(folder):
        if '.pdf' in filename:
            data = filter_pdf(filename, folder)
            if data:
                all_data.append(data + '\n')
    return all_data


def check_for_no_text(pdf: fitz.Document):
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


def filter_pdf(filename: str, data_dir: str):
    corrupt = False
    file_path = os.path.join(data_dir, filename)

    # try to open
    try:
        pdf = fitz.open(file_path)  # open document
    except:
        corrupt = True

    # check if file is readable
    try:
        # when readable check if its type matches
        if check_readable(pdf):
            return (file_type_check(filename, file_path, pdf))

        # file not readable
        else:
            pdf.close()
            print('os.remove(file_path)' + file_path)
            return filename + '@corrupt'
    # could not parse
    except:
        # check if html
        try:
            first_line = get_utf8_line(file_path)
            if 'html' in first_line.lower():
                print('os.remove(file_path)' + file_path)
                return filename + '@html'
        except:
            pass

        # check if could not open PDF
        if corrupt:
            print('os.remove(file_path)' + file_path)
            return filename + '@corrupt'
        # other parse error (uses default 'Failure unknown reason')
        else:
            print('os.remove(file_path)' + file_path)
            return filename + '@unknown'


def get_utf8_line(file_path: str) -> str:
    # open file to check first line
    f2 = open(str(file_path), 'r', encoding="utf8")
    first_line = f2.readline()
    f2.close()  # close opened file
    return first_line


def check_readable(pdf: fitz.Document) -> bool:
    # Check if PDF is readable
    no_text = check_for_no_text(pdf)
    # Text is not readable
    if no_text:
        return False
    # Text is readable
    return True


def check_decision(filename, file_path, pdf) -> str:
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
    print('os.remove(file_path)' + file_path)
    return filename + '@wrong_doctype'


# checks if it is an annex file
def check_annex(filename, file_path, pdf) -> str:
    return check_pdf_type(file_path, filename, pdf, 'annex')


# checks if it is a procedural steps file (from EPAR)
def check_procedural(filename, file_path, pdf) -> str:
    return check_pdf_type(file_path, filename, pdf, 'background information')


# checks if it is an EPAR file
def check_epar(filename, file_path, pdf) -> str:
    return check_pdf_type(file_path, filename, pdf, 'assessment report')


# checks if it is a scientific discussion (from EPAR)
def check_scientific(filename, file_path, pdf) -> str:
    return check_pdf_type(file_path, filename, pdf, 'scientific discussion')


def check_pdf_type(file_path, filename, pdf, text) -> str:
    # gets text of first page
    first_page = pdf[0]
    txt = first_page.get_text()
    # checks if the PDF is of the right type
    if text in txt.lower():
        pdf.close()
        return ''
    else:
        pdf.close()
        print('os.remove(file_path)' + file_path)
        return filename + '@wrong_doctype'


def file_type_check(filename, file_path, pdf) -> str:
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


filter_all_pdfs("../../data")
