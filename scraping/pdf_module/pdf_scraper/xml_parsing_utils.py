import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

import pdf_module.pdf_scraper.xml_tags as tags
from typing import List


def file_is_initial(xml_head: ET.Element) -> bool:
    """
    Returns whether an xml file is an initial authorization.

    Args:
        xml_head (xml.etree.ElementTree.Element): an xml Element of the <head>...</head> node.

    Returns:
        bool: bool equal to the is_initial flag in the xml head node.
    """

    initial_element = xml_head.findall(tags.initial_authorization)[0]
    return initial_element.text.strip() == 'True'


def file_get_name_pdf(xml_head: ET.Element) -> str:
    """
    Returns file name of the pdf from which the xml file was made.

    Args:
        xml_head (xml.etree.ElementTree.Element): an xml Element of the <head>...</head> node.

    Returns:
        str: name of the pdf file in string format.
    """

    return xml_head.findall(tags.pdf_file)[0].text.strip()


def file_get_creation_date(xml_head: ET.Element) -> str:
    """
    Returns creation date of an xml file.

    Args:
        xml_head (xml.etree.ElementTree.Element): an xml Element of the <head>...</head> node.

    Returns:
        str: string representing the creation datetime in the original pdf metadata, can be null.
    """

    try:
        return xml_head.findall(tags.creation_date)[0].text.strip()
    except:
        xml_head.findall(tags.creation_date)[0].text


def file_get_modification_date(xml_head: ET.Element) -> str:
    """
    Returns modification date of an xml file.

    Args:
        xml_head (xml.etree.ElementTree.Element): an xml Element of the <head>...</head> node.

    Returns:
        str: string representing the modification datetime in the original pdf metadata, can be null.
    """

    try:
        return xml_head.findall(tags.modification_date)[0].text.strip()
    except:
        xml_head.findall(tags.modification_date)[0].text


def section_contains_substring(substring: str, section: ET.Element) -> bool:
    """
    Returns whether an xml section contains a substring in its header or paragraph tags.

    Args:
        substring (str): substring to search for in the section.
        section (xml.etree.ElementTree.Element): an xml Element of the <section>...</section> node.

    Returns:
        bool: bool indicating whether or not the section contains the substring.
    """

    return section_contains_header_substring(substring, section) or section_contains_paragraph_substring(substring,
                                                                                                         section)


def section_contains_substring_set(substring_set: list[str], section: ET.Element) -> bool:
    """
    Returns whether an xml section contains any substring of the substring_set in its header or paragraph tags.

    Args:
        substring_set (list[str]): list of substrings to search for in the section.
        section (xml.etree.ElementTree.Element): an xml Element of the <section>...</section> node.

    Returns:
        bool: bool indicating whether or not the section contains any of the substrings.
    """

    return section_contains_header_substring_set(substring_set, section) or section_contains_paragraph_substring_set(
        substring_set, section)


# def section_contains_header_tag(tag: str, header: ET.Element):
#     """
#     Returns whether an xml section section contains a header section

#         Args:
#                 tag (str): string value of an attribute.
#                 header (xml.etree.ElementTree.Element): an xml Element of the <header>...</header> node within a section.

#         Returns:
#                 bool: bool indicating whether or not the section contains an attribute with value tag
#     """
    
#     return len(header.findall(tag)) >= 1


def section_contains_header_substring(substring: str, section: ET.Element) -> bool:
    """
    Returns whether an xml section header contains the given substring.

    Args:
        substring (str): substring to search for in the section header.
        section (xml.etree.ElementTree.Element): an xml Element of the <header>...</header> node within a section.

    Returns:
        bool: bool indicating whether or not the section header contains the substring.
    """

    for head in section.findall(tags.header):
        if not head.text:
            return False
        if substring.lower() in head.text.lower():
            return True
    return False


def section_contains_header_substring_set(substring_set: List[str], section: ET.Element) -> bool:
    """
    Returns whether an xml section header contains any of the substrings within substring_set.

    Args:
        substring_set (list[str]): list of substrings to search for in the section header.
        section (xml.etree.ElementTree.Element): an xml Element of the <header>...</header> node within a section.

    Returns:
        bool: bool indicating whether or not the section contains any of the substrings in substring_set.
    """

    for head in section.findall(tags.header):
        for substring in substring_set:
            if not head.text:
                return False
            if substring.lower() in head.text.lower():
                return True

    return False


def section_contains_header_number(header_number: str, header: ET.Element) -> bool:
    """
    Returns whether an xml section header contains an attribute n with value number.

    Args:
        number (str): string value of an header number in the form of x.y.z with no dot at the end.
        header (xml.etree.ElementTree.Element): an xml Element of the <header>...</header> node within a section.

    Returns:
        bool: bool indicating whether or not the section contains an attribute n with value number
    """

    if len(header.attrib) == 0:
        return False

    return header.attrib["n"] == header_number


def section_contains_paragraph_substring(substring: str, section: ET.Element) -> bool:
    """
    Returns whether a section contains a substring within any of its paragraphs.

    Args:
        substring (str): substring to search for in paragraphs of section.
        section (ET.Element): an xml Element of the <section>...</section> node.

    Returns:
        bool: bool value indicating whether any paragraph in the section containsthe given substring.
    """

    for paragraph in section.findall(tags.paragraph):
        if not paragraph.text:
            return False
        if substring.lower() in paragraph.text:
            return True

    return False


def section_contains_paragraph_substring_set(substring_set: list[str], section: ET.Element) -> bool:
    """
    Returns whether a section contains a substring within substring_set in any of its paragraphs.

    Args:
        substring_set (list[str]): list of substrings to search for in paragraphs of section.
        section (ET.Element): an xml Element of the <section>...</section> node.

    Returns:
        bool: bool value indicating whether any paragraph contains any substring in substring_set.
    """    

    for paragraph in section.findall(tags.paragraph):
        for substring in substring_set:
            if not paragraph.text:
                return False
            if substring.lower() in paragraph.text:
                return True

    return False


def paragraph_contains_substring(substring: str, paragraph: ET.Element) -> bool:
    """
    Returns whether a single paragraph contains the given substring.

    Args:
        substring (str): substring to search withing the paragraph.
        paragraph (ET.Element): an xml Element of the <p>...</p> node.

    Returns:
        bool: bool value indicating whether the paragraph contains the given substring.
    """

    return substring.lower() in paragraph.text.lower()


def section_append_paragraphs(section: ET.Element) -> str:
    """
    Returns a string with all text from all section paragraphs appended to eachother.

    Args:
        section (ET.Element): an xml Element of the <section>...</section> node.

    Returns:
        str: all text within section paragraphs appended to each other in one string.
    """

    combined_text = ""
    for paragraph in section.findall(tags.paragraph):
        combined_text += paragraph.text + "\n"

    return combined_text


def section_get_paragraph_indices(index: int, section: ET.Element) -> ET.Element:
    """
    Returns a paragraph node based on its occurance order in the section node, starts as 0 like an index.

    Args:
        index (int): integer starting from zero indicating which paragraph to get text from
        section (ET.Element): an xml Element of the <section>...</section> node.

    Returns:
        ET.Element: an xml Element of the <p>...</p> node from the given section.
    """    
    return section.findall(tags.paragraph)[index]


def section_get_paragraph_text(index: int, section: ET.Element) -> str:
    """
    Returns text from a paragraph node based on its occurance order in the section node, starts as 0 like an index.

    Args:
        index (int): integer starting from zero indicating which paragraph to get text from.
        section (ET.Element): an xml Element of the <section>...</section> node.

    Returns:
        str: text contained within the paragraph accessed by index.
    """    

    return section.findall(tags.paragraph)[index].text
