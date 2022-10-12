# EPAR parsers
import re
import pdf_helper
import helper

date_pattern: str = r'\d{1,2} \w+ \d{4}'
procedure_info = 'information on the procedure'


# Creates ordered string with all relevant data for EPAR
def get_all_test(filename, table, _):
    res = [filename, table_get_date(table), table_get_opinion_date(table), table_get_legal_basis(table)]
    return res


def get_all(filedata, table, _):
    filedata['ema_procedure_start_initial'] = table_get_date(table)
    filedata['chmp_opinion_date'] = table_get_opinion_date(table)
    filedata['eu_legal_basis'] = table_get_legal_basis(table)
    return filedata


def get_default(filename):
    default = 'Not parsed'
    return {'filename': filename,
            'ema_procedure_start_initial': default,
            'chmp_opinion_date': default,
            'eu_legal_basis': default
            }


def parse_file(filename, medicine_struct):
    print(medicine_struct)


# Scans and orders EPAR document
def get_table(pdf):
    table = {'intro': dict.fromkeys(['front_page']),
             'background': dict.fromkeys(['main_text']),
             'discussion': dict.fromkeys(['dis_text'])}

    pdf_format = pdf_helper.get_text_format(pdf, True)
    # Front page - find first occurrence of 'Assessment report', not yet used
    get_front_page(pdf_format, table)
    # filter table of contents
    rem = filter_table_of_content(pdf_format)
    # background information on the procedure
    rem1 = get_background_info(rem, table)
    # scientific discussion
    table['discussion']['dis_text'] = pdf_helper.filter_font([], [], rem1)

    return table, pdf_format


def filter_table_of_content(pdf_format):
    (content_table, rem) = pdf_helper.find_between_format(procedure_info, procedure_info,
                                                          pdf_format, False)
    return rem


def get_background_info(rem, table):
    (content, rem1) = pdf_helper.find_between_format(procedure_info, 'scientific discussion',
                                                     rem, True, 10)
    table['background']['main_text'] = pdf_helper.filter_font([], [], content)
    return rem1


def get_front_page(pdf_format, table):
    (content, rem) = pdf_helper.find_between_format('assessment report', 'table of contents', pdf_format, False)
    table['intro']['front_page'] = []
    if content:
        (_, font, _) = content[0]
        if font > 10.5:
            table['intro']['front_page'] = pdf_helper.filter_font([], [], content)
    if not rem:
        (content, _) = pdf_helper.find_between_format('assessment report', 'background information on the procedure',
                                                      pdf_format, False)
        table['intro']['front_page'] = pdf_helper.filter_font([], [], content)


# check if table front page is empty (indicating image/unreadable)
def unreadable(table):
    return not table['intro']['front_page']


# ema_procedure_start_initial
def table_get_date(table):
    section = table['background']['main_text']
    found = False
    regex_date = re.compile(date_pattern)
    regex_ema = re.compile(r'the application was received by the em\w+ on')
    for txt in section:
        if found and regex_date.search(txt):
            return convert_month(re.search(date_pattern, txt)[0])
        elif regex_ema.search(txt):
            found = True
            if regex_date.search(txt):
                return convert_month(re.search(date_pattern, txt)[0])
    return ''


# chmp_opinion_date
def table_get_opinion_date(table):
    section = table['background']['main_text']
    list_size = len(section)
    regex_date = re.compile(date_pattern)
    for i in range(list_size):
        if regex_date.search(section[list_size - i - 1]):
            return re.search(date_pattern, section[list_size - i - 1])[0]
    return ''


# eu_legal_basis
def table_get_legal_basis(table: object) -> object:
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
def table_get_prime(table):
    return table
