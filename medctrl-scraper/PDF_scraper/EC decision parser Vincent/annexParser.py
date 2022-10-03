import xml.etree.ElementTree as ET
import xmlParserUtils as Utils
import parsedInfoStruct as PIS
import annexParsingFunctions as APF

def parse(xmlFilePath: str):
    xmlTree = ET.parse(xmlFilePath)
    root = xmlTree.getroot()

    #split xml tree structure into manageable pieces
    xmlHeader = root[0]
    xmlTextBody = root[1][0]
    
    # list of divs grouping headers and paragraphs together
    xmlTextSections = xmlTextBody.findall(Utils.xmlTeiTagDiv)
    parsedInfo = PIS.parsedInfoStruct()

    # loop through all sections and call apropiate parser functions
    for section in xmlTextSections:
        APF.scrapeMedicineName(parsedInfo, section)
        APF.scrapeShelfLife(parsedInfo, section)




    #return struct containing all scraped info
    return parsedInfo



info = parse("ilaris-epar-product-information_en.tei.xml")
print(info.parseDate)
print()
print(info.medicineName)
print()
print(info.shelfLife)