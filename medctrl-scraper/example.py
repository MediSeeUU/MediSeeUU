import pytesseract
import pandas as pd

import sys
sys.path.append('regsci_db/src')
from regsci_scraper import pdf_scraper as ps

""" THE SCRAPING: This will not be used for now as it takes a while to scrape everything. We will instead import the scraped data from the exact same Excel sheet.

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
db = ps.RegSciDB(directory_path = "regsci_db/data")  # directory_path = path to the map containing all the PDF files as has been mentioned above
db.ec_df  # <-- the DB in a Pandas DF
"""

ec_df = pd.read_excel('output.xlsx') # Scraped data
