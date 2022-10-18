from joblib import Parallel, delayed
import fitz
import os
import re


# This program scans all PDF files in the given directory.
# Sometimes, the content of a PDF file is not correct.
# This program therefore creates a log file (retry.txt) that saves the actual type of each erroneous PDF file:
# An image, a HTML webpage, or a corrupt PDF in other cases.

# This file can be used by the webscraper to check for corrupt PDF files,
# as this allows the web scraper to try to scrape these files again.

# The other non-PDF files will be scraped during the next automatic web scraper run. (I.E. Next week)

def filter_all_pdfs():
    print(f'Filtering all PDF files...')
    f = open('retry.txt', 'w', encoding="utf-8")  # open/clean output file
    data_dir = 'PDF_scraper/text_scraper/data'
    all_data = Parallel(n_jobs=8)(
        delayed(filter_folder)(os.path.join(data_dir, folder)) for folder in
        os.listdir(data_dir))

    # Write the error of each PDF file to the output file
    # Each line in retry.txt: filename@error_type
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
            if 'dec' in filename:
                return check_decision(filename, file_path, pdf)
        # file not readable
        else:
            pdf.close()
            os.remove(file_path)
            return filename + '@corrupt'
    # could not parse
    except:
        # check if html
        try:
            firstline = get_utf8_line(file_path)
            if 'html' in firstline.lower():
                os.remove(file_path)
                return filename + '@html'
        except:
            pass

        # check if could not open PDF
        if corrupt:
            os.remove(file_path)
            return filename + '@corrupt'
        # other parse error (uses default 'Failure unknown reason')
        else:
            os.remove(file_path)
            return filename + '@unknown'


def get_utf8_line(file_path: str):
    # open file to check first line
    f2 = open(str(file_path), 'r', encoding="utf8")
    firstline = f2.readline()
    f2.close()  # close opened file
    return firstline


def check_readable(pdf: fitz.Document):
    # Check if PDF is readable
    no_text = check_for_no_text(pdf)
    # Text is not readable
    if no_text:
        return False
    # Text is readable
    return True


def check_decision(filename, file_path, pdf):
    try:
        # gets text of second page
        first_page = pdf[0]
        txt = first_page.get_text()
        # checks if it is a decision file
        if bool(re.search(r'commission \w*\s?decision', txt.lower())):
            return ''
        else:
            # try second page
            second_page = pdf[1]
            txt = second_page.get_text()
            if bool(re.search(r'commission \w*\s?decision', txt.lower())):
                return ''
    except:
        pass
    pdf.close()
    os.remove(file_path)
    return filename + '@wrong_doctype'


filter_all_pdfs()
