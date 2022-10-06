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

    pdf_format = PDFhelper.getTextFormatLower(pdf)

    # Front page - find first occurrence of 'Assessment report', not yet used
    (content, rem) = PDFhelper.findBetweenFormat('assessment report', 'table of contents', pdf_format, False)
    (_, font, _) = content[0]
    if font > 10.5:
        table['intro']['front_page'] = PDFhelper.filterFont([], [], content)

    # filter table of contents
    (content_table, rem) = PDFhelper.findBetweenFormat('table of contents', 'scientific discussion', rem, True)
    if not content_table:
        rem = pdf_format

    # content
    (content, rem1) = PDFhelper.findBetweenFormat('information on the procedure', 'scientific discussion', rem, True)
    (_, font, _) = content[len(content) - 1]
    if font < 10.5:
        (content, rem1) = PDFhelper.findFromFormat('information on the procedure', rem, True)
    table['background']['main_text'] = PDFhelper.filterFont([], [], content)

    # scientific discussion
    table['discussion']['dis_text'] = PDFhelper.filterFont([], [], rem1)

    return table, pdf_format


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
    return ''
