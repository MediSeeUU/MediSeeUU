import pdf_read as PDFr

# external files
import parsers.ec_parse as ec_parse
import parsers.epar_parse as epar_parse

# Main file to run all parsers

# TODO: Create dictionary per medicine
#datum toevoegen

PDFr.parse_folder(ec_parse, 'dec_human')
PDFr.parse_folder(ec_parse, 'dec_orphan')
PDFr.parse_folder(epar_parse, 'epars')

# To add: Xiao yi SMPC parsers
# To add: Elio's OMAR parsers
