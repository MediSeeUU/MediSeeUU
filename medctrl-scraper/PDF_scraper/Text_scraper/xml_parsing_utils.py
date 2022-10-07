import xml.etree.ElementTree as ET
from typing import List

xml_section_tag = "section"
xml_head_tag = "head"
xml_paragraph_tag =  "p"

def section_contains_head_substring(substring: str, section: ET.Element):
    substringFound = False
    for head in section.findall(xml_head_tag):
        if substring.lower() in head.text.lower():
            substringFound |= True
    
    return substringFound

def section_contains_head_substring_set(substrings: List[str], section: ET.Element):
    substringFound = False
    for head in section.findall(xml_head_tag):
        for substring in substrings:
            if substring.lower() in head.text.lower():
                substringFound |= True
    
    return substringFound

def section_contains_header_number(number: str, head: ET.Element):
    if len(head.attrib) == 0:
        return False

    return head.attrib["n"] == number

def paragraph_contains_substring(substring: str, paragraph: ET.Element):
    return substring.lower() in paragraph.text.lower()


def section_append_paragraphs(section: ET.Element):
    combinedText = ""
    for paragraph in section.findall(xml_paragraph_tag):
        combinedText += paragraph.text + "\n"
    
    return combinedText

def section_get_paragraph_index(index: int, section: ET.Element):
    return section.findall(xml_paragraph_tag)[index]

def text_contains_substrings(substring: str, text: str):
    return substring in text

def head_contains_tag(tag: str, head: ET.Element):
    return len(head.findall(tag)) >= 1