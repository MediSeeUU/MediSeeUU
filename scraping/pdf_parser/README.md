# General
The main functionality of the file scraper is to parse relevant attributes from the 
PDF files and Excel files obtained by the web scraper. 

PDF Types:
- Authorisation Decision                (dec)
- Summary of Product Characteristics    (annex)
- European Public Assessment Report     (epar)
- Orphan Maintenance Assessment Report  (omar)

To streamline this process, PDFs are first converted to XML files. This is being
done by the pdf_xml_converter. This allows for a fast and easy way to search 
information in PDFs. This process is being complimented by the xml_parsing_utils
which provides convenient functions to find particular parts of information.

The ec_parse is excluded from this process as it cannot easily be converted to
an XML file.

# Input & Output
## Input
The filepath of the data folder containing the active_withdrawn folder,
which will contain all human and orphan medicines.

## Output
- A JSON file for every medicine, containing all relevant attributes of that medicine.
  - JSON name format: `{EU_number}_pdf_parser.json`

# Other points of interest
Parsing attributes from the XML files is multitudes faster than parsing directly
from a PDF file. Logically it will take some time to create the XML files, but 
they only have to be created once, which will save time in the long run.

Visualisation of the scraped attributes: [Visualisations PDF](MediSee_PDF_visualisation.html)

© Copyright Utrecht University (Department of Information and Computing Sciences)
