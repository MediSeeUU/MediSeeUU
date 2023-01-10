import xml.etree.ElementTree as ET
import scraping.utilities.definitions.xml_tags as xml_tags
import scraping.utilities.xml.xml_parsing_utils as xml_utils
import scraping.utilities.log as log
from tqdm import tqdm
import os.path as path
import json


def clean_string(string: str) -> str:
    """
    Takes string and removes enters, tabs, callbacks and spaces to allow for more meaningful string comparisons.\n

    Args:
        string (str): Content of a section header or paragraphs to be cleaned up for comparison.

    Returns:
        str: string.replace("\\n","").replace("\\t","").replace("\\r","").replace(" ","")
    """    
    return string.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", "")
    

def remove_header_number(header_text: str) -> str:
    """
    Returns a string with header/section number removed at the front and stripped of whitespace prefixes and suffixes.\n
    Header numbers are seen as a sequence of connected integers and dots.\n

    Example:
        input: "4.1. Theraputic Indications"
        output: "Theraputic Indications"

    Args:
        header_text (str): string contents of a section header from an xml file.

    Returns:
        str: cleaned up section header content with header number removed.
    """    
    text_start_index = 0
    for i in range(0, len(header_text)):
        if all(map(lambda c: c.isnumeric() or c == '.', header_text[0:i])):
            text_start_index = i
        else:
            break
    return header_text[text_start_index:].strip()


def clean_renamed_header_text(header_text: str) -> str:
    """
    Takes header text with occurence number at the front and removes the section number.

    Example:
        input: "1 | 4.1. Theraputic Indications"
        output: "1 | Theraputic Indications"

    Args:
        header_text (str): header text content from a renamed header XML.

    Returns:
        str: header text content from a renamed header XML with section number removed.
    """    
    occurence_number = header_text.split("|")[0].strip()
    header_text = header_text.split("|")[-1].strip()
    header_text = remove_header_number(header_text)

    return occurence_number + " | " + header_text


def rename_duplicate_headers(xml_body: ET.ElementTree) -> ET.ElementTree:
    """
    Takes an XML body and returns a new one where each header is now prefixed with an occurence number for
    differentiating between sections that repeat due to annex files containing info on multiple versions
    of the same medicine, such as different dosages.

    Example:\n
        input:\n
        <body>\n
            <section><header>4.1 Therapeutic Indications.</header></section>\n
            <section><header>4.1 Therapeutic Indications.</header></section>\n
            <section><header>Traceability.</header></section>\n
        </body>

        output:\n
        <body>
            <section><header>1 | 4.1 Therapeutic Indications.</header></section>\n
            <section><header>2 | 4.1 Therapeutic Indications.</header></section>\n
            <section><header>1 | Traceability.</header></section>\n
        </body>

    Args:
        xml_body (ET.ElementTree): XML body of the original annex XML file.

    Returns:
        ET.ElementTree: XML body where all sections now have an occurence number prefix.
    """    
    occurences: dict[str, int] = {}
    new_body: ET.Element = ET.Element(xml_tags.body)

    for section in xml_body:
        header_text = xml_utils.section_get_header_text(section)
        header_text_clean = clean_string(remove_header_number(header_text))

        if header_text_clean not in occurences.keys():
            occurences[header_text_clean] = 1
        else:
            occurences[header_text_clean] += 1
        
        count = occurences[header_text_clean]
        new_body.append(xml_utils.section_set_header_text(str(count) + " | " + header_text, section))

    return new_body


def open_xml_path(xml_path: str) -> ET.ElementTree:
    """
    Opens XML file and returns the <body></body> ET.Element with all section headers prefixed with occurence number.

    Args:
        xml_path (str): Filepath to XML file

    Returns:
        ET.ElementTree: ET.ElementTree containing the <body>...</body> node
        with all section headers prefixed with occurence number.
    """    
    try:
        xml_body = ET.parse(xml_path).getroot()[1]  # get xml_body
        xml_body = rename_duplicate_headers(xml_body)
    except ET.ParseError:
        # log.warning("ANNEX COMPARER: failed to open xml file", xml_path) #TODO: enable logging
        return {}

    return xml_body


def create_section_dict(xml_body: ET.Element) -> dict[str, (str, str)]:
    """
    Creates a section_dict dictionary containing a (section header, section text) tuple
    for each cleaned up and renamed XML section header as key.
    Resulting dictionary is to be used for comparing occurences of specific headers between multiple XML files.

    Example:\n
    input:\n
    <body>
        </section>
            <header>1 | 1. section header 1</header>\n
            <p>section content 1</p>
        </section>
        </section>
            <header>1 | section header 2</header>\n
            <p>section content 2</p>
        </section>
    </body>

    output:\n
    {
        "1|sectionheader1": (1 | section header 1, section content 1),
        "1|sectionheader2": (1 | section header 2, section content 2)
    }

    Args:
        xml_body (ET.Element): ET.Element containing a <body>...</body> node from an XML file.
        
    Returns:
        dict[str, (str, str)]: Dictionary containing (section header, section text) tuple
        for each cleaned up section header text.
    """
    section_dict = {}
    for section in xml_body:
        header_text = xml_utils.section_get_header_text(section)
        section_header = clean_renamed_header_text(header_text)
        section_key = clean_string(section_header)
        section_text = xml_utils.section_append_paragraphs(section)
        section_dict[section_key] = (section_header, section_text)

    return section_dict


def compare_xml_files_dict(new_xml_path: str, old_xml_path: str) -> dict[str, any]:
    """
    Returns a dictionary with comparison results between two XML files specified by new_xml_path and old_xml_path.

    Structure of returned dictionary:\n
    changelog_dict: {
        "old_file": [old_filename_string],
        "new_file": [new_filename_string],
        "changes":[
            [change_dicts]
        ]
    }

    change_dict: {
        "change": ["added section"|"removed section"|"changed section content"],
        "header": [section header text],
        "section_text": [section paragraph content]
    }

    Args:
        new_xml_path (str): filepath to new XML file.
        old_xml_path (str): filepath to old XML file.

    Returns:
        dict[str, any]: changelog_dict containing all changes between two XML files.
    """    
    body_new_file = open_xml_path(new_xml_path)
    body_old_file = open_xml_path(old_xml_path)

    if body_new_file == {} or body_old_file == {}:
        return {}
    
    changelog_dict = {"old_file": path.basename(old_xml_path), 
                      "new_file": path.basename(new_xml_path),
                      "changes": []}
    
    sections_new_file = create_section_dict(body_new_file)
    sections_old_file = create_section_dict(body_old_file)

    shared_keys = sections_new_file.keys() & sections_old_file.keys()
    added_keys = [key for key in sections_new_file.keys() if key not in shared_keys]
    removed_keys = [key for key in sections_old_file.keys() if key not in shared_keys]

    for section_key in added_keys:
        change_dict = {
            "change": "added section",
            "header": sections_new_file[section_key][0],
            "section_text": sections_new_file[section_key][1]
        }
        changelog_dict["changes"].append(change_dict)
    
    for section_key in removed_keys:
        change_dict = {
            "change": "removed section",
            "header": sections_old_file[section_key][0],
            "section_text": sections_old_file[section_key][1]
        }
        changelog_dict["changes"].append(change_dict)

    for section_key in shared_keys:
        if clean_string(sections_old_file[section_key][1]) != clean_string(sections_new_file[section_key][1]):
            change_dict = {
                "change": "changed section content",
                "header": sections_new_file[section_key][0],
                "old_content": sections_old_file[section_key][1],
                "new_content": sections_new_file[section_key][1]
            }
            changelog_dict["changes"].append(change_dict)

    return changelog_dict


def compare_xml_files_file(new_xml_path: str, old_xml_path: str, save_dir: str, filename="comparison.json"):
    """
    Creates a changelog.json file containing changelog_dict info on comparison between two XML files
     at save_dir using filename.

    Args:
        new_xml_path (str): Filepath to the new XML file.
        old_xml_path (str): Filepath to the old XML file.
        save_dir (str): Directory to save changelog.json at.
        filename (str, optional): Filename for changelog.json created. Defaults to "comparison.json".
    """    
    comparison_dict = compare_xml_files_dict(new_xml_path, old_xml_path)

    try:
        with open(path.join(save_dir, filename), "w") as comparison_json:
            json.dump(comparison_dict, comparison_json)
    except Exception:
        print("ANNEX COMPARER: write", path.join(save_dir, filename))
