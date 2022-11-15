"""
Parsers module contains files that can scrape a PDF or XML file. Each scraper can scrape one PDF type.

annex_parser.py can get all attributes from annex XML files (converted by XML converter)
dec_parser.py can get all attributes from decision PDF files
epar_parser.py can get all attributes from EPAR XML files (converted by XML converter)
omar_parser.py can get all attributes from OMAR XML files (converted by XML converter)

Running one of these parsers results in an updated medicine_struct in __main__.py
"""