# TODO: remove this import when merging with combiner
# import scraping.combiner.attribute_combining_functions as acf

# All sources :D
decision = "dec"
decision_initial = "dec_initial"
annex = "anx"
annex_initial = "anx_initial"
epar = "epar"
omar = "omar"
web = "web"
file_dates = "filedates"


class ScraperAttribute:
    """
    struct class for attributes
    """

    def __init__(self, name: str, sources: list[str], combine):
        self.name = name
        self.sources = sources
        self.combine = combine


def attribute_factory(all_attributes: dict[str, ScraperAttribute], name: str, sources: list[str], combine=False) -> str:
    """
    add new ScraperAttribute to all_attributes and return name of ScraperAttribute
    Args:
        all_attributes (dict[str, ScraperAttribute]): Dictionary of all attribute names, combined with this name as
            string and a list of sources for that attribute
        name (str): Name of ScraperAttribute
        sources (list[str]): List of sources for ScraperAttribute
        combine (bool): Whether to cross-check attributes from different sources

    Returns:
        str: Name of the attribute
    """
    attr = ScraperAttribute(name, sources, combine)
    all_attributes[name] = attr
    return name


# Initialize all attribute objects
all_attributes = {}
atc_code = attribute_factory(all_attributes, "atc_code", [web])
# atc_name_l1 = attribute_factory(all_attributes, "atc_name_l1", [web])
# atc_name_l2 = attribute_factory(all_attributes, "atc_name_l2", [web])
# atc_name_l3 = attribute_factory(all_attributes, "atc_name_l3", [web])
# atc_name_l4 = attribute_factory(all_attributes, "atc_name_l4", [web])
active_substance = attribute_factory(all_attributes, "active_substance", [web, decision_initial])
eu_nas = attribute_factory(all_attributes, "eu_nas", [decision_initial])
ema_procedure_start_initial = attribute_factory(all_attributes, "ema_procedure_start_initial", [epar])
chmp_opinion_date = attribute_factory(all_attributes, "chmp_opinion_date", [epar])
eu_aut_date = attribute_factory(all_attributes, "eu_aut_date", [web, decision_initial])
eu_aut_type_initial = attribute_factory(all_attributes, "eu_aut_type_initial", [decision_initial, annex_initial, web])
eu_aut_type_current = attribute_factory(all_attributes, "eu_aut_type_current", [web])
eu_brand_name_initial = attribute_factory(all_attributes, "eu_brand_name_initial", [decision_initial])
eu_pnumber = attribute_factory(all_attributes, "eu_pnumber", [web])
eu_pnumber_id = attribute_factory(all_attributes, "eu_pnumber_id", [web])
eu_legal_basis = attribute_factory(all_attributes, "eu_legal_basis", [epar])
aut_url = attribute_factory(all_attributes, "aut_url", [file_dates])
smpc_url = attribute_factory(all_attributes, "smpc_url", [file_dates])
epar_url = attribute_factory(all_attributes, "epar_url", [file_dates])
eu_atmp = attribute_factory(all_attributes, "eu_atmp", [decision])
eu_med_type = attribute_factory(all_attributes, "eu_med_type", [annex_initial])
eu_aut_status = attribute_factory(all_attributes, "eu_aut_status", [web])  # niet web web pls
eu_brand_name = attribute_factory(all_attributes, "eu_brand_name", [web])
eu_brand_name_current = attribute_factory(all_attributes, "eu_brand_name_current", [web])
eu_brand_name_history = attribute_factory(all_attributes, "eu_brand_name_history", [web])
ema_number = attribute_factory(all_attributes, "ema_number", [web])
ema_number_id = attribute_factory(all_attributes, "ema_number_id", [web])
ema_number_certainty = attribute_factory(all_attributes, "ema_number_certainty", [web])
ema_number_check = attribute_factory(all_attributes, "ema_number_check", [web])
# eu_mah = attribute_factory(all_attributes, "eu_mah", )
eu_mah_current = attribute_factory(all_attributes, "eu_mah_current", [web])
eu_mah_initial = attribute_factory(all_attributes, "eu_mah_initial", [decision_initial])
eu_mah_history = attribute_factory(all_attributes, "eu_mah_history", [web])
eu_prime_initial = attribute_factory(all_attributes, "eu_prime_initial", [epar])
eu_prime_history = attribute_factory(all_attributes, "eu_prime_history", [epar])
eu_od_initial = attribute_factory(all_attributes, "eu_od_initial", [decision_initial])
eu_od_history = attribute_factory(all_attributes, "eu_od_history", [decision])  # ?
ema_url = attribute_factory(all_attributes, "ema_url", [file_dates])
ec_url = attribute_factory(all_attributes, "ec_url", [file_dates])
ema_rapp = attribute_factory(all_attributes, "ema_rapp", [epar])
ema_corapp = attribute_factory(all_attributes, "ema_corapp", [epar])
eu_accel_assess_g = attribute_factory(all_attributes, "eu_accel_assess_g", [epar])
eu_accel_assess_m = attribute_factory(all_attributes, "eu_accel_assess_m", [epar])
# assess_time_days_total = attribute_factory(all_attributes, "assess_time_days_total", )
# assess_time_days_active = attribute_factory(all_attributes, "assess_time_days_active", )
# assess_time_days_cstop = attribute_factory(all_attributes, "assess_time_days_cstop", )
# ec_sources.decision_time_days = attribute_factory(all_attributes, "ec_sources.decision_time_days", )
ema_reexamination = attribute_factory(all_attributes, "ema_reexamination", [epar])
eu_orphan_con_initial = attribute_factory(all_attributes, "eu_orphan_con_initial", [web])
eu_orphan_con_current = attribute_factory(all_attributes, "eu_orphan_con_current", [web])
eu_referral = attribute_factory(all_attributes, "eu_referral", [web])
eu_suspension = attribute_factory(all_attributes, "eu_suspension", [web])
omar_url = attribute_factory(all_attributes, "omar_url", [file_dates])
odwar_url = attribute_factory(all_attributes, "odwar_url", [file_dates])
eu_od_number = attribute_factory(all_attributes, "eu_od_number", [web])
ema_od_number = attribute_factory(all_attributes, "ema_od_number", [web])
eu_od_con = attribute_factory(all_attributes, "eu_od_con", [web])
eu_od_date = attribute_factory(all_attributes, "eu_od_date", [file_dates])
eu_od_pnumber = attribute_factory(all_attributes, "eu_od_pnumber", [web])
eu_od_sponsor = attribute_factory(all_attributes, "eu_od_sponsor", [web])
eu_od_comp_date = attribute_factory(all_attributes, "eu_od_comp_date", [file_dates])

#TODO: checks for the following new attrs
eu_therapeutic_indications = attribute_factory(all_attributes, "eu_therapeutic_indications", [])
active_time_elapsed = attribute_factory(all_attributes, "active_time_elapsed", [])
clock_stop_elapsed = attribute_factory(all_attributes, "clock_stop_elapsed", [])