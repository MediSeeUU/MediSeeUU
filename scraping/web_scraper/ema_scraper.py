import logging
from datetime import datetime

import bs4
import regex as re
import requests
import scraping.web_scraper.utils as utils

log = logging.getLogger("web_scraper.ema_scraper")
html_parser_str = "html.parser"


def scrape_medicine_page(url: str, html_active: requests.Response) -> dict[str, str | list[str]]:
    """
    Given an url to an EMA medicine page, the method will return an EPAR, OMAR, and ODWAR in case they exist.
    All other market authorisation documents will also be returned as a list. The special files mentioned above
    are excluded from this list.

    Args:
        url (str): Link to the medicine page on the EMA website
        html_active (requests.Response): html object that contains html of the EMA page for a medicine

    Raises:
        Exception: If nothing is found, we throw an exception. This also passes all found URLs on newlines

    Returns:
        dict[str | list[str]: Dictionary of links to PDF files of interest from the EMA website.
    """
    # Last part of the url, contains the medicine name
    medicine_name: str = url.split('&')[0].split('/')[-1]

    # TODO: Graceful handling
    html_active.raise_for_status()

    soup = bs4.BeautifulSoup(html_active.text, html_parser_str)

    # The documents we search are under the header
    #   Initial marketing-authorisation documents
    # Element is in a <div><h4><span>text</span></h4> [pdfs here] </div>
    # Get parent thrice to find the tag that the PDFs are located in.
    # Parent of the found object is considered <span>

    complete_soup = soup.find(string="Initial marketing-authorisation documents")

    if complete_soup is None:
        log.warning(f"{medicine_name}: No initial marketing-authorisation documents")
        # Code relies on the attributes being present in the dictionary.
        # Fill with empty string for later code.
        return {
            "epar_url": "",
            "omar_url": "",
            "odwar_url": "",
            "other_ema_urls": []
        }

    specific_soup = complete_soup.parent.parent.parent

    link_tags = specific_soup.find_all('a')

    # Transform HTML elements into the urls from the href attribute
    url_list: list[str] = list(map(lambda a: a["href"], link_tags))

    # Files named 'public-assessment-report' will be the highest priority in the search.
    epar_priority_list: list[str] = [
        "public-assessment-report",
        "scientific-discussion",
        "procedural-steps-taken-authorisation"
    ]

    omar_priority_list: list[str] = [
        "orphan-maintenance-assessment-report",
        "orphan-medicine-assessment-report"
    ]

    odwar_priority_list: list[str] = [
        "orphan-designation-withdrawal-assessment-report"
    ]

    # Final dict that will be returned.
    # Filled with values here, last attribute "other_ema_urls" filled after
    result_dict: dict[str, str | list[str]] = {
        "epar_url": find_priority_link(epar_priority_list, url_list),
        "omar_url": find_priority_link(omar_priority_list, url_list),
        "odwar_url": find_priority_link(odwar_priority_list, url_list)
    }

    # All links that are not saved into the dictionary already
    result_dict["other_ema_urls"] = [link for link in url_list if link not in result_dict.values()]

    # Gives a warning if it hasn't found an epar or omar document
    if result_dict["epar_url"] == "":
        log.warning(f"{medicine_name}: No EPAR. Potential URLs are: {url_list}")

    return result_dict


def find_priority_link(priority_list: list[str], url_list: list[str]) -> str:
    """
    Finds the url with the highest priority in a list of urls

    Args:
        priority_list (list[str]): String that the url must contain. Strings with a lower index have higher priority
        url_list (list[str]): List of urls to be searched

    Returns:
        str: Return the highest priority url, or if it can't find it, an empty string

    """
    for type_of_report in priority_list:
        for url in url_list:
            if type_of_report in url:
                return url  # Success return condition

    return ""  # Failure return condition


def get_annex10_files(url: str, annex_dict: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    """
    Gets all the annex 10 files from the EMA website.

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
    html_active = utils.get_html_object(url)

    soup = bs4.BeautifulSoup(html_active.text, html_parser_str)

    start_year: int = 2005  # Starts looking for annex 10 files from this year,
    current_year: int = datetime.now().year  # up to the current year

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
            last_updated_site: datetime = find_last_updated_date_annex10(specific_soup.find_all('small')[1].get_text())

            # ignore files that have not changed since last time downloading
            if last_updated_local > last_updated_site:
                continue

        annex_dict[year_s] = {
            "last_updated": datetime.strftime(datetime.now(), '%d/%m/%Y'),
            "annex10_url": excel_link
        }

    return annex_dict


def find_last_updated_date(html_active: requests.Response) -> datetime:
    """
    Finds the date when a medicine page was last updated

    Args:
        html_active (requests.Response):
            html object that contains raw html for a webpage for a medicine on the EMA website

    Returns:
        datetime: When the medicine page on the EMA website was last updated
    """
    soup = bs4.BeautifulSoup(html_active.text, html_parser_str)
    last_updated_element = soup.find("meta", property="og:updated_time")["content"]
    last_updated_text = last_updated_element.split('T')[0]
    last_updated_datetime = datetime.strptime(last_updated_text, '%Y-%m-%d')
    return last_updated_datetime


def find_last_updated_date_annex10(text: str) -> datetime:
    """
    Converts a piece of text with information when an excel-sheet was last updated to a datetime object

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
