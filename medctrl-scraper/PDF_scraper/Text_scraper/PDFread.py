# importing all the required modules
import fitz  # part of pip install PyMuPDF
import os  # to get all file names in folder
import json
# external classes for debug using parse_test_file
# import ECparse
# import EPARparse

from joblib import delayed, Parallel

# Asks for the class of the PDF that you want to parse [IE 'ECparse']


def parse_test_file(filetype):
    filename = 'epars/h1578_epar.pdf'

    pdf = fitz.open(filename)  # open document

    (table, pdf_format) = filetype.get_table(pdf)  # get formatted dictionary

    if filetype.unreadable(table):
        print(str(filename) + ' has no text')

    pdf.close()  # close document

    res = filetype.get_all_test(filename, table, pdf_format)

    # print found attributes and formatted table
    print(res)
    print(json.dumps(table, indent=3))


def parse_folder(filetype, folder_name):
    # PARSE WHOLE Folder

    # debug to indicate progress
    counter = 0
    print(f'Starting... on {folder_name}')

    f = open('results/results_' + folder_name + '.txt', 'w', encoding="utf-8")  # open/clean output file

    pdf_count = len(os.listdir(folder_name))
    all_data = Parallel(n_jobs=4)(delayed(scrape_pdf)(filename, counter, filetype, folder_name, pdf_count) for filename in os.listdir(folder_name))

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

    # debug keep track of progress
    counter += 1
    if (counter % 500) == 0:
        print(f"{counter}/{pdf_count} - {str(round(((counter / pdf_count) * 100), 2))}% ")

    corrupt = False

    # try to open
    try:
        pdf = fitz.open(folder_name + "/" + filename)  # open document
    except:
        corrupt = True

    try:
        (table, pdf_format) = filetype.get_table(pdf)  # get formatted dictionary

        pdf.close()  # close document

        # check if pdf is readable
        if filetype.unreadable(table):
            filedata['status'] = 'Image/No text'
            return filedata

        filedata = filetype.get_all(filedata, table, pdf_format)

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

# parse_test_file(EPARparse)
