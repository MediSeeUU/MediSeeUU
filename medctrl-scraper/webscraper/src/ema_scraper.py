import requests
import bs4
import re


def pdf_links_from_url(url: str):
    # Expecting a link scraped from the EC website. Link should look like this
    # https://www.ema.europa.eu/en/medicines/human/EPAR/tandemact
    html_obj = requests.get(url)

    # Last part of the url, contains the medicine name
    medicine_name = url.split('/')[-1]

    # If an http error occurred, throw error
    # TODO: Graceful handling
    html_obj.raise_for_status()

    soup = bs4.BeautifulSoup(html_obj.text, "html.parser")

    # The documents we search are under the header
    #   Initial marketing-authorisation documents
    # Element is in a <div><h4><span>text</span></h4> [pdfs here] </div>
    # Get parent thrice to find the tag that the PDFs are located in.
    # Parent of the found object is considered <span>
    specific_soup = soup.find(string="Initial marketing-authorisation documents").parent.parent.parent

    # Compiles a list of all link tags, that link to a .pdf file.
    link_tags = specific_soup.find_all('a')

    # Get all links to pdf files from the
    link_list: [str] = list(map(lambda a: a["href"], link_tags))

    # TEMP: https://www.ema.europa.eu/documents/assessment-report/faslodex-epar-public-assessment-report_en.pdf
    # TEMP: https://www.ema.europa.eu/documents/scientific-discussion/ambirix-epar-scientific-discussion_en.pdf
    # TEMP: https://www.ema.europa.eu/documents/procedural-steps/ambirix-epar-procedural-steps-taken-authorisation_en.pdf
    priority_list = ["public-assessment-report", "scientific-discussion", "procedural-steps-taken-authorisation"]

    # Go through all links, try to find the document that is the highest on the priority list first.
    for type_of_report in priority_list:
        for item in link_list:
            if type_of_report in item:
                return item

    # If nothing is found, we throw an exception. This also passes all found URLs on newlines
    raise Exception(f"No valid URLs found for {medicine_name}. Found URLs are listed below.\n" + "\n".join(link_list))


print(pdf_links_from_url("https://www.ema.europa.eu/en/medicines/human/EPAR/faslodex"))
