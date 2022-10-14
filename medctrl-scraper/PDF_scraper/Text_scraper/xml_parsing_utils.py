import xml.etree.ElementTree as ET
import xml_tags as tags
from typing import List

def file_is_initial(xml_header: ET.Element) -> bool:
    initialElement = xml_header.findall(tags.initial_authorization)[0]
    return initialElement.text.strip() == 'True'


def file_get_name_pdf(xml_header: ET.Element) -> str:
    return xml_header.findall(tags.pdf_file)[0].text.strip()


def file_get_creation_date(xml_header: ET.Element) -> str:
    return xml_header.findall(tags.creation_date)[0].text.strip()


def file_get_modification_date(xml_header: ET.Element) -> str:
    return xml_header.findall(tags.modification_date)[0].text.strip()


def section_contains_substring(substring: str, section: ET.Element)-> bool:
    return section_contains_header_substring(substring, section) or section_contains_paragraph_substring(substring, section)


def section_contains_substring_set(substrings: list[str], section: ET.Element)-> bool:
    return section_contains_header_substring_set(substrings, section) or section_contains_paragraph_substring_set(substrings, section)


def section_contains_header_tag(tag: str, head: ET.Element):
    return len(head.findall(tag)) >= 1


def section_contains_header_substring(substring: str, section: ET.Element) -> bool:
    for head in section.findall(tags.header):
        if substring.lower() in head.text.lower():
            return True

    return False


def section_contains_header_substring_set(substrings: List[str], section: ET.Element) -> bool:
    for head in section.findall(tags.header):
        for substring in substrings:
            if substring.lower() in head.text.lower():
                return True

    return False


def section_contains_header_number(number: str, head: ET.Element) -> bool:
    if len(head.attrib) == 0:
        return False

    return head.attrib["n"] == number


def section_contains_paragraph_substring(substring: str, section: ET.Element) -> bool:
    for paragraph in section.findall(tags.paragraph):
        if substring.lower() in paragraph.text:
            return True

    return False


def section_contains_paragraph_substring_set(substrings: list[str], section: ET.Element) -> bool:
    for paragraph in section.findall(tags.paragraph):
        for substring in substrings:
            if substring.lower() in paragraph.text:
                return True

    return False


def paragraph_contains_substring(substring: str, paragraph: ET.Element) -> bool:
    return substring.lower() in paragraph.text.lower()


def section_append_paragraphs(section: ET.Element) -> str:
    combined_text = ""
    for paragraph in section.findall(tags.paragraph):
        combined_text += paragraph.text + "\n"

    return combined_text


def section_get_paragraph_indices(index: int, section: ET.Element) -> list[int]:
    return section.findall(tags.paragraph)[index]


def section_get_paragraph_text(index: int, section: ET.Element) -> str:
    return section.findall(tags.paragraph)[index].text


def get_paragraphs_by_header(header: str, xml: ET.Element):
    res = []
    for section in xml:
        if section_contains_header_substring(header, section[0]):
            for txt in reversed(section):
                txt = txt.text
                res.append(txt)
    return res