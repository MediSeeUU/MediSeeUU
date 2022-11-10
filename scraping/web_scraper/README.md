# Web Scraper


## General Function
The web scraper ensures that all relevant information about the medicine assessment process is retrieved from the internet. The scraper (currently) obtains information from two different sources: the website of the European Commission (EC) and the European Medicine Agency (EMA). The EC website has a unique page for each medicine that contains information about that medicine, supplemented with files (PDFs) that contain additional information about assessment procedures. In addition, there is also a link to the EMA website, which also has a separate page for that medicine, also with extra information and files.
There are 5 major python files that ensure that the information is extracted from these websites; ec_scraper.py, ema_scraper.py, download.py, filter_retry.py, and __main__.py.

### ec_scraper.py
The script for the EC website has two different functionalities. First, it fetches a list of medicines to scrape. For each of these medicines, a folder is created where the necessary information about the medicine is temporarily stored. In addition, the EC scraper actually ensures that all necessary information is retrieved from the EC website. This information consists of a number of data points for a medicine (attributes), links to additional procedure files (decisions and annexes) and links to the EMA website. The attributes of a medicines are stored in the aforementioned folder, in a JSON. The links to decision documents and annex documents for all medicines are stored in a single JSON (urls.json). This file also contains links to the EMA and the EMA scraper will add to this file too.

### ema_scraper.py
ema_scraper.py has a similar function as the scraper for the European Commission. It retrieves a number of attributes for each drug from the website itself, and it stores all links to files so that this list can be downloaded later. The attributes are included in the JSON per medicine, as are the links to EPAR and OMAR files in the urls JSON if they exist. A list of Annex 10 files must also be downloaded from the EMA website. A start has been made on this, but is not yet finished.

### download.py
The download script ensures that files in the JSON with links to files (scraped by ec_scraper.py and ema_scraper.py) are actually saved. It downloads any decision, annex, EPAR or OMAR file to the appropriate medicine folder. Any file that could not be downloaded is logged in a text file: failed.txt

### filter_retry.py
Based on the .txt file that the filter module provides to the web scraper, the files that could not be downloaded initially will get scraped and downloaded again. On default, the filter module runs three times.

### __main__.py
This script is what controls the entire web scraper. It can turn certain parts of the web scraper on and off so that it doesn't always run in its entirety. If everything is activated, the list of medicines to be scraped will first be scraped from the EC website. Subsequently, all necessary information for each of these medicines is retrieved from the EC website. This also contains links to the EMA website. The EMA website can then be scraped with these links. Finally, all links to files on the EC and EMA website are downloaded and after this the filter and download retry is called three times.


## Input & Output
This module, when first called, starts with no input. It retrieves all necessary information from the EC website, and can use it independently. A separate folder is created for each medicine where all information about that medicine is stored. All attributes that are taken directly from the EC and EMA websites are put in a JSON file. Also, all procedure files for a medicine are stored in that same folder when they are downloaded. The files in the folders are handled by the filter module. It is possible that the file that has been downloaded is corrupt, an html page, or an image. The filter lists all files that are not good and feeds it back to the web scraper so that these files can be downloaded again.
The good PDF files that are in the folders are handled by the PDF scraper, which in turn also retrieves attributes for medicines. The JSON with attributes taken directly from the website, the JSON with attributes from the pdf scraper, and JSONs from external sources are provided to the combiner so that inconsistent information can be properly stored in the database.

## Other important notes
This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.

© Copyright Utrecht University (Department of Information and Computing Sciences)
