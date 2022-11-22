import datetime
import re

import dateutil.parser as dateparser

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
    "feb": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "sept": "09",
    "sep": "09",
    "october": "10",
    "november": "11",
    "december": "12"
}

legal_bases = {'article 10.b', 'article 8.3', 'article 10.2', 'article 4.8.3', 'article 10.a', 'article 10b',
               'article 10c', 'article 10.3', 'article 4.8.2', 'article 10a', 'article 4.8.1', 'article 10.c',
               'article 4.8', 'article 10.1', 'article 10.4'}


def convert_months(date: str) -> str:
    """
    Converts written months (january) to a numeric value

    Args:
        date (str): string containing fully writen month

    Returns:
        str: string with month replaces by numeric value
    """
    date = date.replace("th", "")
    for k in months.keys():
        if k in date:
            date = date.replace(f" {k} ", f"/{months[k]}/")
            break

    return date


def convert_roman_numbers(date: str) -> str:
    """
    Converts the roman numbers (up to XII) to normal numbers

    Args:
        date: string pattern of the date

    Returns
        date: string pattern of the corrected date
    """

    # sort roman_numbers on length (big to small)
    # otherwise I is found in VII before VII is found in VII
    for k in sorted(roman_numbers, key=len, reverse=True):
        if k in date:
            date = date.replace(k, roman_numbers[k])
            break

    return date


def convert_articles(articles: list[str]) -> list[str]:
    """
    Args:
        articles ([str]): The articles to convert to the right format

    Returns:
        list[str]: The converted articles
    """
    res = []
    for article in articles:
        # remove all whitespace from articles
        article = "".join(article.split())
        # add space after article
        article = article[:7] + ' ' + article[7:]
        num = article.split(' ')[1]
        new_num = ""
        for c in num:
            if c == '(':
                new_num += '.'
            # do not add the following characters
            elif c == ')' or c == '-' or c == '–' or c == '‘' or \
                    c == '/' or c == ',':
                continue
            else:
                new_num += c
        # Remove trailing characters
        new_num = new_num.strip(".: ")
        # Add '.' between number and letter in legal basis, IE 10b -> 10.b
        if re.search(r"\d+[a-z]", new_num):
            i = len(new_num) - 1
            new_num = new_num[:i] + '.' + new_num [i:]
        res.append('article ' + new_num)
    return list(set(res))


def get_date(txt: str) -> datetime.datetime:
    """
    Extracts date from a text, also including months with roman numerals and fully written months (IV, january)

    Args:
        txt (str): text containing date

    Returns:
        datetime.datetime: found date.
    """
    if txt:
        txt = txt.lower()
        try:
            return dateparser.parse(txt, fuzzy=True)
        except dateparser._parser.ParserError:
            pass
        temp_date = txt.split(' ')[0]
        temp_date = convert_roman_numbers(temp_date)
        try:
            return dateparser.parse(temp_date, fuzzy=True)
        except dateparser._parser.ParserError:
            pass

        try:
            temp_date = convert_months(txt)
            return dateparser.parse(temp_date, fuzzy=True)
        except dateparser._parser.ParserError:
            pass

    return datetime.datetime(1980, 1, 1, 0, 0)
