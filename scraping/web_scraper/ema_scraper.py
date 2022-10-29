import requests
import logging
import bs4

log = logging.getLogger("webscraper.ema_scraper")


def pdf_links_from_url(url: str) -> (str, str):
    """ Gets the pdf link on the EMA website that is highest on the priority list and a link to the OMAR document if it exists

    Args:
        url (str): Link to the medicine page on the EMA website

    Raises:
        Exception: If nothing is found, we throw an exception. This also passes all found URLs on newlines

    Returns:
        str: The pdf link that is highest on the priority list
    """
    # Expecting a link scraped from the EC website. Link should look like this
    # https://www.ema.europa.eu/en/medicines/human/EPAR/tandemact
    html_obj = requests.get(url)

    # Last part of the url, contains the medicine name
    medicine_name: str = url.split('/')[-1]

    # TODO: Graceful handling
    html_obj.raise_for_status()

    soup = bs4.BeautifulSoup(html_obj.text, "html.parser")

    

    # The documents we search are under the header
    #   Initial marketing-authorisation documents
    # Element is in a <div><h4><span>text</span></h4> [pdfs here] </div>
    # Get parent thrice to find the tag that the PDFs are located in.
    # Parent of the found object is considered <span>

    complete_soup = soup.find(string="Initial marketing-authorisation documents")

    if complete_soup != None:
        specific_soup = complete_soup.parent.parent.parent
    else:
        log.warning(f"There are no initial marketing-authorisation documents")
        return "", ""

    # Compiles a list of all link tags, that link to a .pdf file.
    link_tags = specific_soup.find_all('a')

    # Get all links to pdf files from the
    url_list: list[str] = list(map(lambda a: a["href"], link_tags))

    # Files named 'public-assessment-report' will be the highest priority in the search.
    priority_list: list[str] = ["public-assessment-report", "scientific-discussion", "procedural-steps-taken-authorisation"]
    priority_link: str = ""
    omar_link: str = ""
    break_epar_loop: bool = False

    # Go through all links, try to find the document that is the highest on the priority list first.
    for type_of_report in priority_list:
        for pdf_url in url_list:
            if type_of_report in pdf_url:
                priority_link = pdf_url
                break_epar_loop = True
                break
        if break_epar_loop:
            break

    # Go through all links, try to find the OMAR document
    for pdf_url in url_list:
        if "orphan-medicine-assessment-report" in pdf_url:
            omar_link = pdf_url
            break

    # gives a warning if it hasn't found an epar or omar document
    if priority_link == "" and omar_link == "":
        log.warning(f"No EPAR for {medicine_name}. The searched URLs are {url_list}")

    if priority_link == "" and omar_link != "":
        log.warning(f"No EPAR for {medicine_name}. The searched URLs are {url_list}")
        log.info(f"OMAR for {medicine_name} found. The searched URLs are {url_list}")

    if priority_link != "" and omar_link != "":
        log.info(f"OMAR for {medicine_name} found. The searched URLs are {url_list}")

    return priority_link, omar_link

# print(pdf_links_from_url(""))
