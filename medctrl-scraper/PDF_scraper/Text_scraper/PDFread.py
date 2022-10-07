# importing all the required modules
import json
import fitz  # part of pip install PyMuPDF
import os  # to get all file names in folder
# external files for debug
# import ECparse
# import EPARparse
import json

import joblib
from joblib import delayed, Parallel

# external files
import ECparse
import EPARparse


# Asks for the class of the PDF that you want to parse [IE 'ECparse']
def parseTestFile(filetype):
    # filename = 'decisions/h081_dec_140667.pdf'
    filename = 'epars/h1009_epar.pdf'

    pdf = fitz.open(filename)  # open document

    (table, pdf_format) = filetype.getTable(pdf)  # get formatted dictionary

    if filetype.unreadable(table):
        print(str(filename) + ' has no text')

    pdf.close()  # close document

    res = filetype.getAllTest(filename, table, pdf_format)

    # print found attributes and formatted table
    print(res)
    # print(json.dumps(table, indent=3))
    # print(pdf_format)


def parseFolder(filetype, folder_name):
    # PARSE WHOLE Folder

    # debug to indicate progress
    counter = 0
    print(f'Starting... on {folder_name}')

    f = open('results/results_' + folder_name + '.txt', 'w', encoding="utf-8")  # open/clean output file

    pdfCount = len(os.listdir(folder_name))
    all_data = Parallel(n_jobs=4)(delayed(scrape_pdf)(filename, counter, filetype, folder_name, pdfCount) for filename in os.listdir(folder_name))

    for pdfdata in all_data:
        values = list(pdfdata.values())
        output = '@'.join(map(str, values))
        f.writelines(output)
        f.writelines('\n')
    # for filename in os.listdir(folder_name):
    #    scrape_pdf(filename, counter, filetype, folder_name, pdfCount)

    # write date here
    f.close()  # close output file.
    print('Done')


def scrape_pdf(filename, counter, filetype, folder_name, pdfCount):
    # default values
    filedata = filetype.getDefault(filename)

    # debug keep track of progress
    counter += 1
    if (counter % 500) == 0:
        print(f"{counter}/{pdfCount} - {str(round(((counter / pdfCount) * 100), 2))}% ")

    corrupt = False

    # try to open
    try:
        pdf = fitz.open(folder_name + "/" + filename)  # open document
    except:
        corrupt = True

    try:
        (table, pdf_format) = filetype.getTable(pdf)  # get formatted dictionary

        pdf.close()  # close document

        # check if pdf is readable
        if filetype.unreadable(table):
            filedata['status'] = 'Image/No text'
            return filedata

        filedata = filetype.getAll(filedata, table, pdf_format)

        # if filedata['status'] == 'Failure unknown reason':
        filedata['status'] = 'Parsed'

        return filedata

    # could not parse
    except:
        # check if html
        try:
            # open file to check first line
            f2 = open(str(folder_name + "/" + filename), 'r', encoding="utf8")
            firstline = f2.readline()

            if 'html' in firstline.lower():
                filedata['status'] = 'HTML'
                f2.close()
                return filedata
            f2.close()  # close opened file
        except:
            pass

        # check if could not open PDF
        if corrupt:
            filedata['status'] = 'corrupt/could not open'
            return filedata

        # other parse error (uses default 'Failure unknown reason')
        else:
            return filedata

parseTestFile(EPARparse)
