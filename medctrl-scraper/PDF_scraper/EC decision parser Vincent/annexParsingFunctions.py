import xmlParserUtils as Utils
import parsedInfoStruct as PIS


def scrapeMedicineName(parsedInfo: PIS.parsedInfoStruct, section: Utils.ET.Element):
    if not Utils.divHeadContainsSubstringSetElement(["name"], section):
        return
    
    parsedInfo.medicineName = section.findall(Utils.xmlTeiTagParagraph)[0].text

def scrapeShelfLife(parsedInfo: PIS.parsedInfoStruct, section: Utils.ET.Element):
    if not Utils.divHeadContainsSubstringSetElement(["shelflife", "shelf", "life", "shelf life"], section):
        return
    
    parsedInfo.shelfLife = Utils.combineParagraphTexts(section)