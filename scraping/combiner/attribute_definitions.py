from enum import Enum

# string definitions of all to scrape attributes for reducing hardcoded strings
class id(Enum):
    atc_code = {"name": "atc_code", "sources": ["web"]}     # ATC code (chemical substance level 5)
    atc_name_l1 = {"name": "atc_name_l1"}                                 # ATC name (level 1)*
    atc_name_l2 = {"name": "atc_name_l2"}                                 # ATC name (level 2)*
    atc_name_l3 = {"name": "atc_name_l3"}                                 # ATC name (level 3)*
    atc_name_l4 = {"name": "atc_name_l4"}                                 # ATC name (level 4)*
    active_substance = {"name": "active_substance"}                       # Active substance
    eu_nas = {"name": "eu_nas"}                                           # EU new active substance
    ema_procedure_start_initial = {"name": "ema_procedure_start_initial"} # Initial EMA procedure start date
    chmp_opinion_date = {"name": "chmp_opinion_date"}                     # Initial EMA (CHMP) opinion date
    eu_aut_date = {"name": "eu_aut_date", "sources": ["dec_initial","web"], "combine": True}                                 # Initial EU authorisation date
    eu_aut_type_initial = {"name": "eu_aut_type_initial"}                 # Initial type of EU authorisation*
    eu_aut_type_current = {"name": "eu_aut_type_current"}                 # Current type of EU authorisation*
    eu_brand_name_initial = {"name": "eu_brand_name_initial"}             # Initial EU brand name*
    eu_pnumber = {"name": "eu_pnumber"}                                   # EU product number
    eu_pnumber_id = {"name": "eu_pnumber_id"}                             # EU product number ID
    eu_legal_basis = {"name": "eu_legal_basis"}                           # EU legal basis
    aut_url = {"name": "aut_url"}                                         # URL to EU authorisation decision
    smpc_url = {"name": "smpc_url"}                                       # URL to EU authorisation annex
    epar_url = {"name": "epar_url"}                                       # URL to EMA initial authorisation EPAR
    eu_atmp = {"name": "eu_atmp"}                                         # EU ATMP
    eu_med_type = {"name": "eu_med_type"}                                 # EU type of medicine
    eu_aut_status = {"name": "eu_aut_status"}                             # EU authorisation status
    eu_brand_name = {"name": "eu_brand_name"}                             # EU brand name*
    eu_brand_name_current = {"name": "eu_brand_name_current"}             # Current EU brand name
    eu_brand_name_history = {"name": "eu_brand_name_history"}             # History of EU brand names*
    ema_number = {"name": "ema_number"}                                   # EMA application number
    ema_number_id = {"name": "ema_number_id"}                             # EMA application number ID
    ema_number_certainty = {"name": "ema_number_certainty"}               # EMA application number certainty
    ema_number_check = {"name": "ema_number_check"}                       # EMA application number check
    eu_mah = {"name": "eu_mah"}                                           # EU marketing authorisation holder*
    eu_mah_current = {"name": "eu_mah_current"}                           # Current EU marketing authorisation holder*
    eu_mah_initial = {"name": "eu_mah_initial"}                           # Initial EU marketing authorisation holder
    eu_mah_history = {"name": "eu_mah_history"}                           # History of EU marketing authorisation holders
    eu_prime_initial = {"name": "eu_prime_initial"}                       # EU Priority Medicine at authorisation
    eu_prime_history = {"name": "eu_prime_history"}                       # History of EU Priority Medicine
    eu_od_initial = {"name": "eu_od_initial"}                             # EU orphan designation at au,thorisation
    eu_od_history = {"name": "eu_od_history"}                             # Histo,ry of EU orphan design,ation
    ema_url = {"name": "ema_url"}                                         # URL to EMA medicinal product p,age,
    ec_url = {"name": "ec_url"}                                           # URL to EC medicinal product page,
    ema_rapp = {"name": "ema_rapp"}                                       # EMA rapporteur for initial a,uthorisat,ion
    ema_corapp = {"name": "ema_corapp"}                                   # EMA co-rapporteur for in,itial aut,horisation
    eu_accel_assess_g = {"name": "eu_accel_assess_g"}                     # EU accelerated assessment granted
    eu_accel_assess_m = {"name": "eu_accel_assess_m"}                     # EU accelerated assessment maintained
    assess_time_days_total = {"name": "assess_time_days_total"}           # Duration of initial EU authorisation assessment procedure (total days)
    assess_time_days_active = {"name": "assess_time_days_active"}         # Duration of initial EU authorisation assessment procedure (active days)
    assess_time_days_cstop = {"name": "assess_time_days_cstop"}           # Duration of initial EU authorisation assessment procedure (clock-stop days)
    ec_decision_time_days = {"name": "ec_decision_time_days"}             # EC decision time (days)
    ema_reexamination = {"name": "ema_reexamination"}                     # EMA re-examination performed
    eu_orphan_con_initial = {"name": "eu_orphan_con_initial"}             # Initial EU orphan conditions
    eu_orphan_con_current = {"name": "eu_orphan_con_current"}             # Current EU orphan conditions
    eu_referral = {"name": "eu_referral"}                                 # EU referral
    eu_suspension = {"name": "eu_suspension"}                             # EU suspension
    omar_url = {"name": "omar_url"}                                       # URL to orphan maintanance assessment report
    odwar_url = {"name": "odwar_url"}                                     # URL to orphan designation withdrawal assessment report
    eu_od_number = {"name": "eu_od_number"}                               # EU orphan designation number
    ema_od_number = {"name": "ema_od_number"}                             # EMA orphan designation number
    eu_od_con = {"name": "eu_od_con"}                                     # EU orphan designation condition
    eu_od_date = {"name": "eu_od_date"}                                   # EU orphan designation date
    eu_od_pnumber = {"name": "eu_od_pnumber"}                             # EU product number for orphan designation
    eu_od_sponsor = {"name": "eu_od_sponsor"}                             # Sponsor for EU orphan designation
    eu_od_comp_date = {"name": "eu_od_comp_date"}                         # COMP decision date (for EU orphan designation)

class value(Enum):
    not_found = "|->NOT FOUND<-|"

class file(Enum):
    decision_file = "dec"
    annex_file = "anx"
    epar_file = "epar"
    omar_file = "omar"