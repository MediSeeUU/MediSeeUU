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
filename = "filename"
pdf_file = "pdf_file"
xml_file = "xml_file"
is_initial = "is_initial"
creation_date = "creation_date"
modification_date = "modification_date"


# struct class
class ScraperAttribute:
    def __init__(self, name: str, sources: list[str], combine_function, json_function):
        self.name = name
        self.sources = sources
        self.combine_function = combine_function
        self.json_function = json_function


# add new ScraperAttribute to all_attributes and return name of ScraperAttribute
def attribute_factory(all_attributes: set[ScraperAttribute], name: str, sources: list[str], combine_function = acf.combine_best_source, json_function = acf.json_static):
    attr = ScraperAttribute(name, sources, combine_function, json_function)
    all_attributes.add(attr)
    return name

# Initialize all attribute objects
all_attributes: set[ScraperAttribute] = set()
atc_code = attribute_factory(all_attributes, "atc_code", [web])
# atc_name_l1 = attribute_factory(all_attributes, "atc_name_l1", [web])
# atc_name_l2 = attribute_factory(all_attributes, "atc_name_l2", [web])
# atc_name_l3 = attribute_factory(all_attributes, "atc_name_l3", [web])
# atc_name_l4 = attribute_factory(all_attributes, "atc_name_l4", [web])
active_substance = attribute_factory(all_attributes, "active_substance", [web, decision_initial], acf.combine_select_string_overlap)
eu_nas = attribute_factory(all_attributes, "eu_nas", [decision_initial])
ema_procedure_start_initial = attribute_factory(all_attributes, "ema_procedure_start_initial", [epar])
chmp_opinion_date = attribute_factory(all_attributes, "chmp_opinion_date", [epar])
eu_aut_date = attribute_factory(all_attributes, "eu_aut_date", [web, decision_initial], acf.check_all_equal)
eu_aut_type_initial = attribute_factory(all_attributes, "eu_aut_type_initial", [decision_initial, annex_initial, web])
eu_aut_type_current = attribute_factory(all_attributes, "eu_aut_type_current", [web])
eu_pnumber = attribute_factory(all_attributes, "eu_pnumber", [web])
eu_pnumber_id = attribute_factory(all_attributes, "eu_pnumber_id", [web])
eu_legal_basis = attribute_factory(all_attributes, "eu_legal_basis", [epar])
aut_url = attribute_factory(all_attributes, "aut_url", [file_dates])
smpc_url = attribute_factory(all_attributes, "smpc_url", [file_dates])
epar_url = attribute_factory(all_attributes, "epar_url", [file_dates])
eu_atmp = attribute_factory(all_attributes, "eu_atmp", [decision])
eu_med_type = attribute_factory(all_attributes, "eu_med_type", [annex_initial], acf.combine_eu_med_type)
eu_aut_status = attribute_factory(all_attributes, "eu_aut_status", [web])
eu_brand_name = attribute_factory(all_attributes, "eu_brand_name", [web])
eu_brand_name_current = attribute_factory(all_attributes, "eu_brand_name_current", [web])
# eu_brand_name_history = attribute_factory(all_attributes, "eu_brand_name_history", [web])
eu_brand_name_initial = attribute_factory(all_attributes, "eu_brand_name_initial", [decision_initial])
ema_number = attribute_factory(all_attributes, "ema_number", [web])
ema_number_id = attribute_factory(all_attributes, "ema_number_id", [web])
ema_number_certainty = attribute_factory(all_attributes, "ema_number_certainty", [web])
ema_number_check = attribute_factory(all_attributes, "ema_number_check", [web])
# eu_mah = attribute_factory(all_attributes, "eu_mah", )
eu_mah_current = attribute_factory(all_attributes, "eu_mah_current", [web], acf.combine_best_source, acf.json_history_current)
eu_mah_initial = attribute_factory(all_attributes, "eu_mah_initial", [decision_initial], acf.combine_best_source, acf.json_history_initial)
# eu_mah_history = attribute_factory(all_attributes, "eu_mah_history", [web])
eu_prime_initial = attribute_factory(all_attributes, "eu_prime_initial", [epar])
# eu_prime_history = attribute_factory(all_attributes, "eu_prime_history", [epar])
eu_od_initial = attribute_factory(all_attributes, "eu_od_initial", [decision_initial])
# eu_od_history = attribute_factory(all_attributes, "eu_od_history", [decision])  # ?
ema_url = attribute_factory(all_attributes, "ema_url", [file_dates])
ec_url = attribute_factory(all_attributes, "ec_url", [file_dates])
ema_rapp = attribute_factory(all_attributes, "ema_rapp", [epar])
ema_corapp = attribute_factory(all_attributes, "ema_corapp", [epar])
eu_accel_assess_g = attribute_factory(all_attributes, "eu_accel_assess_g", [epar])
eu_accel_assess_m = attribute_factory(all_attributes, "eu_accel_assess_m", [epar])
assess_time_days_total = attribute_factory(all_attributes, "assess_time_days_total", [annex_10])
assess_time_days_active = attribute_factory(all_attributes, "assess_time_days_active", [annex_10])
assess_time_days_cstop = attribute_factory(all_attributes, "assess_time_days_cstop", [annex_10])
decision_time_days = attribute_factory(all_attributes, "decision_time_days", [annex_10])
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
eu_indication_initial = attribute_factory(all_attributes, "eu_indication_initial", [annex_initial])
ema_omar_condition = attribute_factory(all_attributes, "ema_omar_condition", [omar])

#TODO: check
eu_therapeutic_indications = attribute_factory(all_attributes, "eu_therapeutic_indications", [annex]) #or initial?
active_time_elapsed = attribute_factory(all_attributes, "active_time_elapsed", [])
clock_stop_elapsed = attribute_factory(all_attributes, "clock_stop_elapsed", [])

ema_prevalence = "ema_prevalence"
ema_alternative_treatments = "ema_alternative_treatments"
ema_insufficient_roi = "ema_insufficient_roi" #TODO: check
active_clock_elapseds = "active_clock_elapseds"
