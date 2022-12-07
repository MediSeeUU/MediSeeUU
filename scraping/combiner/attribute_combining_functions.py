import scraping.utilities.definitions.values as values
import scraping.utilities.definitions.sources as src
import scraping.utilities.definitions.attributes as attr
from difflib import SequenceMatcher as SM
import datetime as dt
import logging
import json
import pandas as pd

log = logging.getLogger("combiner")

# TODO: remove try catch
def get_attribute_date(source_string: str, file_dicts: dict[str, dict[str, any]]) -> str:
    if source_string == src.web:
        try:
            return file_dicts[src.web][attr.scrape_date_web]
        except Exception:
            return values.default_date
    else:
        try:
            file_name = file_dicts[source_string][attr.pdf_file]
            return file_dicts[src.web][attr.filedates_web][file_name][attr.meta_file_date]
        except Exception:
            return values.default_date
    

def check_all_equal(values: list[any]) -> bool:
    """
    checks if two values are equal and not None
    Args:
        v1 (any): value to compare
        v2 (any): value to compare

    Returns (bool): result of check
    """
    if len(values) == 0:
        return False

    all_same = True
    for value in values[1:]:
        all_same &= value == values[0]

    return all_same and values[0] is not None


def combine_best_source(eu_pnumber: str, attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]]) -> any:
    """

    Args:
        attribute_name:
        dicts:
        combine_attributes:

    Returns:

    """
    attributes: list[str] = []

    for source in sources:
        dic = file_dicts[source]
        try:
            attributes.append(dic[attribute_name])
        except Exception:
            log.warning(f"COMBINER: can't find value for {attribute_name} in {source}")
            # log.warning("COMBINER: can't find value for ", attribute_name, " in ", dict[attr.source_file])

    attributes.append(values.not_found)
    return attributes[0]

def string_overlap(strings: list[str], min_matching_fraction: float = 0.8) -> str:
    try:
        old_string = strings[0]
        new_string = strings[1]
        sequence_matcher = SM(None, old_string.lower(), new_string.lower())
        overlap = sequence_matcher.find_longest_match(0, len(old_string) - 1, 0, len(new_string) - 1)

        for string in strings[1:]:
            old_string = new_string
            new_string = string
            sequence_matcher = SM(None, old_string.lower(), new_string.lower())
            overlap = sequence_matcher.find_longest_match(0, len(old_string), 0, len(new_string))


        if float(overlap.size / len(strings[0])) >= min_matching_fraction:
            return strings[0][overlap.a:overlap.a + overlap.size]
    except Exception:
        print("COMBINER: no second string")
    return values.insufficient_overlap

# For combine functions
# TODO: fix datum
def combine_select_string_overlap(eu_pnumber: str, attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]],
                                  min_matching_fraction: float = 0.8) -> tuple[str,str]:
    """
    compares two strings to see if a percentage of the shortest string is identical to the longest string
    Args:
        s1 (str): first string
        s2 (str): second string
        perc (float): percentage float between 0 and 1

    Returns (bool): bool indicating equality
    """
    strings = []
    for source in sources:
        dict = file_dicts[source]
        # TODO: Replace try/except with if statements
        try:
            strings.append(dict[attribute_name])
        except Exception:
            log.warning(f"COMBINER: can't find value for {attribute_name} in {source}")
            # log.warning("COMBINER: can't find value for ", attribute_name, " in ", dict[attr.source_file])

    overlap = string_overlap(strings,min_matching_fraction)

    if overlap != values.insufficient_overlap:
        return (overlap, values.default_date)

    return (values.insufficient_overlap, get_attribute_date(sources[0], file_dicts))


def combine_get_file_url(eu_pnumber: str, attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]]) -> str:
    try:
        for source in sources:
            return file_dicts[src.web][attr.filedates_web][file_dicts[source][attr.pdf_file]]["file_link"]
    except Exception:
        print("COMBINER: failed to get url")
        return values.url_not_found

    return values.url_not_found

def combine_decision_time_days(eu_pnumber: str, attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]]) -> int:
    if attr.chmp_opinion_date not in file_dicts[src.epar].keys():
        return values.invalid_period_days

    try:
        initial_chmp_opinion_date = file_dicts[src.epar][attr.chmp_opinion_date]
        initial_decision_date = get_attribute_date(src.decision_initial, file_dicts)

        initial_chmp_opinion_date = dt.datetime.strptime(initial_chmp_opinion_date, "%Y-%m-%d %H:%M:%S")
        initial_decision_date = dt.datetime.strptime(initial_decision_date, "%Y-%m-%d %H:%M:%S")

        return (initial_decision_date - initial_chmp_opinion_date).days

    except Exception as exception:
        print("COMBINER: failed_combine_decision_time_days -", exception)
        return values.invalid_period_days


def combine_assess_time_days_total(eu_pnumber: str, attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]]) -> int:
    epar_keys = file_dicts[src.epar].keys()
    if attr.chmp_opinion_date not in epar_keys or attr.ema_procedure_start_initial not in epar_keys:
        return values.invalid_period_days

    try:
        initial_chmp_opinion_date = file_dicts[src.epar][attr.chmp_opinion_date]
        initial_procedure_start_date = file_dicts[src.epar][attr.ema_procedure_start_initial]

        initial_chmp_opinion_date = dt.datetime.strptime(initial_chmp_opinion_date, "%Y-%m-%d %H:%M:%S")
        initial_procedure_start_date = dt.datetime.strptime(initial_procedure_start_date, "%Y-%m-%d %H:%M:%S")

        if (initial_chmp_opinion_date - initial_procedure_start_date).days < 0:
            print("COMBINER: negative_combine_assess_time_days_total", (initial_chmp_opinion_date - initial_procedure_start_date).days)

        return (initial_chmp_opinion_date - initial_procedure_start_date).days
    except Exception as exception:
        print("COMBINER: failed_combine_assess_time_days_total -", exception)
        return values.invalid_period_days


def combine_assess_time_days_active(eu_pnumber: str, attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]]) -> int:
    print("annex_10:", eu_pnumber, file_dicts[src.annex_10].keys())
    if eu_pnumber not in file_dicts[src.annex_10].keys():
        return values.invalid_period_days

    return file_dicts[src.annex_10][eu_pnumber][attr.assess_time_days_active]


def combine_assess_time_days_cstop(eu_pnumber: str, attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]]) -> int:
    if eu_pnumber not in file_dicts[src.annex_10].keys():
        return values.invalid_period_days

    return file_dicts[src.annex_10][eu_pnumber][attr.assess_time_days_cstop]


def combine_eu_med_type(eu_pnumber: str, attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]]) -> tuple[str,str]:
    """_summary_

    Args:
        filedicts (dict[str, dict[str, any]]): Dictionary of all source dictionaries generated by combine_folder()

    Returns:
        str: _description_
    """
    annex_initial_dict = file_dicts[src.annex_initial]
    eu_med_type = annex_initial_dict[attr.eu_med_type]
    eu_med_type_date = get_attribute_date(src.annex_initial, file_dicts)
    eu_atmp = file_dicts[src.decision][attr.eu_atmp]

    if eu_med_type == values.eu_med_type_biologicals and eu_atmp:
        return (values.eu_med_type_atmp, eu_med_type_date)

    return (eu_med_type, eu_med_type_date)

def combine_ema_number_check(eu_pnumber: str, attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]]) -> tuple[bool, str]:
    are_equal = False

    web_dict = file_dicts[src.web]
    ema_number_web = web_dict[attr.ema_number]
    if ema_number_web == values.not_found:
        return (are_equal,values.default_date)

    ema_excel = get_ema_excel("..\..\data/ema_excel/", "ema_excel.xlsx")

    if ema_number_web in ema_excel:
        web_brandname = web_dict[attr.eu_brand_name_current]
        excel_brandname = ema_excel[ema_number_web]
        if string_overlap([web_brandname,excel_brandname]) != values.insufficient_overlap:
            are_equal = True


    ema_number_date = get_attribute_date(src.web, file_dicts)

    return(are_equal,ema_number_date)


def json_static(value: any, date: str) -> any:
    return value


def json_history_current(value: any, date: str) -> dict[str, any]:
    json_dict = {}
    json_dict["value"] = value
    json_dict["date"] = date
    return [json_dict]


def json_history_initial(value: any, date: str) -> list[dict[str, any]]:
    json_dict = {}
    json_dict["value"] = value
    json_dict["date"] = date
    return json_dict

def convert_ema_num(ema_number: str) -> str:
    if 'EMEA/H/C/' in ema_number:
        number = ema_number.split('EMEA/H/C/',1)[1]
        return f"EMEA/H/C/{number.lstrip('0')}"
    else:
        return values.not_found
def get_ema_excel(filepath: str, filename: str) -> dict:
    #return pre-made dict if available
    try:
        with open(f"{filepath}/ema_excel.json", "r") as file:  # Use file to refer to the file object
            return json.load(file)
    except Exception:
        pass

    #make dictionary from excel
    try:
        df_number = pd.read_excel(f"{filepath}/{filename}", header=8)
        pnumber_key = 'Product number'
        brandname_key = 'Medicine name'

        # remove non human medicine
        df_number = df_number[df_number['Category'] == 'Human']
        # remove all rows other then product number and medicine name.
        df_number = df_number[[pnumber_key, brandname_key]]
        # remove leading zeros
        df_number[pnumber_key] = df_number.apply(lambda x: convert_ema_num(x[pnumber_key]), axis=1)
        df_number[brandname_key] = df_number.apply(lambda x: x[brandname_key].split('(', 1)[0].strip(), axis=1)

        # remove invalid numbers
        df_number = df_number[df_number[pnumber_key] != values.not_found]

        num_dict = dict(zip(df_number[pnumber_key], df_number[brandname_key]))

        # save dict to json file for quick access.
        with open(f"{filepath}/ema_excel.json", "w") as file:
            json.dump(num_dict, file)
        return num_dict

    #excel not found
    except Exception:
        print(f"COMBINER: {src.ema_excel} not found at {filepath}")
        return {}

# print(get_ema_excel("..\..\data/ema_excel/", "ema_excel.xlsx")['EMEA/H/C/281'])
