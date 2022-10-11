# importing all the required modules
import fitz  # part of pip install PyMuPDF
import os  # to get all file names in folder
# external classes for debug using parse_test_file
# import ECparse
from parsers import epar_parse

from joblib import delayed, Parallel


# Asks for the class of the PDF that you want to parse [IE 'ECparse']


def parse_test_file(filetype):
    filename = 'epars/h468_epar.pdf'

    pdf = fitz.open(filename)  # open document

    (table, pdf_format) = filetype.get_table(pdf)  # get formatted dictionary

    if filetype.unreadable(table):
        print(str(filename) + ' has no text')

    pdf.close()  # close document

    res = filetype.get_all_test(filename, table, pdf_format)

    # print found attributes and formatted table
    # print(res)
    # print(json.dumps(table, indent=3))


def parse_folder(filetype, folder_name):
    # PARSE WHOLE Folder

    # debug to indicate progress
    counter = 0
    pdf_type = folder_name.split('/')[1]
    print(f'Starting... on {pdf_type}')

    f = open('results/results_' + pdf_type + '.txt', 'w', encoding="utf-8")  # open/clean output file
    pdf_count = len(os.listdir(folder_name))

    # Get all attributes of each pdf file
    all_data = Parallel(n_jobs=4)(
        delayed(scrape_pdf)(filename, counter, filetype, folder_name, pdf_count) for filename in
        os.listdir(folder_name))

    # Combine attributes from PDFs, separate them using @, write lines to results_{filetype}.txt
    # where filetype is the type of PDF scraped
    for pdfdata in all_data:
        values = list(pdfdata.values())
        output = '@'.join(map(str, values))
        f.writelines(output)
        f.writelines('\n')

    f.close()  # close output file.
    print('Done')


def scrape_pdf(filename, counter, filetype, folder_name, pdf_count):
    # default values
    filedata = filetype.get_default(filename)
    corrupt = False

    # try to open
    try:
        pdf = fitz.open(folder_name + "/" + filename)  # open document
        (table, pdf_format) = filetype.get_table(pdf)  # get formatted dictionary

        pdf.close()  # close document
        filedata = filetype.get_all(filedata, table, pdf_format)
        filedata['status'] = 'Parsed'

        return filedata

    # could not parse
    # TODO: Add exception type
    except:
        filedata['status'] = 'corrupt'
        return filedata


#parse_test_file(epar_parse)
