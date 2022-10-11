import pytest
from .. import ec_scraper as ec

# Unit test that checks whether the correct data is retrieved for a certain medicine.
# It only checks one medicine for now
@pytest.mark.parametrize("url, exp_atc_code, exp_active_substance, exp_eu_pnumber, exp_eu_aut_status, exp_eu_brand_name_current, exp_eu_mah_current, exp_ema_url_list",[
    ("h412", "B03XA01", "epoetin alfa", "EU/1/07/412", "ACTIVE", "Abseamed", "Medice Arzneimittel P&#252;tter GmbH &amp; Co KG", [])
])
def test_get_data_from_medicine_json(url, exp_atc_code, exp_active_substance, exp_eu_pnumber, exp_eu_aut_status, exp_eu_brand_name_current, exp_eu_mah_current, exp_ema_url_list):
    # In order to test this function, first the right JSON object needs to be retrieved
    medicine_json, _ = ec.get_ec_json_objects(ec.get_ec_html(url))
    ema_url_list: list[str] = []

    atc_code, active_substance, eu_pnumber, eu_aut_status, eu_brand_name_current, eu_mah_current, ema_url_list = ec.get_data_from_medicine_json(medicine_json, ema_url_list)

    assert atc_code == exp_atc_code
    assert active_substance == exp_active_substance
    assert eu_pnumber == exp_eu_pnumber
    assert eu_aut_status == exp_eu_aut_status
    assert eu_brand_name_current == exp_eu_brand_name_current
    assert eu_mah_current == exp_eu_mah_current
    # assert ema_url_list == exp_ema_url_list


