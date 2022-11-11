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

# pdf_xml_converter
The pdf_xml_converter is responsible for converting pdf's to XML format. 
Right now it's called by pdf module, but will be seperated for extra modularity.

## XML Structure
The xml converter reads all lines from the given pdf and creates sections with 
bolded text from the pdf as a header and all paragraphs of unbolded text until 
the next header is found.

Each section contains exactly one header element and between 0 and infinite paragraph tags.
example of the structure:

< section >

  < header >

    Bolded text.

  < /header >

  < p >

    Non-bolded text.

  < /p >

< /section >

Additionally the XML converter also includes meta data in the <head>.
The meta data includes:
- PDF file name: str
- initial file indicatior: bool
- creation date of pdf: datetime
- last modification date of pdf: datetime

Example head structure:
<head>
  <creation_date>D:20071005142659+02'00'</creation_date>
  <modification_date>D:20071005142701+02'00'</modification_date>
  <initial_authorization>True or False</initial_authorization>
  <pdf_file>PDF_name.pdf</pdf_file>
</head>

Example of whole XML:
<xml>
  <head>
    <creation_date>D:20071005142659+02'00'</creation_date>
    <modification_date>D:20071005142701+02'00'</modification_date>
    <initial_authorization>True or False</initial_authorization>
    <pdf_file>PDF_name.pdf</pdf_file>
  </head>
  <body>
    <section>
      <header>
        First Section.
      </header>
      <p>
        First Paragraph.
      </p>
      .
      .
      .
      <p>
        Last Paragraph.
      </p>
    </section>
    .
    .
    .
    <section>
      <header>
        Last Section.
      </header>
      <p>
        First Paragraph.
      </p>
      .
      .
      .
      <p>
        Last Paragraph.
      </p>
    </section>
  </body>
</xml>

## Accessing XML data
The XML files can be accessed via the xml_parsing_utils.py. The functions can be called on ET.Elements nodes 
containing sections and provide a simple high level abstraction on XML node accessing allowing the programmer
to interface with the xml contents in a more intuitive manner.

Example utility function:

`section_contains_header_substring("substring to look for", section)` 

instead of:

`for head in section.findall(tags.header):
        if not head.text:
            return False
        if substring.lower() in head.text.lower():
            return True
    return False`

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
`
for section in xml_body:

  if xml_utils.section_contains_header_substring("relevant_header_attribute_1", section)
    medicine_info_struct = scrape_attribute_1(section, medicine_info_struct)

  if xml_utils.section_contains_substring("relevant_substring_attribute_2", section)
    medicine_info_struct = scrape_attribute_2(section, medicine_info_struct)

  if xml_utils.section_contains_paragraph_substring("relevant_paragraph_attribute_3", section)
    medicine_info_struct = scrape_attribute_3(section, medicine_info_struct)


return medicine_info_struct
`

© Copyright Utrecht University (Department of Information and Computing Sciences)
