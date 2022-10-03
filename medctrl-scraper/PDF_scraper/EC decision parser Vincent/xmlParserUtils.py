import xml.etree.ElementTree as ET
from typing import List

xmlTeiTagDiv = "{http://www.tei-c.org/ns/1.0}div"
xmlTeiTagHead = "{http://www.tei-c.org/ns/1.0}head"
xmlTeiTagParagraph =  "{http://www.tei-c.org/ns/1.0}p"

def headContainsSubstring(substring: str, head):
    return substring.lower() in head.text.lower()


def divContainsHeadWithSubstring(substring: str, div: ET.Element):
    substringFound = False
    for head in div.findall(xmlTeiTagHead):
        if substring.lower() in head.text.lower():
            substringFound |= True
    
    return substringFound

def divHeadContainsSubstringSetElement(substrings: List[str], div: ET.Element):
    substringFound = False
    for head in div.findall(xmlTeiTagHead):
        for substring in substrings:
            if substring.lower() in head.text.lower():
                substringFound |= True
    
    return substringFound

def isHeadOfSectionNumber(number: str, head):
    if len(head.attrib) == 0:
        return False

    return head.attrib["n"] == number

def paragraphContainsSubstring(substring: str, paragraph):
    return substring.lower() in paragraph.text.lower()


def combineParagraphTexts(div):
    combinedText = ""
    for paragraph in div.findall(xmlTeiTagParagraph):
        combinedText += paragraph.text + "\n"
    
    return combinedText

def textContainsSubstring(substring: str, text: str):
    return substring in text

def divContainsSubTag(tag: str, div):
    return len(div.findall(tag))