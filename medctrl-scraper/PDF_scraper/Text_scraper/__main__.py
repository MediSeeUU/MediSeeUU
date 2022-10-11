# import pdf_read as pdf_r
import parsers.annex_parser as ap
import parsed_info_struct as pis
from os import listdir
from os.path import isfile, join
from sys import platform
import json

# external files
import parsers.ec_parse as ec_parse
import parsers.epar_parse as epar_parse

# Main file to run all parsers

# TODO: Create dictionary per medicine
# datum toevoegen

#TODO: stub parse, fake function until other parsers are reworked
def parse_file(filename: str, medicine_struct: pis.parsed_info_struct):
    return medicine_struct

def datetime_serializer(date: pis.datetime.datetime):
    if isinstance(date, pis.datetime.datetime):
        return date.__str__()

def parse_pdf_folder(directory: str):
    # get foldername with platform check for slash type
    folder_name = ""
    filepath_splitter = ""
    if platform == "win32":
        folder_name = directory.split("\\")[-1]
        filepath_splitter = "\\"
    else:
        folder_name = directory.split("/")[-1]
        filepath_splitter = "/"

    # struct that contains all scraped attributes dicts as well as eu_number and date of parsing
    medicine_struct = pis.parsed_info_struct(folder_name)
    medicine_struct.eu_number = folder_name

    directory_files = [file for file in listdir(directory) if isfile(join(directory, file))]
    decision_files = [file for file in directory_files if "dec" in file]
    annex_files = [file for file in directory_files if "anx" in file]
    epar_files = [file for file in directory_files if "epar" in file]
    omar_files = [file for file in directory_files if "omar" in file]

    for file in decision_files:
        medicine_struct = parse_file(file, medicine_struct)
        
    for file in annex_files:
        medicine_struct = parse_file(file, medicine_struct)
        
    for file in epar_files:
        medicine_struct = parse_file(file, medicine_struct)
        
    for file in omar_files:
        medicine_struct = parse_file(file, medicine_struct)


    json_file = open(directory + filepath_splitter + folder_name + "_pdf_parser.json", "w")
    medicine_struct_json = json.dumps(pis.asdict(medicine_struct), default=datetime_serializer)
    json_file.write(medicine_struct_json)
    json_file.close()


parse_pdf_folder("D:\\Git_repos\\PharmaVisual\\medctrl-scraper\\PDF_scraper\\Text_scraper\\parsers\\test_data")
# pdf_r.parse_folder(ec_parse, 'dec_human')
#pdf_r.parse_folder(ec_parse, 'dec_orphan')
#pdf_r.parse_folder(epar_parse, 'epars')
# ap.parse_smpc_file("parsers/test_data/vydura-epar-public-assessment-report_en.pdf")

# To add: Xiao yi SMPC parsers
# To add: Elio's OMAR parsers
