# importing all the required modules
#import PyPDF2 replaces with PyMuPDF
import fitz
import json
import os #to get all file names in folder

import ECparse

for filename in os.listdir('decision_files'):
    pdf = fitz.open(filename)  # open document

    table = ECparse.getTableEC(pdf)  #get formated dictionary

    pdf.close() #close document

    res = [filename]

    res.append(ECparse.tableEC_getDate(table))
    res.append(ECparse.tableEC_getName(table))
    res.append(ECparse.tableEC_getAS(table))
    
    print(res)
    #print(json.dumps(table, indent=3))
    