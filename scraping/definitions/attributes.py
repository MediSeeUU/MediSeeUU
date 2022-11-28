import scraping.combiner.attribute_combining_functions as acf

# All sources :D
decision = "dec"
decision_initial = "dec_initial"
annex = "anx"
annex_initial = "anx_initial"
epar = "epar"
omar = "omar"
web = "web"
file_dates = "file_dates"
source_file = "source_file"
annex_10 = "annex_10"

# metadata attributes in json files
file_date = "file_date"
pdf_file = "pdf_file"


# struct class
class ScraperAttribute:
    def __init__(self, name: str, sources: list[str], combine_function: function = acf.combine_best_source, json_function: function = acf.json_static):
        self.name = name
        self.sources = sources
        self.combine_function = combine_function
        self.json_function = json_function


# add new ScraperAttribute to all_attributes and return name of ScraperAttribute
def AttributeFactory(all_attributes: set[ScraperAttribute], name: str, sources: list[str], combine_function, json_function):
    attr = ScraperAttribute(name, sources, combine_function, json_function)
    all_attributes.add(attr)
    return name

# Initialize all attribute objects
all_attributes: set[ScraperAttribute] = set()
atc_code = AttributeFactory(all_attributes, "atc_code", [web])
# atc_name_l1 = AttributeFactory(all_attributes, "atc_name_l1", [web])
# atc_name_l2 = AttributeFactory(all_attributes, "atc_name_l2", [web])
# atc_name_l3 = AttributeFactory(all_attributes, "atc_name_l3", [web])
# atc_name_l4 = AttributeFactory(all_attributes, "atc_name_l4", [web])
active_substance = AttributeFactory(all_attributes, "active_substance", [web, decision_initial], acf.combine_select_string_overlap)
eu_nas = AttributeFactory(all_attributes, "eu_nas", [decision_initial])
ema_procedure_start_initial = AttributeFactory(all_attributes, "ema_procedure_start_initial", [epar])
chmp_opinion_date = AttributeFactory(all_attributes, "chmp_opinion_date", [epar])
eu_aut_date = AttributeFactory(all_attributes, "eu_aut_date", [web, decision_initial], acf.check_all_equal)
eu_aut_type_initial = AttributeFactory(all_attributes, "eu_aut_type_initial", [decision_initial, annex_initial, web])
eu_aut_type_current = AttributeFactory(all_attributes, "eu_aut_type_current", [web])
eu_pnumber = AttributeFactory(all_attributes, "eu_pnumber", [web])
eu_pnumber_id = AttributeFactory(all_attributes, "eu_pnumber_id", [web])
eu_legal_basis = AttributeFactory(all_attributes, "eu_legal_basis", [epar])
aut_url = AttributeFactory(all_attributes, "aut_url", [file_dates])
smpc_url = AttributeFactory(all_attributes, "smpc_url", [file_dates])
epar_url = AttributeFactory(all_attributes, "epar_url", [file_dates])
eu_atmp = AttributeFactory(all_attributes, "eu_atmp", [decision])
eu_med_type = AttributeFactory(all_attributes, "eu_med_type", [annex_initial], acf.combine_eu_med_type)
eu_aut_status = AttributeFactory(all_attributes, "eu_aut_status", [web])
eu_brand_name = AttributeFactory(all_attributes, "eu_brand_name", [web])
eu_brand_name_current = AttributeFactory(all_attributes, "eu_brand_name_current", [web])
# eu_brand_name_history = AttributeFactory(all_attributes, "eu_brand_name_history", [web])
eu_brand_name_initial = AttributeFactory(all_attributes, "eu_brand_name_initial", [decision_initial])
ema_number = AttributeFactory(all_attributes, "ema_number", [web])
ema_number_id = AttributeFactory(all_attributes, "ema_number_id", [web])
ema_number_certainty = AttributeFactory(all_attributes, "ema_number_certainty", [web])
ema_number_check = AttributeFactory(all_attributes, "ema_number_check", [web])
# eu_mah = AttributeFactory(all_attributes, "eu_mah", )
eu_mah_current = AttributeFactory(all_attributes, "eu_mah_current", [web], acf.combine_best_source, acf.json_history_current)
eu_mah_initial = AttributeFactory(all_attributes, "eu_mah_initial", [decision_initial], acf.combine_best_source, acf.json_history_initial)
# eu_mah_history = AttributeFactory(all_attributes, "eu_mah_history", [web])
eu_prime_initial = AttributeFactory(all_attributes, "eu_prime_initial", [epar])
# eu_prime_history = AttributeFactory(all_attributes, "eu_prime_history", [epar])
eu_od_initial = AttributeFactory(all_attributes, "eu_od_initial", [decision_initial])
# eu_od_history = AttributeFactory(all_attributes, "eu_od_history", [decision])  # ?
ema_url = AttributeFactory(all_attributes, "ema_url", [file_dates])
ec_url = AttributeFactory(all_attributes, "ec_url", [file_dates])
ema_rapp = AttributeFactory(all_attributes, "ema_rapp", [epar])
ema_corapp = AttributeFactory(all_attributes, "ema_corapp", [epar])
eu_accel_assess_g = AttributeFactory(all_attributes, "eu_accel_assess_g", [epar])
eu_accel_assess_m = AttributeFactory(all_attributes, "eu_accel_assess_m", [epar])
assess_time_days_total = AttributeFactory(all_attributes, "assess_time_days_total", [annex_10])
assess_time_days_active = AttributeFactory(all_attributes, "assess_time_days_active", [annex_10])
assess_time_days_cstop = AttributeFactory(all_attributes, "assess_time_days_cstop", [annex_10])
decision_time_days = AttributeFactory(all_attributes, "decision_time_days", [annex_10])
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
eu_indication_initial = AttributeFactory(all_attributes, "eu_indication_initial", [annex_initial])
ema_omar_condition = AttributeFactory(all_attributes, "ema_omar_condition", [omar])

ema_prevalence = "ema_prevalence"
ema_alternative_treatments = "ema_alternative_treatments"
ema_significant_benefit = "ema_significant_benefit"
