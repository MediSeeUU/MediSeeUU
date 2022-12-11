# Scraper and Dashboard to make data on regulation of medicines openly available

[Documentation can be viewed online here](https://mediseeuu.github.io/MediSeeUU/)

## How to install

Install python 3.10.7.
All the dependencies for the scraping modules are in the requirements.txt file in the scraping folder. Use `pip install -r requirements.txt` in the scraping folder to install these dependencies.

## How to use

### To run the whole scraping program:
- Either: Run the `__main__.py` in the scraping folder using PyCharm after installing the dependencies.
- Or: Execute run-scraping.bat. This will also install any dependencies that have not yet been installed.

### To run a module in scraping:
Comment out all the modules you don’t want to run in the `__main__.py` file in the scraping folder.
Execute program as stated above.

### To run the frontend (dashboard) and backend:
Follow the instructions in their respective documentations.
<TODO: Add link to install instructions, or place them here.>

## Functionality

The program delivered creates the discussed folder structure and fills it with pdf, xml and json files.

Currently, the program has most of its functionality within the web scraper, filter, xml converter and pdf scraper
modules. This means that all files up until pdf_data.json from the diagram below are made. 

Combiner is still a work in progress and will not create a json file containing useful information.
The database communicator has functionality built in but will not communicate with the back-end 
since no useful data is being generated from the combiner module.

## Architecture Diagram

![architecture diagram](docs/architecture_diagram.svg "Architecture Diagram")

## Modules

- web_scraper: This module is responsible for scraping information from the appropriate websites. 
- This includes information from the website itself, and PDFs located on the websites. A JSON file is provided containing general information that is present on the websites themselves.
- filter: This module keeps track of a list of PDFs that were not successfully scraped. This list is then given back to the web_scraper to make a new attempt at scraping these files.
- pdf_parser: This module uses the xml_converter create PDF files, which are used to create a JSON file that contains attributes that were parsed from every XML file.
- xml_converter: This module creates an XML file for every PDF file.
- combiner: This module merges the JSONs from the web_scraper and pdf_parser into an easily read JSON. 
- db_uploader: The module takes the JSON from the combiner and passes it onto the backend.
- backend: The backend is responsible for communication with the frontend (the dashboard) and the database. Making sure that the data is passed on properly.
- frontend: The frontend, also known as the dashboard, runs a website displaying all data in both textual form and as visualizations.

## Copyright statement

This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.

© Copyright Utrecht University (Department of Information and Computing Sciences)
