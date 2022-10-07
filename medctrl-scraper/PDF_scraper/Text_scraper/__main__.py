import PDFread as PDFr
import annex_parser as AP

# external files
import ECparse
import EPARparse

# Main file to run all parsers

# PDFr.parseFolder(ECparse, 'dec_human')
# PDFr.parseFolder(ECparse, 'dec_orphan')
PDFr.parse_folder(EPARparse, 'epars')

# To add: Xiao yi SMPC Parser
# To add: Elio's OMAR Parser
