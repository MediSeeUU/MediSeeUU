"""Install SEND reader"""
from setuptools import find_packages, setup

setup(
    name="regsci_scraper",
    version="0.0.1",
    packages=find_packages(),
    author="Stefan Verweij",
    author_email="s.verweij@cbg-meb.nl",
    description="Scraper for the Regulatory Science database",
    url="",
    install_requires=[
        "xlrd",
        "requests",
        "loguru",
        "pandas",
        "openpyxl",
        "tabula-py",
        "camelot-py",
        "opencv-python",
        "tika",
        "PyMuPDF",
        "PyPDF4",
        "pytesseract",
        "pdf2image"
    ]
)
