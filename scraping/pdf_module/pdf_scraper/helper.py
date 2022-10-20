import datetime
import dateutil.parser

roman_numbers = {
    "i": "1",
    "ii": "2",
    "iii": "3",
    "iv": "4",
    "v": "5",
    "vi": "6",
    "vii": "7",
    "viii": "8",
    "ix": "9",
    "x": "10",
    "xi": "11",
    "xii": "12"
}

months = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "sept": "09",
    "october": "10",
    "november": "11",
    "december": "12"
}


def convert_months(date: str) -> str:
    for k in months.keys():
        if k in date:
            date = date.replace(f" {k} ", f"/{months[k]}/")
            break

    return date


def convert_roman_numbers(date: str) -> str:
    """ Converts the roman numbers (up to XII) to normal numbers
    Parameters
    ----------
    date: string pattern of the date
    Returns
    -------
    date: string pattern of the corrected date
    """

    # sort roman_numbers on length (big to small)
    # otherwise I is found in VII before VII is found in VII
    for k in sorted(roman_numbers, key=len, reverse=True):
        if k in date:
            date = date.replace(k, roman_numbers[k])
            break

    return date


def convert_articles(articles: [str]) -> [str]:
    res = []
    for article in articles:
        num = article.split(' ')[1]
        newnum = ""
        for c in num:
            if c == '(':
                newnum += '.'
            elif c == ')':
                continue
            else:
                newnum += c
        res.append('article ' + newnum)
    return res


def get_date(txt: str) -> datetime:
    if txt != '':
        txt = txt.lower()
        try:
            return dateutil.parser.parse(txt, fuzzy=True)
        except:
            pass
        try:
            tempdate = convert_roman_numbers(txt)
            return dateutil.parser.parse(tempdate, fuzzy=True)
        except:
            pass

        try:
            tempdate = convert_months(txt)
            return dateutil.parser.parse(tempdate, fuzzy=True)
        except:
            pass

    return datetime.datetime(1980, 1, 1, 0, 0)