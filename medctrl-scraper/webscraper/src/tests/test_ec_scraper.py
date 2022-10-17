import pytest
from .. import ec_scraper as ec


# Unit test that checks whether the correct data is retrieved for a certain medicine.
@pytest.mark.parametrize(
    "eu_num_short, "
    "exp_atc_code, "
    "exp_active_substance, "
    "exp_eu_pnumber, "
    "exp_eu_aut_status, "
    "exp_eu_brand_name_current, "
    "exp_eu_mah_current",
    [
        ("h412",
         "B03XA01",
         "epoetin alfa",
         "EU/1/07/412",
         "ACTIVE",
         "Abseamed",
         "Medice Arzneimittel P&#252;tter GmbH &amp; Co KG"
        ),
        ("h477",
         "L03AX14",
         "Histamine dihydrochloride",
         "EU/1/08/477",
         "ACTIVE",
         "Ceplene",
         "Laboratoires Delbert"
        ),
        ("o1230",
         None,
         "(2R,3R,4S,5R)-2-(6-amino-9H-purin-9-yl)-5-((((1r,3S)-3-(2-(5-(tert-butyl)-1H-benzo[d]imidazol-2-yl)ethyl)cyclobutyl)(isopropyl) amino)methyl)tetrahydrofuran-3,4-diol",
         "EU/3/13/1230",
         "ACTIVE",
         "EU/3/13/1230",
         "Voisin Consulting Life Sciences"
        )
    ]
)
def test_get_data_from_medicine_json(
        eu_num_short,
        exp_atc_code,
        exp_active_substance,
        exp_eu_pnumber,
        exp_eu_aut_status,
        exp_eu_brand_name_current,
        exp_eu_mah_current
):
    html_active = ec.get_ec_html(f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm")
    medicine_json, *_ = ec.get_ec_json_objects(html_active)
    medicine_dict, _ = ec.get_data_from_medicine_json(medicine_json)

    assert medicine_dict["atc_code"] == exp_atc_code
    assert medicine_dict["active_substance"] == exp_active_substance
    assert medicine_dict["eu_pnumber"] == exp_eu_pnumber
    assert medicine_dict["eu_aut_status"] == exp_eu_aut_status
    assert medicine_dict["eu_brand_name_current"] == exp_eu_brand_name_current
    assert medicine_dict["eu_mah_current"] == exp_eu_mah_current


@pytest.mark.parametrize(
    "eu_num_short, "
    "exp_eu_aut_date, "
    "exp_aut_type_initial, "
    "exp_aut_type_current, "
    "exp_ema_number, "
    "exp_ema_number_certainty",
    [
        (
            "h477",
            "07-10-2008",
            "exceptional",
            "",
            "",
            ""
        )
    ]
)
def test_get_data_from_procedures_json(
        eu_num_short,
        exp_eu_aut_date,
        exp_aut_type_initial,
        exp_aut_type_current,
        exp_ema_number,
        exp_ema_number_certainty
):
    html_active = ec.get_ec_html(f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm")
    _, procedures_json, *_ = ec.get_ec_json_objects(html_active)
    procedures_dict, *_ = ec.get_data_from_procedures_json(procedures_json)

    assert procedures_dict["eu_aut_date"] == exp_eu_aut_date
    assert procedures_dict["eu_aut_type_initial"] == exp_aut_type_initial
    # assert procedures_dict["eu_aut_type_current"] = exp_aut_type_current
    # assert procedures_dict["ema_number"] = exp_ema_number
    # assert procedures_dict["ema_number_certainty"] = exp_ema_number_certainty
