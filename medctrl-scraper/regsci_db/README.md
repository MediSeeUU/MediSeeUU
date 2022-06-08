<!-- This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) -->
# Regulatory Science Database
#### *Scripts for web & PDF scraping* 

## Description
This project contains A) scripts for Webscraping the EC Community Register and the EMA website and B) scripts for filescraping the PDF files that have been scraped in step A (Authorisation Decisions, EPARs, SmPCs, "Scientific information" files and "Procedural steps before authorisation" files).

## Installation (local)
This project is tested on `Ubuntu 20.04 LTS` using `Python3.8` and `jupyter-notebook`. The following `Python3` packages where used:

- `beautifulsoup4 4.9.3`; `camelot-py 0.10.1`; `loguru 0.5.3`; `opencv-python 4.5.3.56`; `openpyxl 3.0.7`; 
`pandas 1.3.0`; `pdf2image 1.16.0` `PyMuPDF 1.18.15`; `PyPDF4 1.27.0`; `pytesseract 0.3.8`; `requests 2.26.0`; `tabula-py 2.2.0`;
`tika 1.24` ; `xlrd 2.0.1` 

(Only tested on Linux/Ubuntu, but should work on Windows as well)
1. Open the command terminal 
2. Go to the repository and go to the `src` dir (something like `cd ./src/` on Linux)
3. Install the package using `python3 setup.py install`

When creating the database, your project should have the following structure containing the `data` directory where the `pdf` files will be saved:
```
+-- src
+-- data
|   +-- authorisation_decisions
    |   +-- 100.pdf
|   +-- smpcs
    |   +-- 100.pdf
|   +-- epars
    |   +-- 100.pdf
```

## Usage
You can create the database by running the following line of code:
```python
from regsci_scraper import pdf_scraper as ps

db = ps.RegSciDB(directory_path = "~/xxx/data/")  # directory_path = path to the map containing all the PDF files as has been mentioned above
db.ec_df  # <-- the DB in a Pandas DF
```

The script will run in the following order:
1. Scraping the EC Community Website table "[Union Register of medicinal products for human use](https://ec.europa.eu/health/documents/community-register/html/)"
2. Scraping the [individual product pages](https://ec.europa.eu/health/documents/community-register/html/h1539.htm) on the EC Community website.
  a. Downloading the authorisation decisions to `"~/xxx/data/authorisation_decisions/"`
  b. Downloading the SmPC annexes to `"~/xxx/data/smpcs/"`
(?) __TO BE IMPLEMENTED__ Use the `website_scraper.execute_download_pooling()` function to download the EPARs, "Scientific Information" files and "Procedural steps before authorisation" files   
3. Compare and confirm the EMA numbers with the [Excel file](https://www.ema.europa.eu/sites/default/files/Medicines_output_european_public_assessment_reports.xlsx) on the EMA website
4. Scrape the Authorisation Decisions using the `DecisionMiner` class.
5. Scrape the SmPC annexes using the `SmPCMiner` class.
6. Scrape the EPARs, "Scientific Information" and "Procedural steps before authorisation" files using `RegSciDB.get_epar_vars()`
7. Merge all data to the `ec_df` attribute of the `RegSciDB` class.

## Contents
`src`: This directory contains the `regsci_scraper` package (and a `setup.py` and `__init__.py` for setup). 
The package contains the following scripts:
- `utils.py`: Script containing general functions used by the other scripts mentioned below.
- `pdf_scraper.py`: __Main script__. Uses the `website_scraper.py` and scripts in `file_scrapers` to create the DB.
- `website_scraper.py`: Scripts for scraping the EC and EMA website (based on J. Hoekman's `Overview_v1.0.R`).
- `file_scrapers`: directory with the following file scraping scripts:
  - `decision_miner.py`: Script for mining the authorisation decisions.
  - `smpc_miner.py`: ,, SmPCs.
  - `epar_miner.py`: ,, EPARs.
  - `table_scraper.py`: __[curently outdated]__ Script for mining tables from PDF files.
  - `__init__.py`: Necessary for setup.
- `__init__.py`: Necessary for setup.

## Authors and acknowledgment
The scrips have been written by S. Verweij ([s.verweij@cbg-meb.nl](mailto:s.verweij@cbg-meb.nl)) with the help of J. Hoekman ([J.Hoekman@uu.nl](mailto:J.Hoekman@uu.nl)) and L.T. Bloem ([L.T.Bloem@uu.nl](mailto:L.T.Bloem@uu.nl)).

## Project status
(February 2022) This project is still under development.
