import sys
import fitz
import PDFhelper as ph

header_indicator = "|-HEADER-|"
split_indicator = "|-SPLIT-|"


def remove_all_substring(substring: str, text: str):
    while substring in text:
        text.remove(substring)

    return text

def flags_decomposer(flags):
    """Make font flags human readable."""
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
    if flags & 2 ** 2:
        l.append("serifed")
    else:
        l.append("sans")
    if flags & 2 ** 3:
        l.append("monospaced")
    else:
        l.append("proportional")
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)


def convert_pdf_to_xml(source_filepath: str, output_filepath: str, is_epar: bool):
    document = fitz.open(source_filepath)
    text_format_lower = ph.getTextFormat(document, True)
    clean_lines = cleanup_lines(text_format_lower, is_epar)
    paragraphs = get_marked_paragraphs(clean_lines)
    # paragraphs = preprocess_paragraphs(paragraphs)
    print_xml(paragraphs, output_filepath)

def cleanup_lines(text_format_lower: str, is_epar: bool):
    # skip inital pages until table of content
    if is_epar:
        while "table of content" not in text_format_lower[0][0]:
            del text_format_lower[0]
        
            if len(text_format_lower) == 0:
                break
    
    lines = []
    index = 0
    while index < len(text_format_lower) - 3:
        line = text_format_lower[index]
        text = line[0]
        font_size = line[1]
        font_type = line[2]
        font_type_header_text = text_format_lower[index + 2][2]
        is_chapter_number = all(character.isnumeric() or character == "." for character in text.strip()) and "Bold" in font_type and "Bold" in font_type_header_text

        if is_chapter_number:
            chapter_number = text.strip()
            chapter_text = text_format_lower[index + 2][0]
            mergedline = (chapter_number + " " + chapter_text, font_size, font_type)
            lines.append(mergedline)
            index += 3

        else:
            # if not ("Bold" in font_type and text.strip() == ""):
            lines.append(line)
            index += 1

    for line in text_format_lower:
        print(line)

    return lines

def get_marked_paragraphs(lines: str):
    # concatinate list of lines into list of paragraphs and mark bolded lines
    paragraphs = []
    for line in lines:
        text = line[0]
        font_size = line[1]
        font_type = line[2]

        is_header = "Bold" in font_type and text.strip() != "" and font_size >= 8.8
        suffix = ""

        if is_header:
            suffix = header_indicator

        if is_header:
            paragraphs.append("")
        paragraphs.append(str(paragraphs.pop()) + text + suffix)

    return paragraphs

def insert_splits(paragraphs: list[str]):
    # group header with paragraphs for each section and mark splitting points per xml element
    # index = 1
    # while index <= len(paragraphs) - 1:
    #     previous_paragraph = paragraphs[index - 1]
    #     current_paragraph = paragraphs[index]

    #     header_complete = header_indicator in previous_paragraph and header_indicator not in current_paragraph

    #     if current_paragraph.strip() == "":
    #         del paragraphs[index]

    #     elif header_complete:
    #         paragraphs[index - 1] = paragraphs[index - 1].replace(header_indicator, "") + split_indicator + current_paragraph
    #         del paragraphs[index]

    #     else:
    #         index += 1


    return paragraphs


def print_xml(paragraphs: list[str], output_filepath: str):
    # start printing xml file
    console_out = sys.stdout
    xml = open(output_filepath, "w", encoding="utf8")
    sys.stdout = xml

    print("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>")
    print("<xml>")
    print("<header>")
    print("</header>")
    print("<body>")

    for paragraph in paragraphs:
        xml_section = paragraph
        xml_elements = xml_section.split(header_indicator)
        # sys.stdout = console_out
        # print(xml_elements)
        # sys.stdout = xml

        # replace special xml characters with delimted characters
        for j in range(len(xml_elements)):
            xml_elements[j] = xml_elements[j].replace("&", "&amp;")
            xml_elements[j] = xml_elements[j].replace("\"", "&quot;")
            xml_elements[j] = xml_elements[j].replace("\'", "&apos;")
            xml_elements[j] = xml_elements[j].replace("<", "&lt;")
            xml_elements[j] = xml_elements[j].replace(">", "&gt;")

        section_header = xml_elements[0]
        section_paragraphs = xml_elements[1].split("  ")

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
        print(xml_elements[0].strip())
        print("</header>")

        for section_paragraph in section_paragraphs:
            if section_paragraph.strip() != "":
                print("<p>")
                print(section_paragraph)
                print("</p>")

        print("</section>")

    print("</body>")
    print("</xml>")
    sys.stdout = console_out

# convert_pdf_to_xml("../EC decision parser Vincent/epars/abraxane-epar-public-assessment-report_en.pdf", "xml_converterd_test.xml")
