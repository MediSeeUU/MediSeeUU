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

# pdf_xml_converter
The pdf_xml_converter is responsible for converting pdf's to XML format. 
Right now it's called by pdf scraper, but it will be seperated for extra modularity.

## XML Structure
The xml converter reads all lines from the given pdf and creates sections with 
bolded text from the pdf as a header and all paragraphs of unbolded text until 
the next header is found.

Each section contains exactly one header element and between 0 and infinite paragraph tags.
example of the structure:

![example_structure](https://github.com/MediSeeUU/MediSeeUU/blob/development/scraping/file_scraper/docs/sphinx-source/example_structure.png?raw=true)

Additionally, the XML converter also includes metadata in the <head>.
The meta data includes:
- PDF file name: str
- initial file indicatior: bool
- creation date of pdf: datetime
- last modification date of pdf: datetime

Example head structure:
![head_structure](https://github.com/MediSeeUU/MediSeeUU/blob/development/scraping/file_scraper/docs/sphinx-source/head_structure.png?raw=true)

Example of whole XML:
![whole_xml](https://github.com/MediSeeUU/MediSeeUU/blob/development/scraping/file_scraper/docs/sphinx-source/whole_xml.png?raw=true)

## Accessing XML data
The XML files can be accessed via the xml_parsing_utils.py. The functions can be called on ET.Elements nodes 
containing sections and provide a simple high level abstraction on XML node accessing allowing the programmer
to interface with the xml contents in a more intuitive manner.

Example utility function:

`section_contains_header_substring("substring to look for", section)` 

instead of:
![for_loop](https://github.com/MediSeeUU/MediSeeUU/blob/development/scraping/file_scraper/docs/sphinx-source/for_loop.png?raw=true)

or

`section_get_paragraph_text(paragraph_index, section)`

instead of:

`section.findall(tags.paragraph)[paragraph_index].text`

This method of interfacing with XML files allows the programmer to traverse all content within one pdf file once
and immediately scrape information when relevant rather than searching through the raw text within a PDF file per attribute.
By selecting sections that are relevant to an attribute the chance of scraping incorrect data is also reduced.

Another major advantage is that it now becomes easy to add new scraping functions for specific attributes while keeping
the code simple, clean and efficient.

Example attribute scraping on XML:
![scraping](https://github.com/MediSeeUU/MediSeeUU/blob/development/scraping/file_scraper/docs/sphinx-source/scraping.png?raw=true)

© Copyright Utrecht University (Department of Information and Computing Sciences)
