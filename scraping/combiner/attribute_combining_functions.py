import datetime
import json
import logging
import os
from datetime import datetime
from difflib import SequenceMatcher as SM
from typing import Any

import pandas as pd

import scraping.utilities.definitions.attribute_values as attribute_values
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.sources as src

log = logging.getLogger("combiner")
date_str_format = "%Y-%m-%d"


def get_attribute_date(source_string: str, file_dicts: dict[str, dict[str, Any]]) -> datetime | str:
    """
    Gives the scrape or download date of a source file

    Args:
        source_string (str): Name of source of the attribute
        file_dicts (str): All data stored on source location

    Returns:
        datetime | str: Parse date of the source
    """
    if source_string == src.web:
        return file_dicts[src.web][attr.scrape_date_web]
    if file_dicts == {}:
        return attribute_values.date_not_found
    if source_string in file_dicts.keys():
        if file_dicts[source_string] == {}:
            return attribute_values.date_not_found
        if attr.pdf_file not in file_dicts[source_string].keys():
            log.warning(f"\"{attr.pdf_file}\" not in the keys of the source: {source_string}")
            return attribute_values.date_not_found
        file_name = file_dicts[source_string][attr.pdf_file]
        return file_dicts[src.web][attr.filedates_web][file_name][attr.meta_file_date]
    log.warning(f"{source_string} not in the keys of file_dicts")


def get_values_from_sources(attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, Any]]) -> \
        list[Any]:
    """
    Get values from all sources for a given attribute

    Args:
        attribute_name (str): Name of the attribute values to be returned
        sources (list[str]): All sources of the medicine
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes

    Returns:
        list[Any]: Values for the attribute from all sources
    """
    values = []
    for source in sources:
        source_dict = file_dicts[source]
        if attribute_name not in source_dict.keys():
            log.warning(f"COMBINER: can't find value for {attribute_name} in {source}")
            continue
        values.append(file_dicts[source][attribute_name])
    return values


def check_all_equal(values: list[Any]) -> bool:
    """
    Checks if two values are equal and not None
    Args:
        list[Any]: List of values to check

    Returns:
        bool: Whether all values are equal or not
    """
    if len(values) == 0:
        return False

    all_same = True
    for value in values[1:]:
        all_same &= value == values[0]

    return all_same and values[0] is not None


def string_overlap(strings: list[str]) -> tuple[str, bool]:
    """
    Check if strings overlap more than a certain percentage, then return the overlapping part.
    Otherwise, returns first element.

    Args:
        strings (list[str]): Strings to check for overlap

    Returns:
        tuple[str, bool]: First string if strings do not overlap enough, overlapping part if they do
    """
    min_matching_fraction = 0.8

    if len(strings) < 2:
        return strings[0], False

    overlap = SM(None, strings[0].lower(), strings[1].lower()).find_longest_match()
    overlap_fraction = float(overlap.size / len(strings[0]))
    if overlap_fraction >= min_matching_fraction:
        return strings[0][overlap.a:overlap.a + overlap.size], True

    log.info(f"Strings {strings} did not overlap sufficiently, returning first")
    return strings[0], False


def combine_first(file_dicts: dict[str, dict[str, Any]], sources: list[str], attribute_name: str, **_) -> Any:
    """
    Gives value from first source for attribute_name

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes
        sources (list[str]): Potential sources of the attribute
        attribute_name (str): Name of attribute to add

    Returns:
        Any: Value from first source that is available
    """
    attributes = get_values_from_sources(attribute_name, sources, file_dicts)
    attributes.append(attribute_values.not_found)
    return attributes[0]


def combine_eu_aut_status(file_dicts: dict[str, dict[str, Any]], attribute_name: str, sources: list[str], **_)\
        -> list[dict]:
    """
    Gives value and its scrape date from first source for attribute_name

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes
        attribute_name (str): Name of attribute to add
        sources (list[str]): Potential sources of the attribute

    Returns:
        list[dict]: List of dictionary of value and date from first source that is available
    """
    attributes = get_values_from_sources(attribute_name, sources, file_dicts)
    attributes.append(attribute_values.not_found)
    json_dict = {"value": attributes[0], "date": get_attribute_date(sources[0], file_dicts)}
    return [json_dict]


def combine_string_overlap(file_dicts: dict[str, dict[str, Any]], sources: list[str], attribute_name: str, **_) -> str:
    """
    Gives overlapping part of values for attribute_name from all sources, if overlap is insufficient, gives the value
    from first source in sources.

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes
        sources (list[str]): Potential sources of the attribute
        attribute_name (str): Name of attribute to add

    Returns:
        str: Overlapping part of strings or the value from the first source
    """
    strings = get_values_from_sources(attribute_name, sources, file_dicts)
    res, _ = string_overlap(strings)
    return res


def combine_get_file_url(file_dicts: dict[str, dict[str, Any]], sources: list[str], **_) -> str:
    """
    Gives the URL of the medicine from source in sources

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes
        sources (list[str]): Potential sources of the attribute

    Returns:
        str: Found URL for the given medicine or url_not_found string
    """
    for source in sources:
        if source not in file_dicts.keys():
            continue
        if attr.pdf_file not in file_dicts[source].keys():
            continue
        return file_dicts[src.web][attr.filedates_web][file_dicts[source][attr.pdf_file]]["pdf_link"]
    log.info(f"COMBINER: failed to get url, sources are {sources}")

    return attribute_values.url_not_found


def combine_decision_time_days(file_dicts: dict[str, dict[str, Any]], **_) -> int | str:
    """
    Gives amount of days between decision time and initial procedure start date

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes

    Returns:
        int | str: Days between initial_decision_date and initial_procedure_date if available, else not_found_str
    """
    if attr.chmp_opinion_date not in file_dicts[src.epar].keys():
        return attribute_values.not_found_str

    initial_decision_date = get_attribute_date(src.dec_initial, file_dicts)
    initial_chmp_opinion_date = file_dicts[src.epar][attr.chmp_opinion_date]
    if initial_decision_date != attribute_values.date_not_found and \
            initial_chmp_opinion_date != attribute_values.date_not_found:
        initial_decision_date = datetime.strptime(initial_decision_date, date_str_format)
        initial_procedure_start_date = datetime.strptime(initial_chmp_opinion_date, date_str_format)
        return (initial_decision_date - initial_procedure_start_date).days

    return attribute_values.not_found_str


def combine_assess_time_days_total(file_dicts: dict[str, dict[str, Any]], **_) -> int | str:
    """
    Gives amount of days between CHMP opinion date and initial procedure start date

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes

    Returns:
        int | str: Days between initial_chmp_opinion_date and initial_procedure_start_date if available,
        else not_found_str
    """
    epar_keys = file_dicts[src.epar].keys()
    if attr.chmp_opinion_date not in epar_keys or attr.ema_procedure_start_initial not in epar_keys:
        return attribute_values.not_found_str

    initial_chmp_opinion_date = file_dicts[src.epar][attr.chmp_opinion_date]
    initial_procedure_start_date = file_dicts[src.epar][attr.ema_procedure_start_initial]
    if initial_chmp_opinion_date != attribute_values.date_not_found and \
            initial_procedure_start_date != attribute_values.date_not_found:
        initial_chmp_opinion_date = datetime.strptime(initial_chmp_opinion_date, date_str_format)
        initial_procedure_start_date = datetime.strptime(initial_procedure_start_date, date_str_format)
        return (initial_chmp_opinion_date - initial_procedure_start_date).days
    return attribute_values.not_found_str


def combine_assess_time_days_active(eu_pnumber: str, file_dicts: dict[str, dict[str, Any]], **_) -> int | str:
    """
    Gives the assessment time days active from the latest annex 10 file

    Args:
        eu_pnumber (str): EU number of medicine
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes

    Returns:
        int | str: Value of assess_time_days_active, else not_found_str
    """
    annex_10_keys = reversed(sorted(file_dicts[src.annex_10].keys()))

    for year_key in annex_10_keys:
        if eu_pnumber not in file_dicts[src.annex_10][year_key].keys():
            continue

        return file_dicts[src.annex_10][year_key][eu_pnumber][attr.assess_time_days_active]
    return attribute_values.not_found_str


def combine_assess_time_days_cstop(eu_pnumber: str, file_dicts: dict[str, dict[str, Any]], **_) -> int | str:
    """
    Gives the assessment time day cstop from the latest annex 10 file

    Args:
        eu_pnumber (str): EU number of medicine
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes

    Returns:
        int | str: Value of combine_assess_time_days_cstop, else not_found_str
    """
    annex_10_keys = reversed(sorted(file_dicts[src.annex_10].keys()))

    for year_key in annex_10_keys:
        if eu_pnumber not in file_dicts[src.annex_10][year_key].keys():
            continue

        return file_dicts[src.annex_10][year_key][eu_pnumber][attr.assess_time_days_cstop]
    return attribute_values.not_found_str


def combine_eu_med_type(file_dicts: dict[str, dict[str, Any]], eu_pnumber: str, **_) -> tuple[str, str]:
    """
    Gives the value for eu_med_type from the initial annex file, one of ["biologicals", "ATMP", "small molecule"]

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes
        eu_pnumber (str): EU number of medicine

    Returns:
        tuple[str, str]: Value from initial annex file for eu_med_type ["biologicals", "ATMP", "small molecule"]
    """
    annex_initial_dict = file_dicts[src.anx_initial]
    if annex_initial_dict == {}:
        log.warning(f"COMBINER: no annex initial in {eu_pnumber}")
        return attribute_values.not_found
    if attr.eu_med_type not in annex_initial_dict.keys():
        return attribute_values.not_found
    eu_med_type = annex_initial_dict[attr.eu_med_type]
    eu_atmp = file_dicts[src.decision][attr.eu_atmp]

    if eu_med_type == attribute_values.eu_med_type_biologicals and eu_atmp:
        return attribute_values.eu_med_type_atmp

    return eu_med_type


def combine_ema_number_check(file_dicts: dict[str, dict[str, Any]], **_) -> bool:
    """
    Checks whether brand name overlaps significantly between webdata and ema_excel file

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes

    Returns:
        bool: Whether brand name overlaps significantly between webdata and ema_excel file
    """
    are_equal = False

    web_dict = file_dicts[src.web]
    if attr.ema_number not in web_dict.keys():
        return are_equal
    ema_number_web = web_dict[attr.ema_number]
    if ema_number_web == attribute_values.not_found:
        return are_equal

    ema_excel_path = "../data/ema_excel/", "ema_excel.xlsx"
    if not os.path.exists(os.path.join(ema_excel_path[0], ema_excel_path[1])):
        log.warning(f"ema_excel_path {ema_excel_path} does not exist")
        return are_equal
    ema_excel = get_ema_excel(ema_excel_path[0], ema_excel_path[1])

    if ema_number_web in ema_excel:
        web_brand_name = web_dict[attr.eu_brand_name_current]
        excel_brand_name = ema_excel[ema_number_web]
        _, are_equal = string_overlap([web_brand_name, excel_brand_name])
    return are_equal


def combine_eu_procedures_todo(file_dicts: dict[str, dict[str, Any]], **_) -> Any:
    """
    Gives referral and suspension as booleans, depending on their string boolean value in webdata

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes

    Returns:
        Any: Dict of referral and suspension booleans
    """
    return [{attr.eu_referral: file_dicts[src.web][attr.eu_referral] == "True",
             attr.eu_suspension: file_dicts[src.web][attr.eu_suspension] == "True"}]


def combine_date(file_dicts: dict[str, dict[str, Any]], sources: list[str], attribute_name: str, **_) -> datetime.date:
    """
    Gives the date from the first source.

    Args:
        file_dicts (dict[str, dict[str, Any]]): Dictionary with sources as keys, and data of sources as attributes
        sources (list[str]): Potential sources of the attribute
        attribute_name (str): Name of attribute to add

    Returns:
        datetime.date: Value from first source that is available, date_not_found if no source is available
    """
    values = get_values_from_sources(attribute_name, sources, file_dicts)

    if not check_all_equal(values):
        log.warning(f"COMBINER: crosscheck for {attribute_name} failed")

    values.append(attribute_values.date_not_found)
    return values[0]


def json_static(value: Any, **_) -> Any:
    """
    Saves only the value of an attribute

    Args:
        value (Any): Value of some attribute

    Returns:
        (Any): Value of some attribute
    """
    return value


def json_initial(value: Any, date: Any) -> dict[str, str | Any]:
    """
    Saves both value and scrape date of an attribute as a dictionary

    Args:
        value (Any): Value of some attribute
        date (Any): Scrape date of some attribute

    Returns:
        (dict[str, str | Any]): Dictionary of value and its scrape date
    """
    if date == attribute_values.date_not_found:
        date = attribute_values.default_date
    json_dict = {"value": value, "date": date}
    return json_dict


def json_current(value: Any, date: Any) -> list[dict[str, str | Any]]:
    """
    Saves both value and scrape date of an attribute as a list of a dictionary

    Args:
        value (Any): Value of some attribute
        date (Any): Scrape date of some attribute

    Returns:
        (list[dict[str, str | Any]]): Dictionary of value and its scrape date, in a list
    """
    if date == attribute_values.date_not_found:
        date = attribute_values.default_date
    json_dict = {"value": value, "date": date}
    return [json_dict]


def convert_ema_num(ema_number: str) -> str:
    """
    Converts EMA number to right format: removes leading 0's from the digits of the EMA number

    Args:
        ema_number (str): Original EMA number

    Returns:
        str: Converted EMA number or not_found string
    """
    if 'EMEA/H/C/' in ema_number:
        number = ema_number.split('EMEA/H/C/', 1)[1]
        return f"EMEA/H/C/{number.lstrip('0')}"
    else:
        return attribute_values.not_found


def get_ema_excel(filepath: str, filename: str) -> dict:
    """
    Gives cleaned dictionary of EMA Excel file after saving the cleaned version to its original location

    Args:
        filepath (str): Path of EMA Excel file containing folder
        filename (str): Name of EMA Excel file

    Returns:
        dict: Cleaned dictionary of EMA Excel file
    """
    # return pre-made dict if available
    if os.path.exists(f"{filepath}/ema_excel.json"):
        with open(f"{filepath}/ema_excel.json", "r") as file:
            return json.load(file)

    # make dictionary from excel
    df_number = pd.read_excel(f"{filepath}/{filename}", header=8)
    pnumber_key = 'Product number'
    brand_name_key = 'Medicine name'

    # remove non-human medicine
    df_number = df_number[df_number['Category'] == 'Human']
    # remove all rows other than product number and medicine name.
    df_number = df_number[[pnumber_key, brand_name_key]]
    # remove leading zeros
    df_number[pnumber_key] = df_number.apply(lambda x: convert_ema_num(x[pnumber_key]), axis=1)
    df_number[brand_name_key] = df_number.apply(lambda x: x[brand_name_key].split('(', 1)[0].strip(), axis=1)

    # remove invalid numbers
    df_number = df_number[df_number[pnumber_key] != attribute_values.not_found]

    num_dict = dict(zip(df_number[pnumber_key], df_number[brand_name_key]))

    # save dict to json file for quick access.
    with open(f"{filepath}/ema_excel.json", "w") as file:
        json.dump(num_dict, file)
    return num_dict
