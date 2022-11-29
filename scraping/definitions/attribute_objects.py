import scraping.definitions.attributes as attr
import scraping.definitions.sources as src
import scraping.combiner.attribute_combining_functions as acf

# struct class
class ScraperAttribute:
    def __init__(self, name: str, sources: list[str], combine_function, json_function):
        self.name = name
        self.sources = sources
        self.combine_function = combine_function
        self.json_function = json_function

# add new ScraperAttribute to all_attributes and return name of ScraperAttribute
def AttributeFactory(all_attributes: set[ScraperAttribute], name: str, sources: list[str], combine_function = acf.combine_best_source, json_function = acf.json_static):
    attribute = ScraperAttribute(name, sources, combine_function, json_function)
    all_attributes.add(attribute)

# Initialize all attribute objects
all_attributes: set[ScraperAttribute] = set()
AttributeFactory(all_attributes, attr.atc_code, [src.web])
# AttributeFactory(all_attributes, attr.atc_name_l1, [src.web])
# AttributeFactory(all_attributes, attr.atc_name_l2, [src.web])
# AttributeFactory(all_attributes, attr.atc_name_l3, [src.web])
# AttributeFactory(all_attributes, attr.atc_name_l4, [src.web])
AttributeFactory(all_attributes, attr.active_substance, [src.web, src.decision_initial], acf.combine_select_string_overlap)
AttributeFactory(all_attributes, attr.eu_nas, [src.decision_initial])
AttributeFactory(all_attributes, attr.ema_procedure_start_initial, [src.epar])
AttributeFactory(all_attributes, attr.chmp_opinion_date, [src.epar])
AttributeFactory(all_attributes, attr.eu_aut_date, [src.web, src.decision_initial], acf.combine_best_source)
AttributeFactory(all_attributes, attr.eu_aut_type_initial, [src.decision_initial, src.annex_initial, src.web])
AttributeFactory(all_attributes, attr.eu_aut_type_current, [src.web])
AttributeFactory(all_attributes, attr.eu_pnumber, [src.web])
AttributeFactory(all_attributes, attr.eu_pnumber_id, [src.web])
AttributeFactory(all_attributes, attr.eu_legal_basis, [src.epar])
AttributeFactory(all_attributes, attr.aut_url, [src.file_dates])
AttributeFactory(all_attributes, attr.smpc_url, [src.file_dates])
AttributeFactory(all_attributes, attr.epar_url, [src.file_dates])
AttributeFactory(all_attributes, attr.eu_atmp, [src.decision])
AttributeFactory(all_attributes, attr.eu_med_type, [src.annex_initial], acf.combine_eu_med_type)
AttributeFactory(all_attributes, attr.eu_aut_status, [src.web])
AttributeFactory(all_attributes, attr.eu_brand_name, [src.web])
AttributeFactory(all_attributes, attr.eu_brand_name_current, [src.web])
# AttributeFactory(all_attributes, attr.eu_brand_name_history, [src.web])
AttributeFactory(all_attributes, attr.eu_brand_name_initial, [src.decision_initial])
AttributeFactory(all_attributes, attr.ema_number, [src.web])
AttributeFactory(all_attributes, attr.ema_number_id, [src.web])
AttributeFactory(all_attributes, attr.ema_number_certainty, [src.web])
AttributeFactory(all_attributes, attr.ema_number_check, [src.web])
# AttributeFactory(all_attributes, attr.eu_mah, )
AttributeFactory(all_attributes, attr.eu_mah_current, [src.web], acf.combine_best_source, acf.json_history_current)
AttributeFactory(all_attributes, attr.eu_mah_initial, [src.decision_initial], acf.combine_best_source, acf.json_history_initial)
# AttributeFactory(all_attributes, attr.eu_mah_history, [src.web])
AttributeFactory(all_attributes, attr.eu_prime_initial, [src.epar])
# AttributeFactory(all_attributes, attr.eu_prime_history, [src.epar])
AttributeFactory(all_attributes, attr.eu_od_initial, [src.decision_initial])
# AttributeFactory(all_attributes, attr.eu_od_history, [decision])  # ?
AttributeFactory(all_attributes, attr.ema_url, [src.file_dates])
AttributeFactory(all_attributes, attr.ec_url, [src.file_dates])
AttributeFactory(all_attributes, attr.ema_rapp, [src.epar])
AttributeFactory(all_attributes, attr.ema_corapp, [src.epar])
AttributeFactory(all_attributes, attr.eu_accel_assess_g, [src.epar])
AttributeFactory(all_attributes, attr.eu_accel_assess_m, [src.epar])
AttributeFactory(all_attributes, attr.assess_time_days_total, [src.annex_10])
AttributeFactory(all_attributes, attr.assess_time_days_active, [src.annex_10])
AttributeFactory(all_attributes, attr.assess_time_days_cstop, [src.annex_10])
AttributeFactory(all_attributes, attr.decision_time_days, [src.annex_10])
AttributeFactory(all_attributes, attr.ema_reexamination, [src.epar])
AttributeFactory(all_attributes, attr.eu_orphan_con_initial, [src.web])
AttributeFactory(all_attributes, attr.eu_orphan_con_current, [src.web])
AttributeFactory(all_attributes, attr.eu_referral, [src.web])
AttributeFactory(all_attributes, attr.eu_suspension, [src.web])
AttributeFactory(all_attributes, attr.omar_url, [src.file_dates])
AttributeFactory(all_attributes, attr.odwar_url, [src.file_dates])
AttributeFactory(all_attributes, attr.eu_od_number, [src.web])
AttributeFactory(all_attributes, attr.ema_od_number, [src.web])
AttributeFactory(all_attributes, attr.eu_od_con, [src.web])
AttributeFactory(all_attributes, attr.eu_od_date, [src.file_dates])
AttributeFactory(all_attributes, attr.eu_od_pnumber, [src.web])
AttributeFactory(all_attributes, attr.eu_od_sponsor, [src.web])
AttributeFactory(all_attributes, attr.eu_od_comp_date, [src.file_dates])
AttributeFactory(all_attributes, attr.eu_indication_initial, [src.annex_initial])
AttributeFactory(all_attributes, attr.ema_omar_condition, [src.omar])