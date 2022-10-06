import sys
import fitz
import PDFhelper as ph

bold_indicator = "|-BOLD-|"
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
    text_format_lower = ph.getTextFormatLower(document)
    paragraphs = get_marked_paragraphs(text_format_lower, is_epar)
    paragraphs = preprocess_paragraphs(paragraphs)
    print_xml(paragraphs, output_filepath)


def get_marked_paragraphs(text_format_lower: str, is_epar: bool):

    # skip inital pages until table of content
    if is_epar:
        while "table of content" not in text_format_lower[0][0]:
            del text_format_lower[0]
        
            if len(text_format_lower) == 0:
                break
    
    # concatinate list of lines into list of paragraphs and mark bolded lines
    paragraphs = [""]
    for i in range(len(text_format_lower)):
        line = text_format_lower[i]
        text = line[0]
        font_size = line[1]
        font_type = line[2]

        if i < len(text_format_lower) - 1:
            nextline = text_format_lower[i + 1]
        else:
            nextline = text_format_lower[i]

        suffix = ""
        if "Bold" in font_type and text != " " and font_size >= 10.5: # condition to check if line is header
            suffix += bold_indicator

        if nextline[0] != " ":
            paragraphs.append(str(paragraphs.pop()).replace(suffix, "") + text + suffix)
        else:
            paragraphs.append(str(paragraphs.pop()).replace(suffix, "") + text + suffix)
            paragraphs.append("")
    
    return paragraphs

def preprocess_paragraphs(paragraphs: list[str]):
    # group header with paragraphs for each section and mark splitting points per xml element
    index = 1
    while index <= len(paragraphs) - 1:
        previous_paragraph = paragraphs[index - 1]
        current_paragraph = paragraphs[index]

        previous_paragraph_split = remove_all_substring("", previous_paragraph.strip().replace(bold_indicator, "").split("."))
        should_combine_headers = all(string.isnumeric() for string in previous_paragraph_split)

        if current_paragraph == " ":
            del paragraphs[index]
        elif bold_indicator in previous_paragraph and bold_indicator in current_paragraph and should_combine_headers:
            paragraphs[index - 1] = paragraphs[index - 1].replace(bold_indicator, "") + current_paragraph
            del paragraphs[index]
        elif bold_indicator in previous_paragraph and bold_indicator not in current_paragraph:
            paragraphs[index - 1] = paragraphs[index - 1] + split_indicator + current_paragraph
            del paragraphs[index]
        else:
            index += 1

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

    for i in range(len(paragraphs)):
        xmlElements = paragraphs[i].split(split_indicator)
        xmlElements[0] = xmlElements[0].replace(bold_indicator, "").strip()

        # replace special xml characters with delimted characters
        for i in range(len(xmlElements)):
            xmlElements[i] = xmlElements[i].replace("&", "&amp;")
            xmlElements[i] = xmlElements[i].replace("\"", "&quot;")
            xmlElements[i] = xmlElements[i].replace("\'", "&apos;")
            xmlElements[i] = xmlElements[i].replace("<", "&lt;")
            xmlElements[i] = xmlElements[i].replace(">", "&gt;")

        # check if header contains paragraph number and fill header_attribute with the corresponding number
        split_header = xmlElements[0].split()
        header_numbers = remove_all_substring("", split_header[0].split("."))
        header_attribute = ""

        if all(number.isnumeric() for number in header_numbers):
            if len(header_numbers) == 1:
                header_attribute = " n=\"" + header_numbers[0] + "\""
            if len(header_numbers) == 2:
                header_attribute = " n=\"" + header_numbers[0] + "." + header_numbers[1] + "\""

        # print the section from xmlElements taking sections and subsections into account
        print("<section>")

        print("<header" + header_attribute + ">")
        print(xmlElements[0].strip())
        print("</header>")

        for paragraph_index in range(1, len(xmlElements)):
            print("<p>")
            print(xmlElements[paragraph_index].strip())
            print("</p>")

        print("</section>")

    print("</body>")
    print("</xml>")
    sys.stdout = console_out

# convert_pdf_to_xml("../EC decision parser Vincent/epars/abraxane-epar-public-assessment-report_en.pdf", "xml_converterd_test.xml")
