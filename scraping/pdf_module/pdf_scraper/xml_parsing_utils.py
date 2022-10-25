import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

import pdf_module.pdf_scraper.xml_tags as tags
from typing import List


def file_is_initial(xml_head: ET.Element) -> bool:
    """
    Returns whether an xml file is an initial authorization.

    :param xml_head (xml.etree.ElementTree.Element): an xml Element of the <head>...</head> node.

    :return is_initial (bool): bool equal to the is_initial flag in the xml head node.
    """
    initial_element = xml_head.findall(tags.initial_authorization)[0]
    return initial_element.text.strip() == 'True'


def file_get_name_pdf(xml_head: ET.Element) -> str:
    """
    Returns file name of the pdf from which the xml file was made.

            Parameters:
                    xml_head (xml.etree.ElementTree.Element): an xml Element of the <head>...</head> node.

            Returns:
                    pdf_file (str): name of the pdf file in string format.
    """
    return xml_head.findall(tags.pdf_file)[0].text.strip()


def file_get_creation_date(xml_head: ET.Element) -> str:
    """
    Returns creation date of an xml file.

            Parameters:
                    xml_head (xml.etree.ElementTree.Element): an xml Element of the <head>...</head> node.

            Returns:
                    creation_date (str): string representing the creation datetime in the original pdf metadata, can be null.
    """
    try:
        return xml_head.findall(tags.creation_date)[0].text.strip()
    except:
        xml_head.findall(tags.creation_date)[0].text


def file_get_modification_date(xml_head: ET.Element) -> str:
    """
    Returns modification date of an xml file.

            Parameters:
                    xml_head (xml.etree.ElementTree.Element): an xml Element of the <head>...</head> node.

            Returns:
                    modification_date (str): string representing the modification datetime in the original pdf metadata, can be null.
    """
    try:
        return xml_head.findall(tags.modification_date)[0].text.strip()
    except:
        xml_head.findall(tags.modification_date)[0].text


def section_contains_substring(substring: str, section: ET.Element) -> bool:
    """
    Returns whether an xml section contains a substring in its header or paragraph tags.

            Parameters:
                    substring (str): substring to search for in the section.
                    section (xml.etree.ElementTree.Element): an xml Element of the <section>...</section> node.

            Returns:
                    contains_substring (bool): bool indicating whether or not the section contains the substring
    """
    return section_contains_header_substring(substring, section) or section_contains_paragraph_substring(substring,
                                                                                                         section)


def section_contains_substring_set(substring_set: list[str], section: ET.Element) -> bool:
    """
    Returns whether an xml section contains any substring of the substring_set in its header or paragraph tags.

        Parameters:
                substring_set (list[str]): list of substrings to search for in the section.
                section (xml.etree.ElementTree.Element): an xml Element of the <section>...</section> node.

        Returns:
                contains_substring (bool): bool indicating whether or not the section contains any of the substrings
    """
    return section_contains_header_substring_set(substring_set, section) or section_contains_paragraph_substring_set(
        substring_set, section)


def section_contains_header_tag(tag: str, header: ET.Element):
    """
    Returns whether an xml section header contains the attribute value tag

        Parameters:
                tag (str): list of substrings to search for in the section.
                section (xml.etree.ElementTree.Element): an xml Element of the <section>...</section> node.

        Returns:
                contains_substring (bool): bool indicating whether or not the section contains any of the substrings
    """
    
    return len(header.findall(tag)) >= 1


def section_contains_header_substring(substring: str, section: ET.Element) -> bool:
    """
    Returns whether an xml section header the attribute value

        Parameters:
                substring_set (list[str]): list of substrings to search for in the section.
                section (xml.etree.ElementTree.Element): an xml Element of the <section>...</section> node.

        Returns:
                contains_substring (bool): bool indicating whether or not the section contains any of the substrings
    """
    for head in section.findall(tags.header):
        if not head.text:
            return False
        if substring.lower() in head.text.lower():
            return True
    return False


def section_contains_header_substring_set(substring_set: List[str], section: ET.Element) -> bool:
    for head in section.findall(tags.header):
        for substring in substring_set:
            if not head.text:
                return False
            if substring.lower() in head.text.lower():
                return True

    return False


def section_contains_header_number(number: str, head: ET.Element) -> bool:
    if len(head.attrib) == 0:
        return False

    return head.attrib["n"] == number


def section_contains_paragraph_substring(substring: str, section: ET.Element) -> bool:
    for paragraph in section.findall(tags.paragraph):
        if not paragraph.text:
            return False
        if substring.lower() in paragraph.text:
            return True

    return False


def section_contains_paragraph_substring_set(substring_set: list[str], section: ET.Element) -> bool:
    for paragraph in section.findall(tags.paragraph):
        for substring in substring_set:
            if not paragraph.text:
                return False
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


def section_get_paragraph_indices(index: int, section: ET.Element) -> Element:
    return section.findall(tags.paragraph)[index]


def section_get_paragraph_text(index: int, section: ET.Element) -> str:
    return section.findall(tags.paragraph)[index].text


def get_paragraphs_by_header(header: str, xml: ET.Element):
    res = []
    for section in xml:
        if section_contains_header_substring(header, section):
            for txt in reversed(section):
                txt = txt.text
                res.append(txt)
    return res
