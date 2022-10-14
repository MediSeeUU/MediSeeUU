from email import header
from pydoc import doc
import sys
import fitz
import pdf_helper as ph
import xml_tags as tags
from os import path

header_indicator = "|-HEADER-|"
split_indicator = "|-SPLIT-|"


def convert_pdf_to_xml(source_filepath: str, output_filepath: str):
    document = fitz.open(source_filepath)
    text_format_lower = ph.get_text_format(document, True)
    paragraphs = get_marked_paragraphs(text_format_lower)
    sections = split_paragraphs(paragraphs)
    print_xml(sections, output_filepath, document.metadata["creationDate"], document.metadata["modDate"])


def get_marked_paragraphs(lines: list[(str, float, str)]) -> list[str]:
    # concatinate list of lines into list of paragraphs and mark bolded lines
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


def replace_special_xml_characters(string: str) -> str:
    string = string.replace("&", "&amp;")
    string = string.replace("\"", "&quot;")
    string = string.replace("\'", "&apos;")
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt;")

    return string


def print_xml_tag_open(xml_tag: str, attributes: str = ""):
    print("<" + xml_tag + attributes + ">")


def print_xml_tag_close(xml_tag: str):
    print("</" + xml_tag + ">")


def print_xml(sections: list[(str, str)], output_filepath: str, document_creation_date: str, document_modification_date: str):
    # start printing xml file
    console_out = sys.stdout
    xml = open(output_filepath, "w", encoding="utf-8")
    sys.stdout = xml

    print("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>")
    print_xml_tag_open(tags.xml)
    print_xml_tag_open(tags.head)

    print_xml_tag_open(tags.creation_date)
    print(document_creation_date)
    print_xml_tag_close(tags.creation_date)

    print_xml_tag_open(tags.modification_date)
    print(document_modification_date)
    print_xml_tag_close(tags.modification_date)

    # whether the original pdf was an initial authorization file
    print_xml_tag_open(tags.initial_authorization)
    is_initial_file = output_filepath.split(".")[0].split("_")[-1] == "0"
    print(str(is_initial_file))
    print_xml_tag_close(tags.initial_authorization)

    # original pdf name
    print_xml_tag_open(tags.pdf_file)
    print(path.basename(output_filepath).split(".")[0].strip() + ".pdf")
    print_xml_tag_close(tags.pdf_file)

    print_xml_tag_close(tags.head)
    print_xml_tag_open(tags.body)

    for section in sections:
        section_header = replace_special_xml_characters(section[0])
        section_paragraphs = replace_special_xml_characters(section[1]).split("  ")

        # check if header contains paragraph number and fill header_attribute with the corresponding number
        split_header = section_header.strip().split()
        header_attribute = ""

        if all(character.isnumeric() or character == "." for character in split_header[0]):
            chapter_number_attribute = split_header[0]
            if chapter_number_attribute[-1] == ".":
                chapter_number_attribute = chapter_number_attribute[:-1]

            header_attribute = " n=\"" + chapter_number_attribute + "\""

        # print the section from xml_elements taking sections and subsections into account
        print_xml_tag_open(tags.section)
        print_xml_tag_open(tags.header, header_attribute)
        print(section_header.strip())
        print_xml_tag_close(tags.header)

        for section_paragraph in section_paragraphs:
            if section_paragraph.strip() != "":
                print_xml_tag_open(tags.paragraph)
                print(section_paragraph.rstrip().encode('utf-8', 'ignore'))
                print_xml_tag_close(tags.paragraph)

        print_xml_tag_close(tags.section)

    print_xml_tag_close(tags.body)
    print_xml_tag_close(tags.xml)
    sys.stdout = console_out
