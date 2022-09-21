# importing all the required modules
#import PyPDF2 replaces with PyMuPDF
import fitz
import json

import ECparse

pdf = fitz.open('test_xenon.pdf')  # open document

table = ECparse.getTableEC(pdf)  #get formated dictionary

pdf.close() #close document

print(ECparse.tableEC_getDate(table))
print(ECparse.tableEC_getName(table))
print(json.dumps(table, indent=3))