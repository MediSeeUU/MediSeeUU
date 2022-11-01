import logging
from datetime import datetime

import bs4
import regex as re
import requests

log = logging.getLogger("webscraper.ema_scraper")


def pdf_links_from_url(url: str) -> tuple[str, str]:
    """
    Gets the pdf link on the EMA website that is the highest on the priority list
    and a link to the OMAR document if it exists

    Args:
        url (str): Link to the medicine page on the EMA website

    Raises:
        Exception: If nothing is found, we throw an exception. This also passes all found URLs on newlines

    Returns:
        str: The pdf link that is the highest on the priority list
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

    if complete_soup is not None:
        specific_soup = complete_soup.parent.parent.parent
    else:
        log.warning(f"There are no initial marketing-authorisation documents")
        return "", ""

    # Compiles a list of all link tags, that link to a .pdf file.
    link_tags = specific_soup.find_all('a')

    # Get all links to pdf files from the
    url_list: list[str] = list(map(lambda a: a["href"], link_tags))

    # Files named 'public-assessment-report' will be the highest priority in the search.
    priority_list: list[str] = [
        "public-assessment-report",
        "scientific-discussion",
        "procedural-steps-taken-authorisation"
    ]
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


def get_annex10_files(url: str, annex_dict: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    """ Gets all the annex 10 files from the EMA website.

    The website is scraped for all annex 10 files. Whenever this scraper runs, it checks whether it has to
    update the links in the dictionary, based on whether the document on the site was updated or not. It also
    adds new links to the Excel documents if it finds these

    Args:
        url (str): Link to the EMA website that contains all annex 10 files
        annex_dict (dict[int, dict[str, str]]): Dictionary that contains links to the annex files per year
            and when they were last updated

    Returns:
        dict[int, dict[str, str]]: Amended annex_dict
    """
    html_obj = requests.get(url)

    # TODO: Graceful handling
    html_obj.raise_for_status()

    soup = bs4.BeautifulSoup(html_obj.text, "html.parser")
        
    start_year: int = 2005                       # Starts looking for annex 10 files from this year,
    current_year: int = datetime.now().year         # up to the current year
    
    # Checks for each year if there is an annex 10 Excel file and if the Excel link needs to be updated
    for year in range(start_year, current_year + 1):
        # Get the element that contains annex 10 text
        complete_soup = soup.find(string=re.compile(f"Annex 10 (?:-|–) {year} annual report.*"))

        if complete_soup is None:
            continue

        specific_soup = complete_soup.parent.parent.parent

        excel_link = specific_soup["href"]

        # If the annex 10 link for the current year is already in the dictionary, it checks when it was last updated on
        # the site. It compares this when the dictionary was last updated. If the site was updated after the dictionary,
        # the dictionary needs to be updated with the new link. Also, new entries must always be added
        year_s = str(year)
        if year_s in annex_dict.keys():
            last_updated_local: datetime = datetime.strptime(annex_dict[year_s]["last_updated"], '%d/%m/%Y')
            last_updated_site: datetime = find_last_updated_date(specific_soup.find_all('small')[1].get_text())

            # ignore files that have not changed since last time downloading
            if last_updated_local > last_updated_site:
                continue

        annex_dict[year_s] = {
            "last_updated": datetime.strftime(datetime.now(), '%d/%m/%Y'),
            "annex10_url": excel_link
        }

    return annex_dict


def find_last_updated_date(text: str) -> datetime:
    """ Converts a piece of text with information when an excel-sheet was last updated to a datetime object

    Args:
        text (str): text containing information when it was last updated.

    Returns:
        datetime: When the excel-sheet was last updated
    """
    # Removes all whitespaces from the text, and splits the words in a list
    new_text: list[str] = text.split()

    # When the document has updated somewhere over the years been updated, it has more than three words in the list.
    # Otherwise, the original upload date is taken
    if len(new_text) > 3:
        updated_date: str = new_text[5]
    else:
        updated_date: str = new_text[2]

    return datetime.strptime(updated_date, '%d/%m/%Y')


# print(pdf_links_from_url(""))
