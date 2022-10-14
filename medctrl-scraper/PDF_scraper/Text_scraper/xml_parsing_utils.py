import xml.etree.ElementTree as ET
from typing import List

# meta data tags
xml_head_tag = "head"
xml_initial_authorization_tag = "initial_authorization"
xml_pdf_file_tag = "pdf_file"
xml_creation_date_tag = "creation_date"
xml_modification_date_tag = "modification_date"

# section data tags
xml_section_tag = "section"
xml_section_header_tag = "header"
xml_section_paragraph_tag = "p"

def file_is_initial(xml_header: ET.Element) -> bool:
    initialElement = xml_header.findall(xml_initial_authorization_tag)[0]
    return initialElement.text.strip() == 'True'


def file_get_name_pdf(xml_header: ET.Element) -> str:
    return xml_header.findall(xml_pdf_file_tag)[0].text.strip()


def file_get_creation_date(xml_header: ET.Element) -> str:
    return xml_header.findall(xml_creation_date_tag)[0].text.strip()


def file_get_modification_date(xml_header: ET.Element) -> str:
    return xml_header.findall(xml_modification_date_tag)[0].text.strip()


def section_contains_head_substring(substring: str, section: ET.Element) -> bool:
    substring_found = False
    for head in section.findall(xml_section_header_tag):
        if substring.lower() in head.text.lower():
            substring_found |= True

    return substring_found


def section_contains_head_substring_set(substrings: List[str], section: ET.Element) -> bool:
    substring_found = False
    for head in section.findall(xml_section_header_tag):
        for substring in substrings:
            if substring.lower() in head.text.lower():
                substring_found |= True

    return substring_found


def section_contains_header_number(number: str, head: ET.Element) -> bool:
    if len(head.attrib) == 0:
        return False

    return head.attrib["n"] == number


def paragraph_contains_substring(substring: str, paragraph: ET.Element) -> bool:
    return substring.lower() in paragraph.text.lower()


def section_append_paragraphs(section: ET.Element) -> str:
    combined_text = ""
    for paragraph in section.findall(xml_section_paragraph_tag):
        combined_text += paragraph.text + "\n"

    return combined_text


def section_get_paragraph_indices(index: int, section: ET.Element) -> list[int]:
    return section.findall(xml_section_paragraph_tag)[index]


def get_paragraphs_by_header(header: str, xml):
    res = []
    for section in xml:
        if section_contains_head_substring(header, section[0]):
            for txt in reversed(section):
                txt = txt.text
                res.append(txt)
    return res


def head_contains_tag(tag: str, head: ET.Element):
    return len(head.findall(tag)) >= 1
