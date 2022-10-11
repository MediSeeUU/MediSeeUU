# importing all the required modules
import fitz  # part of pip install PyMuPDF
import os  # to get all file names in folder
# external classes for debug using parse_test_file
# import ECparse
import ec_parse
#from parsers.epar_parse import epar_parse

from joblib import delayed, Parallel


# Asks for the class of the PDF that you want to parse [IE 'ECparse']


def parse_test_file(filetype):
    filename = 'dec_orphan/o1060_dec_124808.pdf'

    pdf = fitz.open(filename)  # open document

    table = filetype.get_table(pdf)  # get formatted dictionary

    pdf.close()  # close document

    res = filetype.get_all_test(filename, table)

    # print found attributes and formatted table
    print(res)
    # print(json.dumps(table, indent=3))


def parse_folder(filetype, folder_name):
    # PARSE WHOLE Folder

    # debug to indicate progress
    counter = 0
    print(f'Starting... on {folder_name}')

    f = open('results/results_' + folder_name + '.txt', 'w', encoding="utf-8")  # open/clean output file

    pdf_count = len(os.listdir(folder_name))
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
    # try to open
    try:
        pdf = fitz.open(folder_name + "/" + filename)  # open document
        table = filetype.get_table(pdf)  # get formatted dictionary

        pdf.close()  # close document
        filedata = filetype.get_all(filedata, table)
        filedata['status'] = 'Parsed'

        return filedata

    # could not parse
    # TODO: Add exception type
    except:
        filedata['status'] = 'could not parse'
        return filedata

res = scrape_pdf('h001_dec_2831.pdf',1,ec_parse,'dec_human',3)
print(res)
#parse_test_file(ec_parse)
