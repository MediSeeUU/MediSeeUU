# General
The main functionality of the PDF scraper is to parse relevant attributes from the 
pdf files obtained by the web scraper. 

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
The filepath of the file that needs to be parsed.

## Output
- An XML file for every PDF file, which contains all the information from the PDFs but
  seperated into headers, sections and paragraphs.
- A JSON file for every medicine, containing all relevant attributes of that medicine.
  - JSON name format: `{EU_number}_pdf_parser.json`

# Other points of interest
Parsing attributes from the XML files is multitudes faster than parsing directly
from a PDF file. Logically it will take some time to create the XML files, but 
they only have to be created once, which will save time in the long run.

Visualisation of the scraped attributes: [Visualisaties PDF](MediSee_PDF_visualisation.html)