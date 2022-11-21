import scraping.combiner.attribute_combining_functions as acf

# All sources :D
decision = "dec"
decision_initial = "dec_initial"
annex = "anx"
annex_initial = "anx_initial"
epar = "epar"
omar = "omar"
web = "web"
file_dates = "filedates"


# struct class
class ScraperAttribute:
    def __init__(self, name: str, sources: list[str], combine):
        self.name = name
        self.sources = sources
        self.combine = combine


# add new ScraperAttribute to all_attributes and return name of ScraperAttribute
def AttributeFactory(all_attributes: dict[str, ScraperAttribute], name: str, sources: list[str], combine=False):
    attr = ScraperAttribute(name, sources, combine)
    all_attributes[name] = attr
    return name

# Initialize all attribute objects
all_attributes = {}
atc_code = AttributeFactory(all_attributes, "atc_code", [web])
atc_name_l1 = AttributeFactory(all_attributes, "atc_name_l1", [web])
atc_name_l2 = AttributeFactory(all_attributes, "atc_name_l2", [web])
atc_name_l3 = AttributeFactory(all_attributes, "atc_name_l3", [web])
atc_name_l4 = AttributeFactory(all_attributes, "atc_name_l4", [web])
active_substance = AttributeFactory(all_attributes, "active_substance", [web, decision_initial])
eu_nas = AttributeFactory(all_attributes, "eu_nas", [decision_initial])
ema_procedure_start_initial = AttributeFactory(all_attributes, "ema_procedure_start_initial", [epar])
chmp_opinion_date = AttributeFactory(all_attributes, "chmp_opinion_date", [epar])
eu_aut_date = AttributeFactory(all_attributes, "eu_aut_date", [web, decision_initial])
eu_aut_type_initial = AttributeFactory(all_attributes, "eu_aut_type_initial", [decision_initial, annex_initial, web])
eu_aut_type_current = AttributeFactory(all_attributes, "eu_aut_type_current", [web])
eu_brand_name_initial = AttributeFactory(all_attributes, "eu_brand_name_initial", [decision_initial])
eu_pnumber = AttributeFactory(all_attributes, "eu_pnumber", [web])
eu_pnumber_id = AttributeFactory(all_attributes, "eu_pnumber_id", [web])
eu_legal_basis = AttributeFactory(all_attributes, "eu_legal_basis", [epar])
aut_url = AttributeFactory(all_attributes, "aut_url", [file_dates])
smpc_url = AttributeFactory(all_attributes, "smpc_url", [file_dates])
epar_url = AttributeFactory(all_attributes, "epar_url", [file_dates])
eu_atmp = AttributeFactory(all_attributes, "eu_atmp", [decision])
eu_med_type = AttributeFactory(all_attributes, "eu_med_type", [annex_initial])
eu_aut_status = AttributeFactory(all_attributes, "eu_aut_status", [web])  # niet web web pls
eu_brand_name = AttributeFactory(all_attributes, "eu_brand_name", [web])
eu_brand_name_current = AttributeFactory(all_attributes, "eu_brand_name_current", [web])
eu_brand_name_history = AttributeFactory(all_attributes, "eu_brand_name_history", [web])
ema_number = AttributeFactory(all_attributes, "ema_number", [web])
ema_number_id = AttributeFactory(all_attributes, "ema_number_id", [web])
ema_number_certainty = AttributeFactory(all_attributes, "ema_number_certainty", [web])
ema_number_check = AttributeFactory(all_attributes, "ema_number_check", [web])
eu_mah = AttributeFactory(all_attributes, "eu_mah", )
eu_mah_current = AttributeFactory(all_attributes, "eu_mah_current", [web])
eu_mah_initial = AttributeFactory(all_attributes, "eu_mah_initial", [decision_initial])
eu_mah_history = AttributeFactory(all_attributes, "eu_mah_history", [web])
eu_prime_initial = AttributeFactory(all_attributes, "eu_prime_initial", [epar])
eu_prime_history = AttributeFactory(all_attributes, "eu_prime_history", [epar])
eu_od_initial = AttributeFactory(all_attributes, "eu_od_initial", [decision_initial])
eu_od_history = AttributeFactory(all_attributes, "eu_od_history", [decision])  # ?
ema_url = AttributeFactory(all_attributes, "ema_url", [file_dates])
ec_url = AttributeFactory(all_attributes, "ec_url", [file_dates])
ema_rapp = AttributeFactory(all_attributes, "ema_rapp", [epar])
ema_corapp = AttributeFactory(all_attributes, "ema_corapp", [epar])
eu_accel_assess_g = AttributeFactory(all_attributes, "eu_accel_assess_g", [epar])
eu_accel_assess_m = AttributeFactory(all_attributes, "eu_accel_assess_m", [epar])
assess_time_days_total = AttributeFactory(all_attributes, "assess_time_days_total", )
assess_time_days_active = AttributeFactory(all_attributes, "assess_time_days_active", )
assess_time_days_cstop = AttributeFactory(all_attributes, "assess_time_days_cstop", )
ec_sources.decision_time_days = AttributeFactory(all_attributes, "ec_sources.decision_time_days", )
ema_reexamination = AttributeFactory(all_attributes, "ema_reexamination", [epar])
eu_orphan_con_initial = AttributeFactory(all_attributes, "eu_orphan_con_initial", [web])
eu_orphan_con_current = AttributeFactory(all_attributes, "eu_orphan_con_current", [web])
eu_referral = AttributeFactory(all_attributes, "eu_referral", [web])
eu_suspension = AttributeFactory(all_attributes, "eu_suspension", [web])
omar_url = AttributeFactory(all_attributes, "omar_url", [file_dates])
odwar_url = AttributeFactory(all_attributes, "odwar_url", [file_dates])
eu_od_number = AttributeFactory(all_attributes, "eu_od_number", [web])
ema_od_number = AttributeFactory(all_attributes, "ema_od_number", [web])
eu_od_con = AttributeFactory(all_attributes, "eu_od_con", [web])
eu_od_date = AttributeFactory(all_attributes, "eu_od_date", [file_dates])
eu_od_pnumber = AttributeFactory(all_attributes, "eu_od_pnumber", [web])
eu_od_sponsor = AttributeFactory(all_attributes, "eu_od_sponsor", [web])
eu_od_comp_date = AttributeFactory(all_attributes, "eu_od_comp_date", [file_dates])
