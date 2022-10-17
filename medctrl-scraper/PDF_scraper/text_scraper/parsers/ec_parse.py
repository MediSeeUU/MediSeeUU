# EC parser
import re
import os.path as path
import helper
import pdf_helper
import datetime
import fitz

# EC Decision document

# Given a pdf, returns one long string of text
def get_txt_from_pdf(pdf):
    pdf_format = pdf_helper.get_text_format(pdf)
    return pdf_helper.format_to_string(pdf_format)

def parse_file(filename, directory, medicine_struct):
    try:
        pdf = fitz.open(path.join(directory, filename))
        txt = get_txt_from_pdf(pdf)
        medicine_struct.decisions.append(get_all(filename, txt))
        pdf.close()
    except:
        print("Could not open PDF: " + filename)
    return medicine_struct

# Given a dictionary, fills in all attributes for EC decisions
def get_all(filename, txt):
    #human use file attributes
    if '_h_' in filename:
        filedata = get_data_human_use(filename,txt)
        return filedata

    #orphan file attributes
    if '_o_' in filename:
        filedata = get_data_orphan(filename,txt)
        return filedata

    #if other file return data with everything 'Not parsed'
    return get_default_human_use(filename)

# The default values before starting a parse.
def get_default_human_use(filename):
    default = 'Not parsed'
    return {'filename': filename,
            'eu_aut_date': default,
            'eu_brand_name_initial': default,
            'active_substance': default,
            'eu_nas': default,
            'eu_atmp': default,
            'eu_od_initial': default,
            'eu_mah_initial': default,
            'eu_aut_type_initial': default,
            'status': 'Failure unknown reason'
            }

# The default values before starting a parse.
def get_default_orphan(filename):
    default = 'Not parsed'
    return {'filename': filename,
            'eu_aut_date': default,
            'eu_brand_name_initial': default,
            'eu_od_initial': default,
            'eu_mah_initial': default,
            'eu_od_comp_date': default,
            'status': 'Failure unknown reason'
            }

def get_data_human_use(filename,txt):
    filedata = get_default_human_use(filename)
    date = dec_get_date(txt)
    filedata['eu_aut_date'] = date

    #if date was left blank return dont find date dependant attributes.
    if isinstance(date,str):
        date = dec_get_date('')

    filedata['eu_brand_name_initial']       = dec_get_bn(txt)
    filedata['active_substance']            = dec_get_as(txt)
    filedata['eu_nas']                      = dec_get_nas(txt, date)
    filedata['eu_atmp']                     = dec_get_atmp(txt, date)
    filedata['eu_od_initial']               = dec_get_od(txt, date)
    filedata['eu_mah_initial']              = dec_get_mah(txt)
    filedata['eu_aut_type_initial']         = dec_get_decision_type(txt, date)
    return filedata

def get_data_orphan(filename,txt):
    filedata = get_default_orphan(filename)
    date = dec_get_date(txt)
    filedata['eu_aut_date'] = date

    #if date was left blank return dont find date dependant attributes.
    if isinstance(date,str):
        date = dec_get_date('')
    filedata['eu_brand_name_initial']   = dec_get_bn(txt)
    filedata['eu_od_initial']           = dec_get_od(txt, date)
    filedata['eu_mah_initial']          = dec_get_mah(txt)
    filedata['eu_od_comp_date']         = dec_get_od_comp_date(txt)

#FUNCTIONS FOR EACH ATTRIBUTE


def dec_get_date(txt):
    try:
        section = re.split('of ',txt,1)[1]
        section = section[:15]
        if '...' in section:
            return 'Date is blank'
        #check if there are digits on first page
        if bool(re.search(r'\d', section)):
            return helper.get_date(section)
        #there are few cases where date on first page is missing
        #retry on second page before giving up.
        try:
            next_page = re.split('commission decision',txt.lower())[2]
            section = re.split('of ',next_page,1)[1]
            section = section[:15]
            return helper.get_date(section)
        except:
            pass
    except:
        pass
    return helper.get_date('')


def dec_get_bn(txt):
    #returns a section containing just the brandname (and potentially the active substance)
    section = get_name_section(txt)

    #use advance regex to find brandname
    regres = None
    try:
        regres = re.search(r'"(\w+[\s\w®/\.,"]*)\s?[-–]\s?\w+.*"', section)
    except:
        pass

    if regres is not None:
        return regres.group(0)

    if section != '':
        # takes everything before split operator, to remove active substance.
        if ' -' in section:
            res = section.split(' -')[:-1]
            res = ''.join(res)
            return res.strip()
        if ' –' in section:
            res = section.split(' –')[:-1]
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

    return 'Brandname Not Found'


def dec_get_as(txt):
    #returns a section containing just the brandname (and potentially the active substance)
    section = get_name_section(txt)
    try:
        if section != '':
            # takes last element after split operator, to remove brandname.
            if ' - ' in section:
                return section.split(' - ')[-1].strip()
            if ' – ' in section:
                return section.split(' – ')[-1].strip()
    except:
        pass
    return 'Active Substance Not Found'


def dec_get_decision_type(txt, date):
    #check if there can be a CMA.
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


def dec_get_mah(txt):
    mahline = ''
    try:
        #get text after one of the following indicators.
        mahline = re.split(r'(( the notification submitted)|( the applicatio\w+ submitted)|( the application\(s\) submitted))', txt)[5]
        
        # gets part after submitted by line
        mah = mahline.split(" by ", 1)[1]

        #clean potential stop words.
        # remove part after MAH
        mah = re.split(r'(( on ))|(( under ))|(( (the marketing authorisation holder)))', mah, 1)[0]
        
        # remove comma if there is a comma at the end.
        if mah[-1] == ',':
            mah = mah[:-1]
        return mah.strip()   
    except:
        return 'MAH Not Found'


def dec_get_od(txt,date):
    #check if there can be a NAS.
    if date < datetime.datetime(2000, 4, 28):
        return "NA before 2000"

    if 'orphan medicinal product' in txt.lower():
        if 'has adopted this decision' in txt.lower():
            return 'adopted'
        return 'appointed'
    return 'OD Not Found'


def dec_get_atmp(txt,date):
    #check if there can be a ATMP.
    if date < datetime.datetime(2007, 12, 30):
        return "NA before 2012"

    regulation = "Regulation (EC) No 1394/2007"
    fn_idx = txt.find("regulation as last amended by")  # sometimes regulation is mentioned in footnote
    footnote = txt[fn_idx:fn_idx + 70]  # select the sentence if the regulation is mentioned in the footnote
    txt = txt.replace(footnote, "")  # remove the footnote with the regulation from the text
    if regulation.lower() in txt.lower():
        return True
    else:
        return False


def dec_get_nas(txt,date):
    #check if there can be a NAS.
    if date < datetime.datetime(2012, 1, 1):
        return "NA before 2012"
    
    if "committee for medicinal products for human use" in txt.lower() and "a new active substance" in txt.lower():
        return True
    return False


def dec_get_od_comp_date(txt):
    try:
        section = re.split('of ',txt,1)[1]
        section = section[:15]
        #check if there are digits on first page
        if bool(re.search(r'\d', section)):
            return helper.get_date(section)
        #there are few cases where date on first page is missing
        #retry on second page before giving up.
        try:
            next_page = re.split('commission decision',txt.lower())[2]
            section = re.split('of ',next_page,1)[1]
            section = section[:15]
            return helper.get_date(section)
        except:
            pass
    except:
        pass
    return helper.get_date('')


#HELPERS
#helper function for finding brandname and active substance.
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

    if section is None:
        section = ''
    return section