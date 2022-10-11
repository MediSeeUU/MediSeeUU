from joblib import Parallel, delayed
import fitz
import os


# This program scans all PDF files in the given directory.
# Sometimes, the content of a PDF file is not correct.
# This program therefore creates a log file (retry.txt) that saves the actual type of each PDF file:
# A PDF file, an image, a HTML webpage, or a corrupt PDF in other cases.

# This file can be used by the webscraper to check for corrupt PDF files,
# as this allows the web scraper to try to scrape these files again.

# The other non-PDF files will be scraped during the next automatic web scraper run. (I.E. Next week)

def filter_all_pdfs():
    print(f'Filtering all PDF files...')
    f = open('retry.txt', 'w', encoding="utf-8")  # open/clean output file
    data_dir = 'PDF_scraper/text_scraper/data'

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

    try:
        return check_readable(filename, pdf)
    # could not parse
    except:
        # Check if html
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


def check_readable(filename, pdf):
    # Check if PDF is readable
    no_text = check_for_no_text(pdf)
    pdf.close()  # close document
    # Text is not readable
    if no_text:
        return filename + '@no_text'
    # Text is readable
    return filename + '@parsed'

# filter_all_pdfs()
