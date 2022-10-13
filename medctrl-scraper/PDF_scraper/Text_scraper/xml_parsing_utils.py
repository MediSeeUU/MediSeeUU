import xml.etree.ElementTree as ET
from typing import List

xml_section_tag = "section"
xml_head_tag = "head"
xml_paragraph_tag = "p"
xml_initial_tag = "initial"
xml_pdf_tag = "pdf"

def file_is_initial(xml_header: ET.Element) -> bool:
    initialElement = xml_header.findall(xml_initial_tag)[0]
    print(initialElement.text)
    return initialElement.text.strip() == 'True'

def file_pdf_name(xml_header: ET.Element) -> str:
    return xml_header.findall(xml_pdf_tag)[0].text

def section_contains_head_substring(substring: str, section: ET.Element):
    substring_found = False
    for head in section.findall(xml_head_tag):
        if substring.lower() in head.text.lower():
            substring_found |= True

    return substring_found


def section_contains_head_substring_set(substrings: List[str], section: ET.Element):
    substring_found = False
    for head in section.findall(xml_head_tag):
        for substring in substrings:
            if substring.lower() in head.text.lower():
                substring_found |= True

    return substring_found


def section_contains_header_number(number: str, head: ET.Element):
    if len(head.attrib) == 0:
        return False

    return head.attrib["n"] == number


def paragraph_contains_substring(substring: str, paragraph: ET.Element):
    return substring.lower() in paragraph.text.lower()


def section_append_paragraphs(section: ET.Element):
    combined_text = ""
    for paragraph in section.findall(xml_paragraph_tag):
        combined_text += paragraph.text + "\n"

    return combined_text


def section_get_paragraph_index(index: int, section: ET.Element):
    return section.findall(xml_paragraph_tag)[index]


def text_contains_substrings(substring: str, text: str):
    return substring in text


def head_contains_tag(tag: str, head: ET.Element):
    return len(head.findall(tag)) >= 1
