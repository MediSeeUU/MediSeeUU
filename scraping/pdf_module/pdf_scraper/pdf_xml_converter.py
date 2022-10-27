from operator import is_
import sys
from typing import TextIO
import fitz
import scraping.pdf_module.pdf_scraper.pdf_helper as ph
import scraping.pdf_module.pdf_scraper.xml_tags as tags
from os import path
import re

header_indicator = "|-HEADER-|"


def convert_pdf_to_xml(source_filepath: str, output_filepath: str):
    """
    Creates a xml file of given pdf file in same directory

    Args:
        source_filepath (str): filepath to pdf file to convert to xml
        output_filepath (str): filepath to write xml converted file to

    Returns:
        None
    """

    document = []
    try:
        document = fitz.open(source_filepath)
        text_format_lower = ph.get_text_format(document, True)
        paragraphs = get_marked_paragraphs(text_format_lower)
        sections = split_paragraphs(paragraphs)
        print_xml(sections, output_filepath, document.metadata["creationDate"], document.metadata["modDate"])
    except fitz.FileDataError:
        print("XML CONVERTER: Could not open PDF: " + source_filepath)


def get_marked_paragraphs(lines: list[(str, float, str)]) -> list[str]:
    """
    Returns a list of paragraph strings based on input from get_text()

    Args:
        lines (list[(str, float, str)]): a list of pdf text line and
        font info tuple line_text: str, line_font_size: float, line_font_type: str)

    Returns:
        list[str]: list of paragraphs in the format of "bolded_text | -HEADER- | unbolded_text"
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
    format "bolded_text | -HEADER- | unbolded_text", meant to take get_marked_paragraph's return value as input.

    Args:
        paragraphs (list[str]): a list of paragraphs in the format returned by 
            get_marked_paragraphs\: "bolded_text | -HEADER- | unbolded_text"

    Returns:
        list[(str, str)]: list of XML section text in form of (header, paragraph)
    """    
    sections = []

    for paragraph in paragraphs:
        if paragraph.strip() == "":
            continue

        paragraph_split = paragraph.split(header_indicator)
        header_text = paragraph_split[0]
        paragraph_text = ""

        if len(paragraph_split) > 1:
            paragraph_text = paragraph_split[1]

        sections.append((header_text, paragraph_text))

    return sections


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
        if character == '':
            continue

        try:
            encoded_char = int.from_bytes(character.encode("utf-8", "ignore"), "big")
        except ValueError:
            continue

        if character == "&":
            non_illegal_string += "&amp;"
            continue

        if character == "\"":
            non_illegal_string += "&quot;"
            continue

        if character == "\'":
            non_illegal_string += "&apos;"
            continue

        if character == "<":
            non_illegal_string += "&lt;"
            continue

        if character == ">":
            non_illegal_string += "&gt;"
            continue

        if 0x1000 <= encoded_char <= 0x8000:
            continue

        if 0xB000 <= encoded_char <= 0xC000:
            continue

        if 0xE000 <= encoded_char <= 0x1F00:
            continue

        if 0x7F00 <= encoded_char <= 0x8400:
            continue

        if 0x8600 <= encoded_char <= 0x9F00:
            continue

        if 0x0011 <= encoded_char <= 0x0015 or 0x0006 <= encoded_char <= 0x0007 or encoded_char == 0x0001:
            continue

        if encoded_char == 0x0000 or encoded_char == 0xEFFF or encoded_char == 0xFFFF:
            continue

        non_illegal_string += character

    return non_illegal_string


def print_xml_tag_open(xml_tag: str, file: TextIO, attributes: str = ""):
    file.write("<" + xml_tag + attributes + ">")


def print_xml_tag_close(xml_tag: str, file: TextIO):
    file.write("</" + xml_tag + ">")


def print_xml(sections: list[(str, str)], output_filepath: str, document_creation_date: str,
              document_modification_date: str):
    # start printing xml file
    console_out = sys.stdout
    xml_file = open(output_filepath, "w", encoding="utf-8")

    xml_file.write("<?xml version=\"1.1\" encoding=\"UTF-8\" standalone=\"yes\"?>")
    print_xml_tag_open(tags.xml, xml_file)
    print_xml_tag_open(tags.head, xml_file)

    print_xml_tag_open(tags.creation_date, xml_file)
    xml_file.write(document_creation_date)
    print_xml_tag_close(tags.creation_date, xml_file)

    print_xml_tag_open(tags.modification_date, xml_file)
    xml_file.write(document_modification_date)
    print_xml_tag_close(tags.modification_date, xml_file)

    # whether the original pdf was an initial authorization file
    print_xml_tag_open(tags.initial_authorization, xml_file)
    is_initial_file = output_filepath.split(".")[0].split("_")[-1] == "0"
    xml_file.write(str(is_initial_file))
    print_xml_tag_close(tags.initial_authorization, xml_file)

    # original pdf name
    print_xml_tag_open(tags.pdf_file, xml_file)
    xml_file.write(path.basename(output_filepath).split(".")[0].strip() + ".pdf")
    print_xml_tag_close(tags.pdf_file, xml_file)

    print_xml_tag_close(tags.head, xml_file)
    print_xml_tag_open(tags.body, xml_file)

    for section in sections:
        section_header = remove_illegal_characters(section[0])
        section_paragraphs = remove_illegal_characters(section[1]).split("  ")

        # check if header contains paragraph number and fill header_attribute with the corresponding number
        split_header = section_header.strip().split()
        header_attribute = ""

        if split_header:
            if all(character.isnumeric() or character == "." for character in split_header[0]):
                chapter_number_attribute = split_header[0]
                if chapter_number_attribute[-1] == ".":
                    chapter_number_attribute = chapter_number_attribute[:-1]

                header_attribute = " n=\"" + chapter_number_attribute + "\""

        # print the section from xml_elements taking sections and subsections into account
        print_xml_tag_open(tags.section, xml_file)
        print_xml_tag_open(tags.header, xml_file, header_attribute)
        xml_file.write(section_header.strip().encode("utf-8", "ignore").decode("utf-8", "ignore"))
        print_xml_tag_close(tags.header, xml_file)

        for section_paragraph in section_paragraphs:
            if section_paragraph.strip() != "":
                print_xml_tag_open(tags.paragraph, xml_file)
                xml_file.write(section_paragraph.rstrip().encode("utf-8", "ignore").decode("utf-8", "ignore"))
                print_xml_tag_close(tags.paragraph, xml_file)

        print_xml_tag_close(tags.section, xml_file)

    print_xml_tag_close(tags.body, xml_file)
    print_xml_tag_close(tags.xml, xml_file)
    xml_file.close()
