import datetime

#data type values
#generic string values
generic_not_found = "Not found."
generic_not_applicable = "Not available at time of document publication."
generic_should_be_present = "Value should be present in document."

#booleans
bool_true = "true"
bool_false = "false"
bool_not_found = generic_not_found
bool_not_applicable = generic_not_applicable
bool_should_be_present = generic_should_be_present

#strings
string_not_found = generic_not_found
string_not_applicable = generic_not_applicable
string_should_be_present = generic_should_be_present

#numeric
numeric_not_found = generic_not_found
numeric_not_applicable = generic_not_applicable
numeric_should_be_present = generic_should_be_present

#integer
int_not_found = numeric_not_found
int_not_applicable = numeric_not_applicable
int_should_be_present = numeric_should_be_present

#floating point
float_not_found = numeric_not_found
float_not_applicable = numeric_not_applicable
float_should_be_present = numeric_should_be_present

#dates
# default_date = datetime.datetime.min.date()
# default_date_str = str(datetime.datetime.min.date())
date_not_found = generic_not_found
date_not_applicable = generic_not_applicable
date_should_be_present = generic_should_be_present
date_left_blank = "date is left blank in document"

#datetimes
# default_datetime = datetime.date.min.day()
# default_datetime_str = str(datetime.date.min.day())
datetime_not_found = generic_not_found
datetime_not_applicable = generic_not_applicable
datetime_should_be_present = generic_should_be_present
datetime_left_blank = "date is left blank in document"
