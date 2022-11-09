"""
This program scans all PDF files in the given directory.
Sometimes, the content of a PDF file is not correct.
This program therefore creates a log file (filter.txt) that saves the actual type of each erroneous PDF file:
An image, a HTML webpage, or a corrupt PDF in other cases.

This file can be used by the webscraper to check for corrupt PDF files,
as this allows the web scraper to try to scrape these files again.

The other non-PDF files will be scraped during the next automatic web scraper run. (I.E. Next week)
"""