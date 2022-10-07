# EPAR Parser
import re
import PDFhelper


# Creates ordened string with all relevant data for EPAR
def getAllTest(filename, table, _):
    res = [filename, table_getDate(table), table_getOpinionDate(table), table_getLegalBasis(table)]
    return res


def getAll(filedata, table, _):
    filedata['ema_procedure_start_initial'] = table_getDate(table)
    filedata['chmp_opinion_date'] = table_getOpinionDate(table)
    filedata['eu_legal_basis'] = table_getLegalBasis(table)
    return filedata


def getDefault(filename):
    return {'filename': filename,
            'ema_procedure_start_initial': 'Not parsed',
            'chmp_opinion_date': 'Not parsed',
            'eu_legal_basis': 'Not parsed'
            }


# Scans and ordens EPAR document
def getTable(pdf):
    table = {'intro': dict.fromkeys(['front_page']),
             'background': dict.fromkeys(['main_text']),
             'discussion': dict.fromkeys(['dis_text'])}

    pdf_format = PDFhelper.get_text_format(pdf, True)

    # Front page - find first occurrence of 'Assessment report', not yet used
    rem = get_front_page(pdf_format, table)
    # filter table of contents
    rem = filter_table_of_content(pdf_format)
    # background information on the procedure
    rem1 = get_background_info(rem, table)
    # scientific discussion
    table['discussion']['dis_text'] = PDFhelper.filterFont([], [], rem1)

    return table, pdf_format


def filter_table_of_content(pdf_format):
    (content_table, rem) = PDFhelper.findBetweenFormat('information on the procedure', 'information on the procedure',
                                                       pdf_format, False)
    return rem


def get_background_info(rem, table):
    (content, rem1) = PDFhelper.findBetweenFormatSize('information on the procedure', 'scientific discussion',
                                                      rem, True, 10)
    table['background']['main_text'] = PDFhelper.filterFont([], [], content)
    return rem1


def get_front_page(pdf_format, table):
    (content, rem) = PDFhelper.findBetweenFormat('assessment report', 'table of contents', pdf_format, False)
    table['intro']['front_page'] = []
    if content:
        (_, font, _) = content[0]
        if font > 10.5:
            table['intro']['front_page'] = PDFhelper.filterFont([], [], content)
    if not rem:
        (content, rem) = PDFhelper.findBetweenFormat('assessment report', 'background information on the procedure',
                                                     pdf_format, False)
        table['intro']['front_page'] = PDFhelper.filterFont([], [], content)
    return rem


# check if table front page is empty (indicating image/unreadable)
def unreadable(table):
    return not table['intro']['front_page']


# ema_procedure_start_initial
def table_getDate(table):
    section = table['background']['main_text']
    found = False
    regex_date = re.compile(r'\d{1,2} \w+ \d{4}')
    regex_ema = re.compile(r'the application was received by the em\w+ on')
    for txt in section:
        if found and regex_date.search(txt):
            return re.search(r'\d{1,2} \w+ \d{4}', txt)[0]
        elif regex_ema.search(txt):
            found = True
            if regex_date.search(txt):
                return re.search(r'\d{1,2} \w+ \d{4}', txt)[0]
    return ''


# chmp_opinion_date
def table_getOpinionDate(table):
    section = table['background']['main_text']
    list_size = len(section)
    regex_date = re.compile(r'\d{1,2} \w+ \d{4}')
    for i in range(list_size):
        if regex_date.search(section[list_size - i - 1]):
            return re.search(r'\d{1,2} \w+ \d{4}', section[list_size - i - 1])[0]
    return ''


# eu_legal_basis
def table_getLegalBasis(table):
    section = table['background']['main_text']
    found = False
    regex_legal = re.compile(r'article [^ ]+')
    for txt in section:
        if found and regex_legal.search(txt):
            return re.search(r'article [^ ]+', txt)[0]
        elif 'legal basis for' in txt:
            found = True
    return 'none'


# eu_legal_basis
def table_getprime(table):
    # section = table['background']['main_text']
    # found = False
    # regex_legal = re.compile(r'article [^ ]+')
    # for txt in section:
    #     if found and regex_legal.search(txt):
    #         return re.search(r'article [^ ]+', txt)[0]
    #     elif 'legal basis for' in txt:
    #         found = True
    return ''
