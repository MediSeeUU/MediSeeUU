import PDFread as PDFr

# external files
import ECparse
import EPARparse

# Main file to run all parsers

PDFr.parse_folder(ECparse, 'dec_human')
PDFr.parse_folder(ECparse, 'dec_orphan')
PDFr.parse_folder(EPARparse, 'epars')

# To add: Xiao yi SMPC Parser
# To add: Elio's OMAR Parser
