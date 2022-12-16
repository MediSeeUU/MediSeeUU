import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.sources as src
import scraping.combiner.attribute_combining_functions as acf

# struct class
class ScraperAttribute:
    def __init__(self, name: str, sources: list[str], combine_function, json_function):
        self.name = name
        self.sources = sources
        self.combine_function = combine_function
        self.json_function = json_function

# add new ScraperAttribute to all_attribute_objects and return name of ScraperAttribute
def AttributeFactory(all_attribute_objects: set[ScraperAttribute], name: str, sources: list[str], combine_function = acf.combine_best_source, json_function = acf.json_static):
    attribute = ScraperAttribute(name, sources, combine_function, json_function)
    all_attribute_objects.add(attribute)

# Initialize all attribute objects
all_attribute_objects: set[ScraperAttribute] = set()
AttributeFactory(all_attribute_objects, attr.atc_code, [src.web])
AttributeFactory(all_attribute_objects, attr.active_substance, [src.web, src.decision_initial], acf.combine_select_string_overlap)
AttributeFactory(all_attribute_objects, attr.eu_nas, [src.decision_initial])
AttributeFactory(all_attribute_objects, attr.ema_procedure_start_initial, [src.epar])
AttributeFactory(all_attribute_objects, attr.chmp_opinion_date, [src.epar])
AttributeFactory(all_attribute_objects, attr.eu_aut_date, [src.web, src.decision_initial], acf.combine_best_source)
AttributeFactory(all_attribute_objects, attr.eu_aut_type_initial, [src.decision_initial, src.annex_initial, src.web], acf.combine_best_source, acf.json_history_initial)
AttributeFactory(all_attribute_objects, attr.eu_aut_type_current, [src.web], acf.combine_best_source, acf.json_history_current)
AttributeFactory(all_attribute_objects, attr.eu_pnumber, [src.web])
AttributeFactory(all_attribute_objects, attr.eu_legal_basis, [src.epar]) #TODO: initial and current split?
AttributeFactory(all_attribute_objects, attr.aut_url, [src.decision_initial], acf.combine_get_file_url, acf.json_history_current)
AttributeFactory(all_attribute_objects, attr.smpc_url, [src.annex_initial], acf.combine_get_file_url, acf.json_history_current)
AttributeFactory(all_attribute_objects, attr.epar_url, [src.epar], acf.combine_get_file_url, acf.json_history_current)
AttributeFactory(all_attribute_objects, attr.eu_atmp, [src.decision_initial])
AttributeFactory(all_attribute_objects, attr.eu_med_type, [src.annex_initial], acf.combine_eu_med_type)
AttributeFactory(all_attribute_objects, attr.eu_aut_status, [src.web]) #TODO: initial and current split?
AttributeFactory(all_attribute_objects, attr.eu_brand_name_current, [src.web], acf.combine_best_source, acf.json_history_current)
AttributeFactory(all_attribute_objects, attr.eu_brand_name_initial, [src.decision_initial], acf.combine_best_source, acf.json_history_initial)
AttributeFactory(all_attribute_objects, attr.ema_number, [src.web])
AttributeFactory(all_attribute_objects, attr.ema_number_id, [src.web])
AttributeFactory(all_attribute_objects, attr.ema_number_certainty, [src.web])
AttributeFactory(all_attribute_objects, attr.ema_number_check, [src.web], acf.combine_ema_number_check)
AttributeFactory(all_attribute_objects, attr.eu_mah_current, [src.web], acf.combine_best_source, acf.json_history_current)
AttributeFactory(all_attribute_objects, attr.eu_mah_initial, [src.decision_initial], acf.combine_best_source, acf.json_history_initial)
AttributeFactory(all_attribute_objects, attr.eu_prime_initial, [src.epar], acf.combine_best_source, acf.json_history_initial)
# AttributeFactory(all_attribute_objects, attr.eu_prime_history, [src.epar]) #TODO: naar current?
AttributeFactory(all_attribute_objects, attr.eu_od_initial, [src.decision_initial], acf.combine_best_source, acf.json_history_initial)
# AttributeFactory(all_attribute_objects, attr.eu_od_history, [decision])  # TODO: naar current?
# AttributeFactory(all_attribute_objects, attr.ema_url, [src.web], acf.combine_get_file_url, acf.json_history_current) #TODO: scrape links to webpages
# AttributeFactory(all_attribute_objects, attr.ec_url, [src.web], acf.combine_get_file_url, acf.json_history_current)
AttributeFactory(all_attribute_objects, attr.ema_rapp, [src.epar])
AttributeFactory(all_attribute_objects, attr.ema_corapp, [src.epar])
AttributeFactory(all_attribute_objects, attr.eu_accel_assess_g, [src.epar])
# AttributeFactory(all_attribute_objects, attr.eu_accel_assess_m, [src.epar]) #TODO: not defined in koran
AttributeFactory(all_attribute_objects, attr.assess_time_days_total, [src.epar], acf.combine_assess_time_days_total)
AttributeFactory(all_attribute_objects, attr.assess_time_days_active, [src.annex_10], acf.combine_assess_time_days_active)
AttributeFactory(all_attribute_objects, attr.assess_time_days_cstop, [src.annex_10], acf.combine_assess_time_days_cstop)
AttributeFactory(all_attribute_objects, attr.ec_decision_time_days, [src.annex_10], acf.combine_decision_time_days)
AttributeFactory(all_attribute_objects, attr.ema_reexamination, [src.epar])
AttributeFactory(all_attribute_objects, attr.eu_orphan_con_current, [src.web], acf.combine_best_source, acf.json_history_current)
AttributeFactory(all_attribute_objects, attr.eu_referral, [src.web])
AttributeFactory(all_attribute_objects, attr.eu_suspension, [src.web])
AttributeFactory(all_attribute_objects, attr.omar_url, [src.omar], acf.combine_get_file_url, acf.json_history_current)
# AttributeFactory(all_attribute_objects, attr.odwar_url, [src.odwar], acf.combine_get_file_url, acf.json_history_current) #TODO: add odwar
AttributeFactory(all_attribute_objects, attr.eu_od_number, [src.web])
AttributeFactory(all_attribute_objects, attr.ema_od_number, [src.web])
AttributeFactory(all_attribute_objects, attr.eu_od_con, [src.web])
AttributeFactory(all_attribute_objects, attr.eu_od_date, [src.web])
AttributeFactory(all_attribute_objects, attr.eu_od_pnumber, [src.web])
AttributeFactory(all_attribute_objects, attr.eu_od_sponsor, [src.web])
AttributeFactory(all_attribute_objects, attr.eu_od_comp_date, [src.decision_initial])
AttributeFactory(all_attribute_objects, attr.eu_indication_initial, [src.annex_initial], acf.combine_best_source, acf.json_history_initial)
AttributeFactory(all_attribute_objects, attr.ema_omar_condition, [src.omar])
AttributeFactory(all_attribute_objects, attr.eu_procedures_todo, [src.web], acf.combine_eu_procedures_todo)
AttributeFactory(all_attribute_objects, attr.orphan_status, [src.web])
