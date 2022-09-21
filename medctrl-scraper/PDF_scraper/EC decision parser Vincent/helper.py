import dateutil.parser

def getDate(txt):
    try:
        return dateutil.parser.parse(txt, fuzzy = True)
    except:
        return datetime.datetime(1980, 1, 1, 0, 0)