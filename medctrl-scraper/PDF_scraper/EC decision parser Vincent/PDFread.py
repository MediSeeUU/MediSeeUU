# importing all the required modules
#import PyPDF2 replaces with PyMuPDF
import fitz
import json
import os #to get all file names in folder

import ECparse


# filename = 'decisions/h001_dec_2830.pdf'

# pdf = fitz.open(filename)  # open document

# table = ECparse.getTableEC(pdf)  #get formated dictionary

# if table['intro']['front_page'] == []:
#     print(str(filename) + ' has no text')

# pdf.close() #close document

# res = [filename]

# res.append(ECparse.tableEC_getDate(table))
# res.append(ECparse.tableEC_getName(table))
# res.append(ECparse.tableEC_getAS(table))

# print(res)
# print(json.dumps(table, indent=3))



# PARSE WHOLE MAP
counter = 0
f = open('results.txt', 'w') 
for filename in os.listdir('decisions'):
    
    
    counter += 1
    print(counter)
    corrupt = False
    
    #can't open
    try:
        pdf = fitz.open("decisions/" + filename)  # open document
    except:
        corrupt = True
        
    try:
        table = ECparse.getTableEC(pdf)  #get formated dictionary
        
        #check if table front page is empty (indicating image/unreadable)
        if table['intro']['front_page'] == []:
            f.writelines(str(filename) + ' has no text')
            f.write('\n')
            continue
            
    
        pdf.close() #close document
    
        res1 = res2 = res3 = 'Not parsed'
        res1 = ECparse.tableEC_getDate(table)
        res2 = ECparse.tableEC_getName(table)
        res3 = ECparse.tableEC_getAS(table)
        
        f.writelines(str(filename) + ';' + str(res1) + ';' + str(res2) + ';' + str(res3))
        f.write('\n')
        #print(res)
        #print(json.dumps(table, indent=3))
    #could not parse
    except:
        #check if html
        try:
            f2 = open(str("decisions/" + filename), 'r', encoding="utf8")
            firstline = f2.readline() 
        
            if 'html' in firstline.lower():
                f.writelines(f'{filename} is an HTML')
                f.write('\n')
                f2.close()
                continue
            f2.close()
        except:
            pass

        #check if could not open PDF       
        if corrupt:
            f.writelines(f'{filename} is corrupt/could not open')
            f.write('\n')
            continue
        #other parse error
        else:
            f.writelines(str(filename) + ' was a failure for unknown reason')
            f.write('\n')
            continue
    
f.close()