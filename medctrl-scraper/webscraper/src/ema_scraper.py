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

    # Compiles a list of all link tags, that link to a .pdf file.
    link_tags = soup.findAll('a', href=re.compile(r"en.pdf"))

    # Get all links to pdf files from the
    link_list = list(map(lambda a: a["href"], link_tags))

    # Find the assessment report
    assessment_reports = list(filter(lambda x: "public-assessment-report" in x, link_list))

    if len(assessment_reports) == 0:
        print(f"No PDF for {medicine_name}")
        return []

    print("debug stop point")


pdf_links_from_url("https://www.ema.europa.eu/en/medicines/human/EPAR/abraxane")
