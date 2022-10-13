from pydoc import doc
import sys
import fitz
import pdf_helper as ph
from os import path

header_indicator = "|-HEADER-|"
split_indicator = "|-SPLIT-|"


def convert_pdf_to_xml(source_filepath: str, output_filepath: str, is_epar: bool):
    document = fitz.open(source_filepath)
    # document_creation_date = document.metadata["creationDate"]
    # document_modification_date= document.metadata["modDate"]
    # print(type(document_creation_date))
    # print(document_modification_date)
    # print(document)
    text_format_lower = ph.get_text_format(document, True)
    clean_lines = cleanup_lines(text_format_lower, is_epar)
    paragraphs = get_marked_paragraphs(clean_lines)
    sections = split_paragraphs(paragraphs)
    print_xml(sections, output_filepath)


def cleanup_lines(text_format_lower: list[(str, float, str)], is_epar: bool) -> list[(str, float, str)]:
    # skip initial pages until table of content
    if is_epar:
        while "table of content" not in text_format_lower[0][0]:
            del text_format_lower[0]

            if len(text_format_lower) == 0:
                break

    return text_format_lower


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


def print_xml(sections: list[(str, str)], output_filepath: str):
    # start printing xml file
    # console_out = sys.stdout
    xml_file = open(output_filepath, "w", encoding="utf8")
    # sys.stdout = xml_file

    xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n")
    xml_file.write("<xml>\n")
    xml_file.write("<header>\n")

    xml_file.write("<initial>\n")
    is_initial_file = output_filepath.split(".")[0].split("_")[-1] == "0"
    xml_file.write(str(is_initial_file) + "\n")
    xml_file.write("</initial>\n")

    xml_file.write("<pdf>\n")
    xml_file.write(path.basename(output_filepath).split(".")[0] + ".pdf\n")
    xml_file.write("</pdf>\n")

    xml_file.write("</header>\n")

    xml_file.write("<body>\n")

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

        # xml_file.write the section to xml file taking header number into account
        xml_file.write("<section>\n")
        xml_file.write("<header" + header_attribute + ">\n")
        xml_file.write(section_header.strip() + "\n")
        xml_file.write("</header>\n")

        for section_paragraph in section_paragraphs:
            if section_paragraph.strip() != "":
                xml_file.write("<p>\n")
                xml_file.write(section_paragraph.strip() + "\n")
                xml_file.write("</p>\n")

        xml_file.write("</section>\n")

    xml_file.write("</body>\n")
    xml_file.write("</xml>\n")
    xml_file.close()
    # sys.stdout = console_out
