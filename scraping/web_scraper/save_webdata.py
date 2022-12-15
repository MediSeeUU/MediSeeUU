from scraping.utilities.web.json_helper import JsonHelper
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.attribute_values as attribute_values
from datetime import datetime
from pathlib import Path
import json


def set_active_refused_webdata(eu_n: str, medicine_url: str, dec_list: list[str], anx_list: list[str],
                               ema_list: list[str], attributes_dict: dict[str, str], data_path: str,
                               url_file: JsonHelper, url_refused_file: JsonHelper):
    """
    Based on whether the medicine is refused or not, it will set the parameters, so that it can be saved to the file
    system correctly.

    Args:
        eu_n (str): EU number of the medicine.
        medicine_url (str): url to a medicine page for a specific medicine.
        dec_list (list[str]): List of urls to decisions on the EC website.
        anx_list (list[str]): List of urls to annexes on the EC website.
        ema_list (list[str]): List of urls to EMA pages on the EC website.
        attributes_dict (dict[str, str]): Dictionary of scraped attributes on the EC website
        data_path (str): The path where the JSON files need to be stored.
        url_file (JsonHelper): the dictionary containing all the urls of a specific medicine
        url_refused_file (JsonHelper): The dictionary containing the urls of all refused files
    """
    # Sets parameter values for active and withdrawn medicines that need to be saved
    if attributes_dict[attr.eu_aut_status] != "REFUSED":
        medicine_identifier: str = eu_n
        target_path: str = f"{data_path}/active_withdrawn/{medicine_identifier}"
        save_webdata_and_urls(medicine_identifier, medicine_url, dec_list, anx_list, ema_list,
                              attributes_dict, url_file, target_path)
    # Sets parameter values for refused medicines that need to be saved
    else:
        # Checks if the medicine is a human or orphan one, and based on that picks the right EMA number
        ema_number_str: str = "ema_number"
        ema_od_number_str: str = "ema_od_number"
        # Based on whether there is an EMA number, sets the medicine identifier to the EMA number or the product name
        if ema_number_str in attributes_dict.keys():
            medicine_identifier: str = "REFUSED-" + attributes_dict[ema_number_str].replace('/', '-')
        elif ema_od_number_str in attributes_dict.keys():
            medicine_identifier: str = "REFUSED-" + attributes_dict[ema_od_number_str].replace('/', '-')
        else:
            medicine_identifier: str = "REFUSED-" + attributes_dict[attr.eu_brand_name_current].replace('/', '-')

        target_path: str = f"{data_path}/refused/{medicine_identifier}"
        save_webdata_and_urls(medicine_identifier, medicine_url, dec_list, anx_list, ema_list,
                              attributes_dict, url_refused_file, target_path)


def save_webdata_and_urls(medicine_identifier: str, medicine_url: str, dec_list: list[str],
                          anx_list: list[str], ema_list: list[str], attributes_dict: dict[str, str],
                          url_file: JsonHelper, target_path: str):
    """
    Saves a webdata JSON file in the correct location, containing scraped attributes from the EC website.
    It also adds urls to the right url JSON file.

    Args:
        medicine_identifier (str): Identifier for a medicine. An EU number for non-refused medicine, EMA number for
            refused medicine
        medicine_url (str): url to a medicine page for a specific medicine.
        dec_list (list[str]): List of urls to decisions on the EC website.
        anx_list (list[str]): List of urls to annexes on the EC website.
        ema_list (list[str]): List of urls to EMA pages on the EC website.
        attributes_dict (dict[str, str]): Dictionary of scraped attributes on the EC website
        url_file (JsonHelper): The url json where all the data needs to be stored.
        target_path (str): Directory where the json needs to be stored.
    """
    # TODO: Common name structure?
    url_json: dict[str, list[str] | str, str] = {
        medicine_identifier: {
            attr.ec_url: medicine_url,
            attr.aut_url: dec_list,
            attr.smpc_url: anx_list,
            attr.ema_url: ema_list,
            attr.scrape_date_web: datetime.strftime(datetime.today(), '%d/%m/%Y'),
            "overwrite_ec_files": "True"
        }
    }

    url_file.add_to_dict(url_json)

    # Creates a directory if the medicine doesn't exist yet,
    # otherwise it just adds the json file to the existing directory
    Path(f"{target_path}").mkdir(exist_ok=True)
    with open(f"{target_path}/{medicine_identifier}_webdata.json", 'w') as f:
        attributes_dict["scrape_date_web"] = datetime.strftime(datetime.today(), '%d/%m/%Y')
        json.dump(attributes_dict, f, indent=4)
