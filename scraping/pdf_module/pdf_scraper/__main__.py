import parsers.annex_parser as ap
import parsed_info_struct as pis
from os import listdir
import os.path as path
import json
import pdf_xml_converter as xml_converter
import joblib
import multiprocessing

# external parsers
import parsers.ec_parse as ec_parse
import parsers.epar_parse as epar_parse
import parsers.omar_parse as omar_parse


# Main file to run all parsers
def main(directory: str):
    print("Parsing PDF files")
    directory_folders = [folder for folder in listdir(directory) if path.isdir(path.join(directory, folder))]

    # Use all the system's threads to maximize use of all hyper-threads
    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(parse_folder)(path.join(directory, folder_name), folder_name) for folder_name in
        directory_folders)
    print("Done!")

    # Single-threaded parsing
    # for folder in directory_folders:
    #     parse_folder(path.join(directory, folder), folder)


# scraping on medicine folder level
def parse_folder(directory: str, folder_name):
    # struct that contains all scraped attributes dicts as well as eu_number and date of parsing
    medicine_struct = pis.parsed_info_struct(folder_name)

    # do xml conversion on annex, epar and omar files
    directory_files = [file for file in listdir(directory) if path.isfile(path.join(directory, file))]
    for file in directory_files:
        # Skip over all decision files, XML files, and non-pdf files
        if "dec" in file or ".xml" in file or ".pdf" not in file:
            continue
        # Skip file if XML is already created (temporary)
        # if file[:len(file) - 4] + ".xml" in directory_files:
        #     continue
        file_path = path.join(directory, file)
        xml_converter.convert_pdf_to_xml(file_path, file_path[:len(file_path) - 4] + ".xml")

    # update list of files and filter out relevant files for each parser
    directory_files = [file for file in listdir(directory) if path.isfile(path.join(directory, file))]
    decision_files = [file for file in directory_files if "dec" in file and ".xml" not in file]
    annex_files = [path.join(directory, file) for file in directory_files if "anx" in file and ".xml" in file]
    epar_files = [file for file in directory_files if
                  ("public-assessment-report" in file or "procedural-steps-taken" in file) and ".xml" in file]
    omar_files = [file for file in directory_files if "omar" in file and ".xml" in file]

    # call scrapers on correct files and update medicine struct
    medicine_struct = run_scrapers(annex_files, decision_files, directory, epar_files, medicine_struct, omar_files)

    # dump json result to medicine folder directory
    json_file = open(path.join(directory, folder_name) + "_pdf_parser.json", "w")
    medicine_struct_json = json.dumps(pis.asdict(medicine_struct), default=datetime_serializer)
    json_file.write(medicine_struct_json)
    json_file.close()


# scraping all XML or PDF files and updating medicine_struct with the scraped attributes
def run_scrapers(annex_files, decision_files, directory, epar_files, medicine_struct, omar_files):
    for file in decision_files:
        medicine_struct = ec_parse.parse_file(file, directory, medicine_struct)
    for file in annex_files:
        medicine_struct = ap.parse_file(file, medicine_struct)
    for file in epar_files:
        medicine_struct = epar_parse.parse_file(file, directory, medicine_struct)
    for file in omar_files:
        medicine_struct = omar_parse.parse_file(file, directory, medicine_struct)
    return medicine_struct


# datetime to string serializer for json dumping
def datetime_serializer(date: pis.datetime.datetime):
    if isinstance(date, pis.datetime.datetime):
        return date.__str__()


if __name__ == "__main__":
    main('..\..\..\data')
