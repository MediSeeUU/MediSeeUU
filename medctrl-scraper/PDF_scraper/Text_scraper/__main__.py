import pdf_read as pdf_r
import parsers.annex_parser as ap

# external files
import parsers.ec_parse as ec_parse
#import parsers.epar_parse as epar_parse

# Main file to run all parsers

# TODO: Create dictionary per medicine
# datum toevoegen


pdf_r.parse_folder(ec_parse, 'dec_human')
#pdf_r.parse_folder(ec_parse, 'dec_orphan')
#pdf_r.parse_folder(epar_parse, 'epars')
ap.parse_smpc_file("parsers/test_data/vydura-epar-public-assessment-report_en.pdf")

# To add: Xiao yi SMPC parsers
# To add: Elio's OMAR parsers
