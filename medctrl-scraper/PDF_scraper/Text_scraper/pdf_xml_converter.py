import sys
import fitz
import pdf_helper as ph

header_indicator = "|-HEADER-|"
split_indicator = "|-SPLIT-|"


def convert_pdf_to_xml(source_filepath: str, output_filepath: str, is_epar: bool):
    document = fitz.open(source_filepath)
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
    console_out = sys.stdout
    xml = open(output_filepath, "w", encoding="utf8")
    sys.stdout = xml

    print("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>")
    print("<xml>")
    print("<header>")
    print("</header>")
    print("<body>")

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
        print("<section>")
        print("<header" + header_attribute + ">")
        print(section_header.strip())
        print("</header>")

        for section_paragraph in section_paragraphs:
            if section_paragraph.strip() != "":
                print("<p>")
                print(section_paragraph.strip())
                print("</p>")

        print("</section>")

    print("</body>")
    print("</xml>")
    sys.stdout = console_out
