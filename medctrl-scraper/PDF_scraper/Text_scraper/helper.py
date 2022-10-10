import datetime
import dateutil.parser

roman_numbers = {
    "I": "1",
    "II": "2",
    "III": "3",
    "IV": "4",
    "V": "5",
    "VI": "6",
    "VII": "7",
    "VIII": "8",
    "IX": "9",
    "X": "10",
    "XI": "11",
    "XII": "12"
}

months = {
    "January": "1",
    "February": "2",
    "March": "3",
    "April": "4",
    "May": "5",
    "June": "6",
    "July": "7",
    "August": "8",
    "September": "9",
    "October": "10",
    "November": "11",
    "December": "12"
}


def convert_months(date: str):
    for k in months.keys():
        if k in date:
            date = date.replace(f" {k} ", f"/{months[k]}/")
            break

    return date


def convert_roman_numbers(date: str):
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


def getDate(txt):
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
        tempdate = convert_roman_numbers(txt)
        return dateutil.parser.parse(tempdate, fuzzy=True)
    except:
        pass

    return datetime.datetime(1980, 1, 1, 0, 0)