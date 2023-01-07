import datetime
import json
import logging
from datetime import datetime
from difflib import SequenceMatcher as SM
from typing import Any

import pandas as pd

import scraping.utilities.definitions.attribute_values as attribute_values
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.sources as src

log = logging.getLogger("combiner")


def get_attribute_date(source_string: str, file_dicts: dict[str, dict[str, any]]) -> datetime | None:
    """
    Gives the scrape or download date of a source file

    Args:
        source_string (str): Name of source of the attribute
        file_dicts (str): All data stored on source location

    Returns:
        datetime: Parse date of the source
    """
    if source_string == src.web:
        return file_dicts[src.web][attr.scrape_date_web]
    if file_dicts == {}:
        return
    if source_string in file_dicts.keys():
        if file_dicts[source_string] == {} or "annex10" in str(file_dicts[source_string].keys()):
            return
        if attr.pdf_file not in file_dicts[source_string].keys():
            log.warning(f"\"{attr.pdf_file}\" not in the keys of the source: {source_string}")
            return
        file_name = file_dicts[source_string][attr.pdf_file]
        return file_dicts[src.web][attr.filedates_web][file_name][attr.meta_file_date]
    log.warning(f"{source_string} not in the keys of file_dicts")


def get_values_from_sources(attribute_name: str, sources: list[str], file_dicts: dict[str, dict[str, any]]) -> \
        list[any]:
    """
    Get values from all sources for a given attribute

    Args:
        attribute_name (str): Name of the attribute values to be returned
        sources (list[str]): All sources of the medicine
        file_dicts (dict[str, dict[str, any]]): Dictionary with sources as keys, and data of sources as attributes

    Returns:
        list[any]: Values for the attribute from all sources
    """
    values = []
    for source in sources:
        source_dict = file_dicts[source]
        if attribute_name not in source_dict.keys():
            log.warning(f"COMBINER: can't find value for {attribute_name} in {source}")
            continue
        values.append(attribute_name)
    return values


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


def combine_first(eu_pnumber: str, attribute_name: str, sources: list[str],
                  file_dicts: dict[str, dict[str, any]]) -> any:
    """

    Args:
        attribute_name:
        dicts:
        combine_attributes:

    Returns:

    """
    attributes = get_values_from_sources(attribute_name, sources, file_dicts)
    attributes.append(attribute_values.not_found)
    return attributes[0]


def combine_eu_aut_status(eu_pnumber: str, attribute_name: str, sources: list[str],
                        file_dicts: dict[str, dict[str, any]]) -> any:
    """

    Args:
        attribute_name:
        dicts:
        combine_attributes:

    Returns:

    """
    attributes = get_values_from_sources(attribute_name, sources, file_dicts)
    attributes.append(attribute_values.not_found)
    json_dict = {"value": attributes[0], "date": get_attribute_date(sources[0], file_dicts)}
    return [json_dict]


def string_overlap(strings: list[str], min_matching_fraction: float = 0.8) -> str:
    if len(strings) >= 2:
        overlap = SM(None, strings[0].lower(), strings[1].lower()).find_longest_match()
        if float(overlap.size / len(strings[0])) >= min_matching_fraction:
            return strings[0][overlap.a:overlap.a + overlap.size]

    return strings[0]  # TODO: log check failed


# For combine functions
# TODO: fix datum
def combine_string_overlap(eu_pnumber: str, attribute_name: str, sources: list[str],
                           file_dicts: dict[str, dict[str, any]],
                           min_matching_fraction: float = 0.8) -> str:
    """
    compares two strings to see if a percentage of the shortest string is identical to the longest string
    Args:
        s1 (str): first string
        s2 (str): second string
        perc (float): percentage float between 0 and 1

    Returns (bool): bool indicating equality
    """
    strings = get_values_from_sources(attribute_name, sources, file_dicts)

    if strings:
        overlap = string_overlap(strings, min_matching_fraction)

        if overlap != attribute_values.insufficient_overlap:
            return overlap

    log.info(f"Insufficient overlap for {strings}")
    return strings[0]


def combine_get_file_url(eu_pnumber: str, attribute_name: str, sources: list[str],
                         file_dicts: dict[str, dict[str, any]]) -> str:
    try:
        for source in sources:
            return file_dicts[src.web][attr.filedates_web][file_dicts[source][attr.pdf_file]]["pdf_link"]
    except Exception as exception:
        log.info(f"COMBINER: failed to get url, key is {exception}")

    return attribute_values.url_not_found


def combine_decision_time_days(eu_pnumber: str, attribute_name: str, sources: list[str],
                               file_dicts: dict[str, dict[str, any]]) -> int:
    if attr.chmp_opinion_date not in file_dicts[src.epar].keys():
        return attribute_values.not_found_str

    try:
        initial_chmp_opinion_date = file_dicts[src.epar][attr.chmp_opinion_date]
        initial_chmp_opinion_date = datetime.datetime.strptime(initial_chmp_opinion_date, "%Y-%m-%d")
        initial_decision_date = get_attribute_date(src.dec_initial, file_dicts)
        if isinstance(initial_decision_date, str) and initial_decision_date != attribute_values.not_found:
            initial_decision_date = datetime.datetime.strptime(initial_decision_date, "%Y-%m-%d")

        return (initial_decision_date - initial_chmp_opinion_date).days

    except Exception as exception:
        log.info(f"COMBINER: failed_combine_decision_time_days - {exception}")

        return attribute_values.not_found_str


def combine_assess_time_days_total(eu_pnumber: str, attribute_name: str, sources: list[str],
                                   file_dicts: dict[str, dict[str, any]]) -> int:
    epar_keys = file_dicts[src.epar].keys()
    if attr.chmp_opinion_date not in epar_keys or attr.ema_procedure_start_initial not in epar_keys:
        return attribute_values.not_found_str

    try:
        initial_chmp_opinion_date = file_dicts[src.epar][attr.chmp_opinion_date]
        initial_procedure_start_date = file_dicts[src.epar][attr.ema_procedure_start_initial]

        initial_chmp_opinion_date = datetime.datetime.strptime(initial_chmp_opinion_date, "%Y-%m-%d")
        initial_procedure_start_date = datetime.datetime.strptime(initial_procedure_start_date, "%Y-%m-%d")
        return (initial_chmp_opinion_date - initial_procedure_start_date).days
    except Exception as exception:
        log.info(f"COMBINER: failed_combine_assess_time_days_total - {exception}")
        return attribute_values.not_found_str


def combine_assess_time_days_active(eu_pnumber: str, attribute_name: str, sources: list[str],
                                    file_dicts: dict[str, dict[str, any]]) -> int:
    try:
        annex_10_keys = reversed(sorted(file_dicts[src.annex_10].keys()))

        for year_key in annex_10_keys:
            if eu_pnumber not in file_dicts[src.annex_10][year_key].keys():
                continue

            return file_dicts[src.annex_10][year_key][eu_pnumber][attr.assess_time_days_active]
    except Exception:
        pass
    return attribute_values.not_found_str


def combine_assess_time_days_cstop(eu_pnumber: str, attribute_name: str, sources: list[str],
                                   file_dicts: dict[str, dict[str, any]]) -> int:
    try:
        annex_10_keys = reversed(sorted(file_dicts[src.annex_10].keys()))

        for year_key in annex_10_keys:
            if eu_pnumber not in file_dicts[src.annex_10][year_key].keys():
                continue

            return file_dicts[src.annex_10][year_key][eu_pnumber][attr.assess_time_days_cstop]

    except Exception:
        pass
    return attribute_values.not_found_str


def combine_eu_med_type(eu_pnumber: str, attribute_name: str, sources: list[str],
                        file_dicts: dict[str, dict[str, any]]) -> tuple[str, str]:
    """

    Args:
        filedicts(dict[str, dict[str, any]]): Dictionary of all source dictionaries generated by combine_folder()

    Returns:
        str: _description_
    """
    try:  # TODO: this try except should not be necisarry if sources are always {} when not found
        annex_initial_dict = file_dicts[src.anx_initial]
        if annex_initial_dict == {}:
            log.warning(f"COMBINER: no annex initial in {eu_pnumber}")
            return attribute_values.not_found
        eu_med_type = annex_initial_dict[attr.eu_med_type]
        eu_atmp = file_dicts[src.decision][attr.eu_atmp]

        if eu_med_type == attribute_values.eu_med_type_biologicals and eu_atmp:
            return attribute_values.eu_med_type_atmp
    except:
        return attribute_values.not_found

    return eu_med_type


def combine_ema_number_check(eu_pnumber: str, attribute_name: str, sources: list[str],
                             file_dicts: dict[str, dict[str, any]]) -> bool:
    try:
        are_equal = False

        web_dict = file_dicts[src.web]
        ema_number_web = web_dict[attr.ema_number]
        if ema_number_web == attribute_values.not_found:
            return are_equal

        ema_excel = get_ema_excel("../data/ema_excel/", "ema_excel.xlsx")  # TODO: not hardcoding path

        if ema_number_web in ema_excel:
            web_brand_name = web_dict[attr.eu_brand_name_current]
            excel_brand_name = ema_excel[ema_number_web]
            if string_overlap([web_brand_name, excel_brand_name]) != attribute_values.insufficient_overlap:
                are_equal = True
        return are_equal
    except Exception:
        return False


def combine_eu_procedures_todo(eu_pnumber: str, attribute_name: str, sources: list[str],
                               file_dicts: dict[str, dict[str, any]]) -> list[dict[str, bool]]:
    return [{attr.eu_referral: file_dicts[src.web][attr.eu_referral] == "True",
             attr.eu_suspension: file_dicts[src.web][attr.eu_suspension] == "True"}]


def combine_date(eu_pnumber: str, attribute_name: str, sources: list[str],
                 file_dicts: dict[str, dict[str, any]]) -> datetime.date:
    values = get_values_from_sources(attribute_name, sources, file_dicts)

    if not check_all_equal(values):
        log.warning(f"COMBINER: crosscheck for {attribute_name} failed")

    values.append(attribute_values.date_not_found)
    return values[0]


def json_static(value: any, _) -> any:
    return value


def json_initial(value: any, date: str) -> dict[str, str | Any]:
    json_dict = {"value": value, "date": date}
    return json_dict


def json_current(value: any, date: str) -> list[dict[str, str | Any]]:
    json_dict = {"value": value, "date": date}
    return [json_dict]


def convert_ema_num(ema_number: str) -> str:
    if 'EMEA/H/C/' in ema_number:
        number = ema_number.split('EMEA/H/C/', 1)[1]
        return f"EMEA/H/C/{number.lstrip('0')}"
    else:
        return attribute_values.not_found


def get_ema_excel(filepath: str, filename: str) -> dict:
    # return pre-made dict if available
    try:
        with open(f"{filepath}/ema_excel.json", "r") as file:  # Use file to refer to the file object
            return json.load(file)
    except Exception:
        pass

    # make dictionary from excel
    try:
        df_number = pd.read_excel(f"{filepath}/{filename}", header=8)
        pnumber_key = 'Product number'
        brand_name_key = 'Medicine name'

        # remove non human medicine
        df_number = df_number[df_number['Category'] == 'Human']
        # remove all rows other then product number and medicine name.
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

    # excel not found
    except Exception:
        log.info(f"COMBINER: {src.ema_excel} not found at {filepath}")
        return {}
