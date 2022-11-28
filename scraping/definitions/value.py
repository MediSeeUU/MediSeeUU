import datetime

# default values
not_found = "|->NOT FOUND<-|"
insufficient_overlap = "|->INSUFFICIENT OVERLAP<-|"
default_date = datetime.datetime(1900, 1, 1, 0, 0)
NA_before = "NA_at_release_date"
not_scrapeable = "not_easily_scrapeable"
yes_str = "yes"
no_str = "no"

# attribute values:
aut_type_standard = "standard"
aut_type_conditional = "conditional"
aut_type_exceptional = "exceptional"
# TODO: dit soort dingen afspreken
authorization_type_unknown = "exceptional or conditional"

eu_aut_date_blank = "date_is_blank"

eu_med_type_biologicals = "biologicals"
eu_med_type_atmp = "ATMP"
eu_med_type_small_molecule = "small molecule"

eu_alt_treatment_no_benefit = "no_significant_benefit"
eu_alt_treatment_benefit = "significant_benefit"
