from joblib import Parallel, delayed
import fitz
import os
import re


# This program scans all PDF files in the given directory.
# Sometimes, the content of a PDF file is not correct.
# This program therefore creates a log file (retry.txt) that saves the actual type of each PDF file:
# A PDF file, an image, a HTML webpage, or a corrupt PDF in other cases.

# This file can be used by the webscraper to check for corrupt PDF files,
# as this allows the web scraper to try to scrape these files again.

# The other non-PDF files will be scraped during the next automatic web scraper run. (I.E. Next week)

def filter_all_pdfs(directory: str):
    print(f'Filtering all PDF files...')
    f = open('retry.txt', 'w', encoding="utf-8")  # open/clean output file
    data_dir = directory

    all_data = Parallel(n_jobs=8)(
        delayed(filter_pdf)(filename, data_dir) for filename in
        os.listdir(data_dir))

    # Write the file type of each PDF file to the output file
    for pdfdata in all_data:
        values = list(pdfdata)
        f.writelines(values)
        f.writelines('\n')

    f.close()  # close output file.
    print('Done filtering files')


def check_for_no_text(pdf):
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


def filter_pdf(filename, data_dir):
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
                return check_decision(filename, pdf)
        # file not readable
        else: 
            pdf.close()
            return filename + '@no_text'
    # could not parse
    except:
        # check if html
        try:
            firstline = get_utf8_line(file_path)
            if 'html' in firstline.lower():
                return filename + '@html'
        except:
            pass

        # check if could not open PDF
        if corrupt:
            return filename + '@corrupt'
        # other parse error (uses default 'Failure unknown reason')
        else:
            return filename + '@unknown'


def get_utf8_line(file_path):
    # open file to check first line
    f2 = open(str(file_path), 'r', encoding="utf8")
    firstline = f2.readline()
    f2.close()  # close opened file
    return firstline


def check_readable(pdf):
    # Check if PDF is readable
    no_text = check_for_no_text(pdf)
    # Text is not readable
    if no_text:
        return False
    # Text is readable
    return True


def check_decision(filename, pdf):
    try:
        # gets text of second page
        first_page = pdf[0]
        txt = first_page.get_text()
        # checks if it is a decision file
        if bool(re.search(r'commission \w{0,}\s{0,1}decision', txt.lower())):
            return filename + '@valid'
        else:
            # try second page
            second_page = pdf[1]
            txt = second_page.get_text()
            if bool(re.search(r'commission \w{0,}\s{0,1}decision', txt.lower())):
                pdf.close()
                return filename + '@valid'
    except:
        pass
    return filename + '@wrong_doctype'

# filter_all_pdfs("text_scraper/data/dec_initial")
