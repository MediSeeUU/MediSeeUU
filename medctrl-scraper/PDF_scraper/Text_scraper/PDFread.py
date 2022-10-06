# importing all the required modules
import json
import fitz  # part of pip install PyMuPDF
import os  # to get all file names in folder
# external files for debug
#import ECparse
#import EPARparse
import json

# external files
import ECparse
import EPARparse


def writeData(outputFile, filedata):
    values = list(filedata.values())
    output = '@'.join(map(str, values))
    outputFile.writelines(output)
    outputFile.writelines('\n')


# Asks for the class of the PDF that you want to parse [IE 'ECparse']
def parseTestFile(filetype):
    # filename = 'decisions/h081_dec_140667.pdf'
    filename = 'dec_human/h008_dec_121029.pdf'

    pdf = fitz.open(filename)  # open document

    (table, pdf_format) = filetype.getTable(pdf)  # get formatted dictionary

    if filetype.unreadable(table):
        print(str(filename) + ' has no text')

    pdf.close()  # close document

    res = filetype.getAllTest(filename, table, pdf_format)

    # print found attributes and formatted table
    # print(res)
    print(json.dumps(table, indent=3))
    # print(pdf_format)


def parseFolder(filetype, folder_name):
    # PARSE WHOLE Folder

    # debug to indicate progress
    counter = 0
    print(f'Starting... on {folder_name}')

    f = open('results/results_' + folder_name + '.txt', 'w', encoding="utf-8")  # open/clean output file

    # to make sure f is always closed if scrape is interrupted.
    try:
        pdfCount = len(os.listdir(folder_name))

        for filename in os.listdir(folder_name):

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
                    writeData(f, filedata)
                    continue

                filedata = filetype.getAll(filedata, table, pdf_format)

                # if filedata['status'] == 'Failure unknown reason':
                filedata['status'] = 'Parsed'

                writeData(f, filedata)

            # could not parse
            except:
                # check if html
                try:
                    # open file to check first line
                    f2 = open(str(folder_name + "/" + filename), 'r', encoding="utf8")
                    firstline = f2.readline()

                    if 'html' in firstline.lower():
                        filedata['status'] = 'HTML'
                        writeData(f, filedata)
                        f2.close()
                        continue
                    f2.close()  # close opened file
                except:
                    pass

                # check if could not open PDF
                if corrupt:
                    filedata['status'] = 'corrupt/could not open'
                    writeData(f, filedata)
                    continue

                # other parse error (uses default 'Failure unknown reason')
                else:
                    writeData(f, filedata)
                    continue


    except:
        pass
    f.close()  # close output file.
    print('Done')


#parseFolder(ECparse, 'dec_orphan')
#parseFolder(EPARparse, 'epars')
parseTestFile(ECparse)
