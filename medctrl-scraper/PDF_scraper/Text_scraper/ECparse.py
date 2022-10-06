# EC parser
import re
import helper
import PDFhelper


# EC Decision document

# Creates ordened string with all relevant data for EC decision document
def getAllTest(filename, table, pdf_format):
    res = [filename, table_getDate(table), table_getPN(table), table_getAS2(table), table_getNAS(table),
           table_getATMP(table, pdf_format), table_getOrphanDesignation(table)]
    return res


def getAll(filedata, table, pdf_format):
    #filedata['status'] = table_checkValid(table)
    filedata['DecisionDate'] = table_getDate(table)
    filedata['BrandName'] = table_getPN(table)
    filedata['ActiveSubstance'] = table_getAS2(table)
    filedata['NAS'] = table_getNAS(table)
    filedata['ATMP'] = table_getATMP(table, pdf_format)
    filedata['OD'] = table_getOrphanDesignation(table)
    filedata['MAH'] = table_getMAH(table)
    filedata['CMA'] = table_getDecisionType(table)

    return filedata


def getDefault(filename):
    return {'filename': filename,
            'DecisionDate': 'Not parsed',
            'BrandName': 'Not parsed',
            'ActiveSubstance': 'Not parsed',
            'NAS': 'Not parsed',
            'ATMP': 'Not parsed',
            'OD': 'Not parsed',
            'MAH': 'Not parsed',
            'CMA': 'Not parsed',
            'status': 'Failure unknown reason'
            }


# Scans and ordens EC orphan designation pdfs
def getTable(pdf):
    table = {'intro': dict.fromkeys(['front_page']),
             'body': dict.fromkeys(['main_text', 'P1']),
             'decision': dict.fromkeys(['dec_text']),
             'remaining': []}

    pdf_format = PDFhelper.getTextFormat(pdf)

    # intro
    (content, rem) = PDFhelper.findBetweenFormat('DECISION', 'AUTHENTIC', pdf_format, True)
    table['intro']['front_page'] = PDFhelper.filterFont([], [], content)

    # filter second intro message
    (_, rem) = PDFhelper.findBetweenFormat('DECISION', 'COMMISSION', rem, False)

    # content
    (content, rem) = PDFhelper.findBetweenFormat('COMMISSION', 'Whereas:', rem, True)
    table['body']['main_text'] = PDFhelper.filterFont([], [], content)

    # bullet points as one chunck
    (bulletpoints, rem) = PDFhelper.findBetweenFormat('', 'HAS ADOPTED THIS DECISION:', rem, False)

    zoeken = True
    bullet_count = 1
    while zoeken:
        # finds section from start till next bullet point
        (bp_content, bulletpoints) = PDFhelper.findBetweenFormat('', '(' + str(bullet_count + 1) + ')', bulletpoints,
                                                                 False)
        table['body']['P' + str(bullet_count)] = PDFhelper.filterFont([12], [], bp_content)

        # nothing more to be found or stuck in loop
        if bulletpoints == [] or bullet_count > 15:
            zoeken = False
        bullet_count += 1

    # decision
    (content, rem) = PDFhelper.findBetweenFormat('HAS ADOPTED THIS DECISION:', 'Article 1', rem, False)
    table['decision']['dec_text'] = PDFhelper.filterFont([], [], content)

    article_count = PDFhelper.countStr('Article', 'TimesNewRoman,Italic', rem)
    #older docs use different font
    if article_count == 0:
        article_count = PDFhelper.countStr('Article', 'TimesNewRomanPS-ItalicMT', rem)
        

    for arc in range(article_count):
        arc_num = arc + 1

        if arc_num == article_count:
            (content, rem) = PDFhelper.findBetweenFormat('Article ' + str(arc_num), 'Done at', rem, False)
            table['decision']['A' + str(arc_num)] = PDFhelper.filterFont([12], [], content)
        else:
            (content, rem) = PDFhelper.findBetweenFormat('Article ' + str(arc_num), 'Article ' + str(arc_num + 1), rem,
                                                         False)
            table['decision']['A' + str(arc_num)] = PDFhelper.filterFont([12], [], content)

    table['remaining'] = PDFhelper.filterFont([12], [], rem)

    return table, pdf_format


# check if table front page is empty (indicating image/unreadable)
def unreadable(table):
    return not table['intro']['front_page']

# def table_checkValid(table):
#     for txt in table['decision']['dec_text']:
#         if 'HAS ADOPTED THIS DECISION' in txt:
#             return 'Failure unknown reason'
#     return 'Not valid'

def get_name_section(txt):
    #to make sure no commas from pdf format itself, split at date.
    #try since this only works on default english documents.
    
    try:
        txt = txt.split('of ')
        txt = ' '.join(txt[1:]) #to remove part before date
    except:
        pass
    
    section = ''
    
    #try multiple quotation combinations
    try:
        section = re.search('"([^"]*)"', txt)[0]
        section = section.replace('"', '')
    except:
        try:
            section = re.search('“(.+?)”', txt)[0]
            section = section.replace('“', '')
            section = section.replace('”', '')
        except:
            try:
                section = re.search('“(.+?)"', txt)[0]
                section = section.replace('“', '')
                section = section.replace('"', '')
            except:
                try:
                    section = re.search('"(.+?)\'', txt)[0]
                    section = section.replace('"', '')
                    section = section.replace('\'', '')
                except:
                    pass
                
    if section == None:
        section = ''
    return section

def table_getPN(table):
    section = table['intro']['front_page']
    
    txt = ''
    for line in section:
        txt += line

    section = get_name_section(txt)
    
    if section != '':
        # takes everything before split operator
        if ' - ' in section:
            res = section.split(' - ')[:-1]
            res = ''.join(res)
            return res.strip()
        if ' – ' in section:
            res = section.split(' – ')[:-1]
            res = ''.join(res)
            return res.strip()
        #no active substace, so return whole name
        return section
    
    #for orphan structure
    try:
        res = txt.split('relating to the designation of medicinal product')[1]
        res = res.split('as an orphan medicinal')[0]
        res = res.replace('"', '')
        res = res.replace('“', '')
        res = res.replace('”', '')
        res.strip()
        return res
    except:
        pass
    
    return 'Product name Not Found'

def table_getAS2(table):
    section = table['intro']['front_page']
    
    txt = ''
    for line in section:
        txt += line
    
    section = get_name_section(txt)
    
    try:
        if section != '':
            # takes last element after split operator
            if ' - ' in section:
                return section.split(' - ')[-1].strip()
            if ' – ' in section:
                return section.split(' – ')[-1].strip()
    except:
        pass
    return 'Active Substance Not Found'
    
    

    
    
def table_getDecisionType(table):
    txt = get_section_text(table,'body',True)
    excep = re.search(r"article\s+14\W8", txt.lower())  # exceptional: Article 14(8) or alt. (e.g. Article 14.8)

    # conditional
    if "507/2006" in txt or "conditional marketing authorisation" in txt.lower():
        return "conditional"

    # exceptional
    elif "exceptional circumstances" in txt.lower() or excep is not None:
        return "exceptional"
    else:
        return "CMA Not Found"
    
def table_getMAH(table):
    section = table['body']['main_text']
    
    mahlines = ''
    found = False
    for line in section:
        #finds first line
        identifiers = ['the notification submitted','the application submitted','the application(s) submitted']
        if any(iden in line.lower() for iden in identifiers):
            mahlines += line
            found = True
            continue
        #gets second line    
        if found:
            mahlines += line
            break
    if mahlines == '':
        return 'MAH Not Found'
    
    #format found lines
    else:
        #gets part after submitted by line
        mah = mahlines.split(" by ",1)[1]
        #remove part after MAH
        mah = mah.split(" on ",1)[0]
        #different format
        mah = mah.split(" under ",1)[0]
        
        mah = mah.split('  (the marketing authorisation holder)')[0]
        #remove comma if there was comma before on
        if mah[-1] == ',':
            mah = mah[:-1]
        return mah.strip()


def table_getOrphanDesignation(table):
    txt = get_section_text(table,'decision',True)
    if 'orphan medicinal product' in txt.lower() and 'has adopted this decision' in txt.lower():
        return 'adopted'
    return 'appointed'


def table_getDate(table):
    section = table['intro']['front_page']
    for txt in section:
        if 'of ' in txt:
            if '[.....' in txt:
                return 'Date is blank'
            return helper.getDate(txt)
    return helper.getDate('')


# NOT OPTIMISED YET
def table_getATMP(_, pdf_format):
    lines = PDFhelper.filterFont([], [], pdf_format)
    txt = ''.join(lines)
    txt = txt.lower()
    regulation = "Regulation (EC) No 1394/2007"
    fn_idx = txt.find("regulation as last amended by")  # sometimes regulation is mentioned in footnote
    footnote = txt[fn_idx:fn_idx + 70]  # select the sentence if the regulation is mentioned in the footnote
    txt = txt.replace(footnote, "")  # remove the footnote with the regulation from the text
    if regulation.lower() in txt.lower():
        return True
    else:
        return False


# new active substance bool
def table_getNAS(table):
    txt = get_section_text(table,'body',False)
    if "committee for medicinal products for human use" in txt.lower() and "a new active substance" in txt.lower():
        return True
    return False

def get_section_text(table, section, inclusive):
    iterPoints = iter(table[section])
    if not inclusive:
        next(iterPoints)  # to skip main_text
    temp = ''
    for point in iterPoints:
        for txt in table[section][point]:
            temp += txt
    return temp



#OLD NAME AND ACTIVE SUBSTANCE FUNCTIONS
# def table_getName(table):
#     section = table['intro']['front_page']

#     temp = ''
#     for txt in section:
#         temp += txt

#     if '\"' in temp:
#         try:
#             section = re.search('"([^"]*)"', temp)[0]
#             section = section.replace('"', '')
#             # gets only first section
#             if ' - ' in section:
#                 return section.split(' - ')[0].strip()
#             if ' – ' in section:
#                 return section.split(' – ')[0].strip()
#             return section
#         except:
#             pass
#     if '“' in temp:
#         try:
#             section = re.search('“(.+?)”', temp)[0]
#             if ' -' in section:
#                 section = section.split(' - ')
#                 section.pop()
#                 section = ''.join(section)
#                 section = section.replace('“', '')
#                 section = section.replace('”', '')
#                 return section
#             elif ' – ' in section:
#                 section = section.split(' – ')
#                 section.pop()
#                 section = ''.join(section)
#                 section = section.replace('“', '')
#                 section = section.replace('”', '')
#                 return section
#         except:
#             # this is repetitive and should be cleaned
#             try:
#                 section = re.search('“(.+?)"', temp)[0]
#                 if ' - ' in section:
#                     section = section.split(' - ')
#                     section.pop()
#                     section = ''.join(section)
#                     section = section.replace('“', '')
#                     section = section.replace('”', '')
#                     return section
#                 elif ' – ' in section:
#                     section = section.split(' – ')
#                     section.pop()
#                     section = ''.join(section)
#                     section = section.replace('“', '')
#                     section = section.replace('”', '')
#                     return section
#             except:
#                 pass
#         return section

#     # # old cases that don't use quotations
#     # if ' - ' in temp:
#     #     section = temp.split(' for ', 1)[1]
#     #     section = section.split(' - ')[0]
#     #     return section

#     return "Product name Not Found"


# # active substance
# def table_getAS(table):
#     section = table['intro']['front_page']

#     temp = ''
#     for txt in section:
#         temp += txt

#     # find normal quotes
#     if '\"' in temp:
#         try:
#             section = re.search('"([^"]*)"', temp)[0]
#             section = section.replace('"', '')
#             # gets only second section if present
#             try:
#                 # gets only first section
#                 return section.split(' - ')[1].strip()
#             except:
#                 try:
#                     return section.split(' – ')[1].strip()
#                 except:
#                     pass
#         except:
#             pass

#     # finds unicode quote
#     if '“' in temp:
#         try:
#             section = re.search('“(.+?)”', temp)[0].split(' - ').pop()
#             section = ''.join(section)
#             section = section.replace('“', '')
#             section = section.replace('”', '')
#             return section
#         except:
#             try:
#                 section = re.search('“(.+?)”', temp)[0].split(' – ').pop()
#                 section = ''.join(section)
#                 section = section.replace('“', '')
#                 section = section.replace('”', '')
#                 return section
#             except:
#                 try:
#                     section = re.search('“(.+?)"', temp)[0].split(' - ').pop()
#                     section = ''.join(section)
#                     section = section.replace('“', '')
#                     section = section.replace('”', '')
#                     return section
#                 except:
#                     try:
#                         section = re.search('“(.+?)"', temp)[0].split(' – ').pop()
#                         section = ''.join(section)
#                         section = section.replace('“', '')
#                         section = section.replace('”', '')
#                         return section
#                     except:
#                         pass

#     # # old cases that don't use quotations
#     # if ' - ' in temp:
#     #     section = temp.split(' for ', 1)[1]
#     #     section = section.split(' - ')[1]
#     #     # till next comma

#     #     # MIGHT LOSE INFORMATION IS SPECIFIC CASES
#     #     section = section.split(',')[0]
#     #     return section

#     return "Active Substance Not Found"



