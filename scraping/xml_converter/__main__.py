from typing import TextIO

import fitz

from scraping.utilities.pdf import pdf_helper as ph
import scraping.utilities.definitions.xml_tags as tags
import logging
from os import path, listdir
import joblib
import multiprocessing

header_indicator = "|-HEADER-|"
log = logging.getLogger("xml_converter")


def convert_pdf_to_xml(source_filepath: str, output_filepath: str):
    """
    Creates a xml file of given pdf file in same directory

    Args:
        source_filepath (str): filepath to pdf file to convert to xml
        output_filepath (str): filepath to write xml converted file to
    """

    try:
        document: fitz.Document = fitz.open(source_filepath)
        text_format_lower = ph.get_text_format(document, True)
        paragraphs = get_marked_paragraphs(text_format_lower)
        sections = split_paragraphs(paragraphs)
        print_xml(sections, output_filepath, document.metadata["creationDate"], document.metadata["modDate"])
    except fitz.FileDataError:
        log.warning("XML CONVERTER: Could not open PDF: " + source_filepath)


def get_marked_paragraphs(lines: list[(str, float, str)]) -> list[str]:
    """
    Returns a list of paragraph strings based on input from get_text()

    Args:
        lines (list[(str, float, str)]): a list of pdf text line and
            font info tuple line_text: str, line_font_size: float, line_font_type: str)

    Returns:
        list[str]: list of paragraphs in the format of `bolded_text | -HEADER- | unbolded_text`
    """
    # concatenate list of lines into list of paragraphs and mark bolded lines
    paragraphs = []
    for line in lines:
        text = line[0]
        font_size = line[1]
        font_type = line[2]

        is_header = "Bold" in font_type and text.strip() != "" and font_size >= 8.5
        suffix = ""

        if is_header:
            suffix = header_indicator

        if is_header or len(paragraphs) == 0:
            paragraphs.append("")
        paragraphs.append(str(paragraphs.pop()) + text + suffix)

    return paragraphs


def split_paragraphs(paragraphs: list[str]) -> list[(str, str)]:
    """
    Returns a list of (header, paragraph) tuples from a list of paragraphs in
    format `bolded_text | -HEADER- | unbolded_text`, meant to take get_marked_paragraph's return value as input.

    Args:
        paragraphs (list[str]): a list of paragraphs in the format returned by
            get_marked_paragraphs: `bolded_text | -HEADER- | unbolded_text`

    Returns:
        list[(str, str)]: list of XML section text in form of (header, paragraph)
    """
    sections = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            continue

        paragraph_split = paragraph.split(header_indicator)
        header_text = paragraph_split[0]
        paragraph_text = ""

        if len(paragraph_split) > 1:
            paragraph_text = paragraph_split[1]

        sections.append((header_text, paragraph_text))

    return sections


def check_illegal(encoded_char: int) -> bool:
    """
    Checks whether a character is the range of illegal XML characters.
    Args:
        encoded_char (int): integer of a given character

    Returns:
        Whether given character is illegal
    """
    if 0x1000 <= encoded_char <= 0x8000:
        return True
    if 0xB000 <= encoded_char <= 0xC000:
        return True
    if 0xE000 <= encoded_char <= 0x1F00:
        return True
    if 0x7F00 <= encoded_char <= 0x8400:
        return True
    if 0x8600 <= encoded_char <= 0x9F00:
        return True
    if 0x0011 <= encoded_char <= 0x0015:
        return True
    other_illegal_chars = [0x0000, 0x0001, 0x0006, 0x0007, 0xEFFF, 0xFFFF]
    if encoded_char in other_illegal_chars:
        return True
    return False


def remove_illegal_characters(string: str) -> str:
    """
    Takes a string and returns a string where all special XML characters are replaced with their
    delimited version and all illegal UTF-8 characters removed.

    Args:
        string (str): input string to be converted to legal XML text

    Returns:
        str: legal XML text with special and illegal characters replaced
    """
    non_illegal_string = ""

    for character in string:
        if not character:
            continue

        match character:
            case '&':
                non_illegal_string += "&amp;"
                continue
            case '\"':
                non_illegal_string += "&quot;"
                continue
            case '\'':
                non_illegal_string += "&apos;"
                continue
            case '<':
                non_illegal_string += "&lt;"
                continue
            case '>':
                non_illegal_string += "&gt;"
                continue

        try:
            encoded_char = int.from_bytes(character.encode("utf-8", "ignore"), "big")
        except ValueError:
            continue

        if check_illegal(encoded_char):
            continue
        non_illegal_string += character

    return non_illegal_string


def print_xml_tag_open(xml_tag: str, file: TextIO, attribute: str = ""):
    """
    Prints xml_tag string to file as a xml opening tag with attribute: <xml_tag attribute>

    Args:
        xml_tag (str): XML tag to be printed, for example: "head", "body", "p". Should be imported from xml_tags.py.
        file (TextIO): File handle to write to. Obtained from open("filename", access_type).
        attribute (str, optional): Attributes to be added to opening tag. Defaults to "".
    """

    file.write("<" + xml_tag + attribute + ">")


def print_xml_tag_close(xml_tag: str, file: TextIO):
    """
    Prints xml_tag string to file as a closing xml tag with attribute: </xml_tag>

    Args:
        xml_tag (str): XML tag to be printed, for example: "head", "body", "p". Should be imported from xml_tags.py.
        file (TextIO): File handle to write to. Obtained from open("filename", access_type).
    """

    file.write("</" + xml_tag + ">")


def print_xml(sections: list[(str, str)], output_filepath: str, document_creation_date: str,
              document_modification_date: str):
    """
    Prints whole XML file output_filepath from the given list of section text tuples,
    with given document_creation_date and document_modification_date in metadata.

    Args:
        sections (list[str, str)]): List of section text tuples in form of (header_text, paragraph_text).
        output_filepath (str): Filepath of the file to be written in form of `*.xml`, where * is a wildcard.
        document_creation_date (str): Meta-data creation date of original pdf in string form from PyMuPDF.
        document_modification_date (str): Meta-data modification date of original pdf in string form from PyMuPDF.
    """
    # start printing xml file
    xml_file = open(output_filepath, "w", encoding="utf-8")

    xml_file.write("<?xml version=\"1.1\" encoding=\"UTF-8\" standalone=\"yes\"?>")
    print_xml_tag_open(tags.xml, xml_file)
    print_xml_head(document_creation_date, document_modification_date, output_filepath, xml_file)
    print_xml_body(sections, xml_file)
    print_xml_tag_close(tags.xml, xml_file)
    xml_file.close()


def print_xml_head(document_creation_date: str, document_modification_date: str, output_filepath: str,
                   xml_file: TextIO):
    """
    Prints entire XML head, writing it to output_filepath.
    Contains a given document_creation_date and document_modification_date from PDF metadata.

    Args:
        document_creation_date (str): Meta-data creation date of original pdf in string form from PyMuPDF.
        document_modification_date (str): Meta-data modification date of original pdf in string form from PyMuPDF.
        output_filepath (str): Filepath of the file to be written in form of `*.xml`, where * is a wildcard.
        xml_file (TextIO): File to write the XML tags to
    """
    print_xml_tag_open(tags.head, xml_file)
    print_xml_tag_open(tags.creation_date, xml_file)
    xml_file.write(document_creation_date)
    print_xml_tag_close(tags.creation_date, xml_file)
    print_xml_tag_open(tags.modification_date, xml_file)
    xml_file.write(document_modification_date)
    print_xml_tag_close(tags.modification_date, xml_file)
    # whether the original pdf was an initial authorization file
    print_xml_tag_open(tags.initial_authorization, xml_file)
    is_initial_file = output_filepath.split(".")[-2].split("_")[-1] == "0"
    xml_file.write(str(is_initial_file))
    print_xml_tag_close(tags.initial_authorization, xml_file)
    # original pdf name
    print_xml_tag_open(tags.pdf_file, xml_file)
    xml_file.write(path.basename(output_filepath).split(".")[0].strip() + ".pdf")
    print_xml_tag_close(tags.pdf_file, xml_file)
    print_xml_tag_close(tags.head, xml_file)


def print_xml_body(sections, xml_file):
    """
    Prints entire XML body, writing the PDF file contents as XML to output_filepath.

    Args:
        sections (list[str, str)]): List of section text tuples in form of (header_text, paragraph_text).
        xml_file (TextIO): File to write the XML tags to
    """
    print_xml_tag_open(tags.body, xml_file)
    for section in sections:
        section_header = remove_illegal_characters(section[0])
        section_paragraphs = remove_illegal_characters(section[1]).split("  ")

        # check if header contains paragraph number and fill header_attribute with the corresponding number
        split_header = section_header.strip().split()
        header_attribute = ""

        if split_header and all(character.isnumeric() or character == "." for character in split_header[0]):
            chapter_number_attribute = split_header[0]
            if chapter_number_attribute[-1] == ".":
                chapter_number_attribute = chapter_number_attribute[:-1]

            header_attribute = f" n=\"{chapter_number_attribute}\""

        # print the section from xml_elements taking sections and subsections into account
        print_xml_tag_open(tags.section, xml_file)
        print_xml_tag_open(tags.header, xml_file, header_attribute)
        xml_file.write(section_header.strip().encode("utf-8", "ignore").decode("utf-8", "ignore"))
        print_xml_tag_close(tags.header, xml_file)

        for section_paragraph in section_paragraphs:
            if section_paragraph.strip():
                print_xml_tag_open(tags.paragraph, xml_file)
                xml_file.write(section_paragraph.rstrip().encode("utf-8", "ignore").decode("utf-8", "ignore"))
                print_xml_tag_close(tags.paragraph, xml_file)

        print_xml_tag_close(tags.section, xml_file)
    print_xml_tag_close(tags.body, xml_file)


def convert_folder(directory: str):
    """
    Given a folder containing medicines, parse_folder walks creates an XML file for each PDF when it doesn't exist.
    After this, a parser for each pdf/xml file is called,
    writing a json file containing the scraped attributes to the folder.

    Args:
        directory: location of folder to parse
    """
    directory_files = [file for file in listdir(directory) if path.isfile(path.join(directory, file))]
    for file in directory_files:
        # Skip over all XML files and non-PDF files
        if ".xml" in file or ".pdf" not in file:
            continue
        # Skip file if XML is already created (temporary)
        if file[:len(file) - 4] + ".xml" in directory_files:
            continue

        file_path = path.join(directory, file)
        convert_pdf_to_xml(file_path, file_path[:len(file_path) - 4] + ".xml")


def main(directory: str):
    """
    Given a folder containing medicine folders, converts each PDF file to XML for all Annex files, EPARs and OMARs.

    Args:
        directory: data folder, containing medicine-category folders that contain the medicines
    """
    med_folders = []
    category_folders = [path.join(directory, folder) for folder in listdir(directory) if
                        path.isdir(path.join(directory, folder))]
    for category in category_folders:
        med_folders += [path.join(category, med_folder) for med_folder in listdir(category) if
                        path.isdir(path.join(category, med_folder))]

    # Use all the system's threads to maximize use of all hyper-threads
    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(convert_folder)(folder_name) for folder_name in med_folders)
