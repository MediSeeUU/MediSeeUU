import scraping.combiner.attribute_combining_functions as acf
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.sources as src


# struct class
class ScraperAttribute:
    def __init__(self, name: str, sources: list[str], combine_function, json_function, is_orphan):
        self.name = name
        self.sources = sources
        self.combine_function = combine_function
        self.json_function = json_function
        self.is_orphan = is_orphan


# add new ScraperAttribute to all_attribute_objects and return name of ScraperAttribute
def attribute_factory(all_attribute_objects: set[ScraperAttribute], name: str, sources: list[str],
                      is_orphan: bool = False, combine_function=acf.combine_first,
                      json_function=acf.json_static):
    attribute = ScraperAttribute(name, sources, combine_function, json_function, is_orphan)
    all_attribute_objects.add(attribute)


# Initialize all attribute objects
objects: set[ScraperAttribute] = set()
attribute_factory(objects, attr.atc_code, [src.web])
attribute_factory(objects, attr.active_substance, [src.web, src.dec_initial], False, acf.combine_string_overlap)
attribute_factory(objects, attr.eu_nas, [src.dec_initial])
attribute_factory(objects, attr.ema_procedure_start_initial, [src.epar])
attribute_factory(objects, attr.chmp_opinion_date, [src.epar], False, acf.combine_date)
attribute_factory(objects, attr.eu_aut_date, [src.web, src.dec_initial], False, acf.combine_date)
attribute_factory(objects, attr.eu_aut_type_initial, [src.dec_initial, src.anx_initial, src.web], False,
                  acf.combine_first, acf.json_initial)
attribute_factory(objects, attr.eu_aut_type_current, [src.web], False, acf.combine_first, acf.json_current)
attribute_factory(objects, attr.eu_pnumber, [src.web])
attribute_factory(objects, attr.eu_legal_basis, [src.epar])
attribute_factory(objects, attr.aut_url, [src.dec_initial], False, acf.combine_get_file_url, acf.json_static)
attribute_factory(objects, attr.smpc_url, [src.anx_initial], False, acf.combine_get_file_url, acf.json_static)
attribute_factory(objects, attr.epar_url, [src.epar], False, acf.combine_get_file_url, acf.json_static)
attribute_factory(objects, attr.eu_atmp, [src.dec_initial])
attribute_factory(objects, attr.eu_med_type, [src.anx_initial], False, acf.combine_eu_med_type)
attribute_factory(objects, attr.eu_aut_status, [src.web], False, acf.combine_eu_aut_status)
attribute_factory(objects, attr.eu_brand_name_current, [src.web], False, acf.combine_first, acf.json_current)
attribute_factory(objects, attr.eu_brand_name_initial, [src.dec_initial], False, acf.combine_first, acf.json_initial)
attribute_factory(objects, attr.ema_number, [src.web])
attribute_factory(objects, attr.ema_number_id, [src.web])
attribute_factory(objects, attr.ema_number_certainty, [src.web])
attribute_factory(objects, attr.ema_number_check, [src.web], False, acf.combine_ema_number_check)
attribute_factory(objects, attr.eu_mah_current, [src.web], False, acf.combine_first, acf.json_current)
attribute_factory(objects, attr.eu_mah_initial, [src.dec_initial], False, acf.combine_first, acf.json_initial)
attribute_factory(objects, attr.eu_prime_initial, [src.epar], False, acf.combine_first, acf.json_initial)
attribute_factory(objects, attr.eu_od_initial, [src.dec_initial], False, acf.combine_first, acf.json_initial)
attribute_factory(objects, attr.ema_rapp, [src.epar])
attribute_factory(objects, attr.ema_corapp, [src.epar])
attribute_factory(objects, attr.eu_accel_assess_g, [src.epar])
attribute_factory(objects, attr.assess_time_days_total, [src.epar], False, acf.combine_assess_time_days_total)
attribute_factory(objects, attr.assess_time_days_active, [src.annex_10], False, acf.combine_assess_time_days_active)
attribute_factory(objects, attr.assess_time_days_cstop, [src.annex_10], False, acf.combine_assess_time_days_cstop)
attribute_factory(objects, attr.ec_decision_time_days, [src.annex_10], False, acf.combine_decision_time_days)
attribute_factory(objects, attr.ema_reexamination, [src.epar])
attribute_factory(objects, attr.eu_orphan_con_current, [src.web], False, acf.combine_first, acf.json_current)
attribute_factory(objects, attr.eu_referral, [src.web])
attribute_factory(objects, attr.eu_suspension, [src.web])
attribute_factory(objects, attr.omar_url, [src.omar], True, acf.combine_get_file_url, acf.json_static)
attribute_factory(objects, attr.odwar_url, [src.odwar], True, acf.combine_get_file_url, acf.json_static)
attribute_factory(objects, attr.eu_od_number, [src.web], True)
attribute_factory(objects, attr.ema_od_number, [src.web], True)
attribute_factory(objects, attr.eu_od_con, [src.web], True)
attribute_factory(objects, attr.eu_od_date, [src.web], True, acf.combine_date)
attribute_factory(objects, attr.eu_od_pnumber, [src.web], True)
attribute_factory(objects, attr.eu_od_sponsor, [src.web], True, acf.combine_first, acf.json_current)
attribute_factory(objects, attr.eu_od_comp_date, [src.dec_initial], True, acf.combine_date)
attribute_factory(objects, attr.eu_indication_initial, [src.anx_initial], False, acf.combine_first, acf.json_initial)
attribute_factory(objects, attr.ema_omar_condition, [src.omar])
attribute_factory(objects, attr.eu_procedures_todo, [src.web], False, acf.combine_eu_procedures_todo)
attribute_factory(objects, attr.orphan_status, [src.web])


# TODO: scrape links to webpages
# attribute_factory(objects, attr.ema_url, [src.web], acf.combine_get_file_url, acf.json_static)
# attribute_factory(objects, attr.ec_url, [src.web], acf.combine_get_file_url, acf.json_static)
