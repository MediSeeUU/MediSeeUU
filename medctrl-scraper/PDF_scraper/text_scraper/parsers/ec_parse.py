# EC parser
import re
import helper
import pdf_helper
import datetime

# EC Decision document

# Creates ordered string with all relevant data for EC decision document
def get_all_test(filename, table):
    return get_all(get_default(filename),table)



def get_all(filedata, table):
    filedata['DecisionDate']    = table_get_date(table)
    filedata['BrandName']       = table_get_pn(table)
    filedata['ActiveSubstance'] = table_get_as2(table)
    filedata['NAS']             = table_get_nas(table)
    filedata['ATMP']            = table_get_atmp(table)
    filedata['OD']              = table_get_orphan_designation(table)
    filedata['MAH']             = table_get_mah(table)
    filedata['CMA']             = table_get_decision_type(table, filedata['DecisionDate'])
    return filedata


def get_default(filename):
    default = 'Not parsed'
    return {'filename': filename,
            'DecisionDate': default,
            'BrandName': default,
            'ActiveSubstance': default,
            'NAS': default,
            'ATMP': default,
            'OD': default,
            'MAH': default,
            'CMA': default,
            'status': 'Failure unknown reason'
            }


# Scans and ordens EC orphan designation pdfs
def get_table(pdf):
    pdf_format = pdf_helper.get_text_format(pdf)
    return pdf_helper.format_to_string(pdf_format)

def get_name_section(txt):
    # to make sure no commas from pdf format itself, split at date.
    # try since this only works on default english documents.

    try:
        txt = txt.split('of ')
        txt = ' '.join(txt[1:])  # to remove part before date
    except:
        pass

    section = ''

    # try multiple quotation combinations
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


def table_get_pn(txt):

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
        # no active substace, so return whole name
        return section

    # for orphan structure
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


def table_get_as2(txt):
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


def table_get_decision_type(txt, date):
    if date < datetime.datetime(2006, 1, 1):
        return "CMA not available before 2006"
    
    excep = re.search(r"article\s+14\W8", txt.lower())  # exceptional: Article 14(8) or alt. (e.g. Article 14.8)
    # conditional
    if "507/2006" in txt or "conditional marketing authorisation" in txt.lower():
        return "conditional"

    # exceptional
    elif "exceptional circumstances" in txt.lower() or excep is not None:
        return "exceptional"
    else:
        return "CMA Not Found"


def table_get_mah(txt):
    mahline = ''
    try:
        #why [5]? 
        mahline = re.split(r'(( the notification submitted)|( the application submitted)|( the application\(s\) submitted))', txt)[5]
        # gets part after submitted by line
        mah = mahline.split(" by ", 1)[1]
        #clean potential stop words.
        # remove part after MAH
        mah = re.split(r'(( on ))|(( under ))|(( (the marketing authorisation holder)))', mah, 1)[0]
        # remove comma if there was comma before on
        if mah[-1] == ',':
            mah = mah[:-1]
        return mah.strip()
    
    except:
        return 'MAH Not Found'
      


def table_get_orphan_designation(txt):
    if 'orphan medicinal product' in txt.lower() and 'has adopted this decision' in txt.lower():
        return 'adopted'
    return 'appointed'


def table_get_date(txt):
    try:
        section = re.split('of ',txt,1)[1]
        section = section[:15]
        return helper.getDate(section)
    except:
        pass
    return helper.getDate('')


# NOT OPTIMISED YET
def table_get_atmp(txt):
    regulation = "Regulation (EC) No 1394/2007"
    fn_idx = txt.find("regulation as last amended by")  # sometimes regulation is mentioned in footnote
    footnote = txt[fn_idx:fn_idx + 70]  # select the sentence if the regulation is mentioned in the footnote
    txt = txt.replace(footnote, "")  # remove the footnote with the regulation from the text
    if regulation.lower() in txt.lower():
        return True
    else:
        return False


# new active substance bool
def table_get_nas(txt):
    if "committee for medicinal products for human use" in txt.lower() and "a new active substance" in txt.lower():
        return True
    return False

