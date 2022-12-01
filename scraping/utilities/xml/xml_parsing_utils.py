import xml.etree.ElementTree as ET
import scraping.utilities.definitions.xml_tags as tags


def file_is_initial(xml_head: ET.Element) -> bool:
    """
    Returns whether a xml file is an initial authorization.

    Args:
        xml_head (ET.Element): A xml Element of the <head>...</head> node.

    Returns:
        bool: is_initial flag bool value in the xml head node.
    """

    initial_element = xml_head.findall(tags.initial_authorization)[0]
    return initial_element.text.strip() == "True"


def file_get_name_pdf(xml_head: ET.Element) -> str:
    """
    Returns file name of the pdf from which the xml file was made.

    Args:
        xml_head (ET.Element): A xml Element of the <head>...</head> node.

    Returns:
        str: Name of the pdf file in string format.
    """

    return xml_head.findall(tags.pdf_file)[0].text.strip()


def file_get_creation_date(xml_head: ET.Element) -> str:
    """
    Returns creation date of a xml file.

    Args:
        xml_head (ET.Element): A xml Element of the <head>...</head> node.

    Returns:
        str: String representing the creation datetime in the original pdf metadata, can be null.
    """

    if xml_head.findall(tags.creation_date)[0].text:
        return xml_head.findall(tags.creation_date)[0].text.strip()
    return "no_creation_date"


def get_paragraphs_by_header(header: str, xml: ET.Element) -> list[str]:
    """
    Returns a list of all paragraphs contained by the given header.

    Args:
        header (str): Substring to search for in the section header.
        xml (ET.Element): The entire xml document.

    Returns:
        list[str]: List of all paragraphs contained by the given header
    """
    res = []
    for section in xml:
        if section_contains_header_substring(header, section):
            for txt in reversed(section):
                txt = txt.text
                res.append(txt)
    return res


def file_get_modification_date(xml_head: ET.Element) -> str:
    """
    Returns modification date of a xml file.

    Args:
        xml_head (ET.Element): A xml Element of the <head>...</head> node.

    Returns:
        str: String representing the modification datetime in the original pdf metadata, can be null.
    """

    if xml_head.findall(tags.modification_date)[0].text:
        return xml_head.findall(tags.modification_date)[0].text.strip()
    return "no_modification_date"


def section_contains_substring(substring: str, section: ET.Element) -> bool:
    """
    Returns whether a xml section contains a substring in its header or paragraph tags.

    Args:
        substring (str): Substring to search for in the section.
        section (ET.Element): A xml Element of the format <section>...</section>

    Returns:
        bool: bool indicating whether the section contains the substring.
    """

    return section_contains_header_substring(substring, section) or section_contains_paragraph_substring(substring,
                                                                                                         section)


def section_contains_substring_set(substring_set: list[str], section: ET.Element) -> bool:
    """
    Returns whether a xml section contains any substring of the substring_set in its header or paragraph tags.

    Args:
        substring_set (list[str]): List of substrings to search for in the section.
        section (ET.Element): A xml Element of the format <section>...</section>

    Returns:
        bool: bool indicating whether the section contains any of the substrings.
    """

    return section_contains_header_substring_set(substring_set, section) or section_contains_paragraph_substring_set(
        substring_set, section)


def section_contains_header_substring(substring: str, section: ET.Element) -> bool:
    """
    Returns whether a xml section header contains the given substring.

    Args:
        substring (str): substring to search for in the section header.
        section (ET.Element): A xml Element of the format <section>...</section>

    Returns:
        bool: bool indicating whether the section header contains the substring.
    """

    for head in section.findall(tags.header):
        if not head.text:
            return False
        if substring.lower() in head.text.lower():
            return True
    return False


def section_contains_header_substring_set(substring_set: list[str], section: ET.Element) -> bool:
    """
    Returns whether a xml section header contains any of the substrings within substring_set.

    Args:
        substring_set (list[str]): List of substrings to search for in the section header.
        section (ET.Element): A xml Element of the format <section>...</section>

    Returns:
        bool: bool indicating whether the section contains any of the substrings in substring_set.
    """

    for head in section.findall(tags.header):
        for substring in substring_set:
            if not head.text:
                return False
            if substring.lower() in head.text.lower():
                return True

    return False


def section_contains_header_substring_set_all(substring_set: list[str], section: ET.Element) -> bool:
    """
    Returns whether a xml section header contains all the substrings within substring_set.

    Args:
        substring_set (list[str]): List of substrings to search for in the section.
        section (ET.Element): A xml Element of the format <section>...</section>

    Returns:
        bool: bool indicating whether the section contains all the substrings in substring_set.
    """    
    head = section.findall(tags.header)[0]
    substring_in_header = [substring in head.text.lower() for substring in substring_set]

    return all(substring_in_header)


def section_contains_header_number(header_number: str, header: ET.Element) -> bool:
    """
    Returns whether a xml section header contains an attribute n with value number.

    Args:
        header_number (str): String value of a header number in the form of x.y.z with no dot at the end.
        header (ET.Element): A xml Element of the <header>...</header> node within a section.

    Returns:
        bool: bool indicating whether the section contains an attribute n with value number.
    """

    if len(header.attrib) == 0:
        return False

    return header.attrib["n"] == header_number

def section_get_header_number(section: ET.Element) -> tuple[bool, str]:
    """
    Returns tuple indicating whether the header of a section contains a header number and the headernumber as string.
    If the section header contains a header number ending on a dot then the last dot will be removed. 
    
    <header>"4.1. Therapeutic indications"</header> returns (True, "4.1")
    <header>"4.1  Therapeutic indications"</header> returns (True, "4.1")
    <header>"Therapeutic indications"</header>  returns (False, "")

    Args:
        section (ET.Element): A xml Element of the <section>...</section> node within a xml_body.

    Returns:
        tuple[bool, str]: bool indicating the section contains an attribute n. 
                          str is the value of n, empty string if no attribute n.
    """

    header = section.findall(tags.header)[0]
    if len(header.attrib) == 0:
        return (False, "")

    return (True, header.attrib["n"])

def section_get_header_text(section: ET.Element) -> str:
    """
    Returns string containing the text within the header of the given section.

    e.g.:
    <header>"4.1. Therapeutic indications"</header> returns "4.1. Therapeutic indications"

    Args:
        section (ET.Element): A xml Element of the <section>...</section> node within a xml_body.

    Returns:
        str: text contained within the header of given section.
    """

    header = section.findall(tags.header)[0]
    return header.text


def section_get_header_text_numberless(section: ET.Element) -> str:
    """
    Returns string containing the text within the header of the given section without header / chapter numbers.

    e.g.:
    <header>"4.1. Therapeutic indications"</header> returns "Therapeutic indications"

    Args:
        section (ET.Element): A xml Element of the <section>...</section> node within a xml_body.

    Returns:
        str: text contained within the header of given section without header number.
    """

    contains_number, header_number = section_get_header_number(section)
    header_text = section_get_header_text(section)
    
    if contains_number:
        header_text.replace(header_number + ".", "")
        header_text.replace(header_number, "")

    return header_text

def section_contains_paragraph_substring(substring: str, section: ET.Element) -> bool:
    """
    Returns whether a section contains a substring within any of its paragraphs.

    Args:
        substring (str): substring to search for in paragraphs of section.
        section (ET.Element): A xml Element of the <section>...</section> node.

    Returns:
        bool: bool value indicating whether any paragraph in the section contains the given substring.
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
        substring_set (list[str]): List of substrings to search for in paragraphs of section.
        section (ET.Element): A xml Element of the <section>...</section> node.

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


def section_is_table_of_contents(section: ET.Element) -> bool:
    """
    Returns whether a section is part of the table of contents.

    Args:
        section (ET.Element): A xml Element of the <section>...</section> node.

    Returns:
        bool: Returns whether a section is part of the table of contents.
    """
    return section.findall(tags.header)[0].text.count('.') >= 3


def paragraph_contains_substring(substring: str, paragraph: ET.Element) -> bool:
    """
    Returns whether a single paragraph contains the given substring.

    Args:
        substring (str): Substring to search withing the paragraph.
        paragraph (ET.Element): A xml Element of the <p>...</p> node.

    Returns:
        bool: bool value indicating whether the paragraph contains the given substring.
    """

    return substring.lower() in paragraph.text.lower()


def section_append_paragraphs(section: ET.Element) -> str:
    """
    Returns a string with all text from all section paragraphs appended to each other.

    Args:
        section (ET.Element): A xml Element of the <section>...</section> node.

    Returns:
        str: all text within section paragraphs appended to each other in one string.
    """

    combined_text = ""
    for paragraph in section.findall(tags.paragraph):
        combined_text += paragraph.text + "\n"

    return combined_text


def section_get_paragraph_indices(index: int, section: ET.Element) -> ET.Element:
    """
    Returns a paragraph node based on its occurrence order in the section node, starts as 0 like an index.

    Args:
        index (int): Integer starting from zero indicating which paragraph to get text from.
        section (ET.Element): A xml Element of the <section>...</section> node.

    Returns:
        ET.Element: A xml Element of the <p>...</p> node from the given section.
    """
    
    return section.findall(tags.paragraph)[index]


def section_get_paragraph_text(index: int, section: ET.Element) -> str:
    """
    Returns text from a paragraph node based on its occurrence order in the section node, starts as 0 like an index.

    Args:
        index (int): Integer starting from zero indicating which paragraph to get text from.
        section (ET.Element): A xml Element of the <section>...</section> node.

    Returns:
        str: Text contained within the paragraph accessed by index.
    """

    return section.findall(tags.paragraph)[index].text


def get_section_header(section: ET.Element) -> str:
    """
    This function gets the <header>...</header> text from a section.

    Args:
        section (ET.Element): A xml Element of the <section>...</section> node.

    Returns:
        str: Returns the text of the <header>...</header> text from a section.
    """    
    return section.findall(tags.header)[0].text


def get_body_section_by_index(index: int, xml_body: ET.Element) -> ET.Element:
    """
    This function returns a section based on index (0-based index).

    Args:
        index (int): Index describing which section to get
        xml_body (ET.Element): A xml Element of the <body>...</body> node.


    Returns:
        ET.Element: Returns a section based on index.
    """    
    return xml_body.findall(tags.section)[index]


def get_body_section_count(xml_body: ET.Element) -> int:
    """
    This function returns the total amount of sections.

    Args:
        xml_body (ET.Element): A xml Element of the <body>...</body> node.

    Returns:
        int: Returns the count of all the sections.
    """    
    return len(xml_body.findall(tags.section))
