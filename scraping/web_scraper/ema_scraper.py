from csv import excel
from datetime import datetime
from time import strptime
from turtle import update
import requests
import logging
import bs4
import regex as re

log = logging.getLogger("webscraper.ema_scraper")


def pdf_links_from_url(url: str) -> str:
    """ Gets the pdf link on the EMA website that is highest on the priority list

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
    specific_soup = soup.find(string="Initial marketing-authorisation documents").parent.parent.parent

    # Compiles a list of all link tags, that link to a .pdf file.
    link_tags = specific_soup.find_all('a')

    # Get all links to pdf files from the
    url_list: list[str] = list(map(lambda a: a["href"], link_tags))

    # Files named 'public-assessment-report' will be the highest priority in the search.
    priority_list = ["public-assessment-report", "scientific-discussion", "procedural-steps-taken-authorisation"]

    # Go through all links, try to find the document that is the highest on the priority list first.
    for type_of_report in priority_list:
        for pdf_url in url_list:
            if type_of_report in pdf_url:
                return pdf_url

    log.warning(f"No EPAR for {medicine_name}. The searched URLs are {url_list}")
    return ""


def get_annex10_files(url: str, annex_dict: dict[int, dict[str, str]]) -> dict[int, dict[str, str]]:
    """_summary_

    Args:
        url (str): _description_
    """
    html_obj = requests.get(url)

    # TODO: Graceful handling
    html_obj.raise_for_status()

    soup = bs4.BeautifulSoup(html_obj.text, "html.parser")
    # TODO: change so that it updates current year automatically
    current_year: int = 2022
    year_iterator: int = 2005
    
    # Checks for each year if there is an annex 10 excel file and if the excel link needs to be updated
    while year_iterator <= current_year:
        complete_soup = soup.find(string=re.compile(f"Annex 10 (?:-|–) {year_iterator} annual report.*"))

        if complete_soup != None:
            specific_soup = complete_soup.parent.parent.parent
        else:
            year_iterator += 1
            continue

        excel_link = specific_soup["href"]

        if str(year_iterator) in annex_dict:
            last_updated_local: datetime = datetime.strptime(annex_dict[str(year_iterator)]["last_updated"], '%d/%m/%Y')
            last_updated_site: datetime = find_last_updated_date(specific_soup.find_all('small')[1].get_text())   

            if last_updated_local > last_updated_site:
                year_iterator += 1
                continue

        annex_dict[str(year_iterator)] = {
            "last_updated": datetime.strftime(datetime.now(), '%d/%m/%Y'),
            "annex10_url": excel_link
        }

        year_iterator += 1

    return annex_dict


def find_last_updated_date(text: str) -> datetime:
    new_text: list[str] = text.split()

    if len(new_text) > 3:
        updated_date: str = new_text[5]
    else:
        updated_date: str = new_text[2]

    return datetime.strptime(updated_date, '%d/%m/%Y')
# print(pdf_links_from_url(""))
