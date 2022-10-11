import pdf_read as pdf_r

# external files
import parsers.ec_parse as ec_parse
#import parsers.epar_parse as epar_parse

# Main file to run all parsers

# TODO: Create dictionary per medicine
# datum toevoegen


pdf_r.parse_folder(ec_parse, 'dec_human')
#pdf_r.parse_folder(ec_parse, 'dec_orphan')
#pdf_r.parse_folder(epar_parse, 'epars')

# To add: Xiao yi SMPC parsers
# To add: Elio's OMAR parsers
