#EC parser
import re
import helper
import PDFhelper 

#EC Decision document 

#Scans and ordens EC orphan designation pdfs
def getTableEC(pdf):
    table = {'intro': dict.fromkeys(['front_page']),
             'body' : dict.fromkeys(['main_text','P1','P2','P3']),
             'decision' : dict.fromkeys(['dec_text']),
             'remaining' : []}

    pdf_format = PDFhelper.getTextFormat(pdf)

    #intro
    (content,rem) = PDFhelper.findBetweenFormat('DECISION','AUTHENTIC',pdf_format,True)
    table['intro']['front_page'] = PDFhelper.filterFont([],[],content)

    #filter second intro message
    (_,rem) = PDFhelper.findBetweenFormat('DECISION','AUTHENTIC',rem,True)

    #content
    (content,rem) = PDFhelper.findBetweenFormat('COMMISSION','Whereas:',rem,True)
    table['body']['main_text'] = PDFhelper.filterFont([],[],content)
 
    
    #bullet points as one chunck
    (bulletpoints,rem) = PDFhelper.findBetweenFormat('','HAS ADOPTED THIS DECISION:',rem,False)
    
    zoeken = True
    bullet_count = 1
    while zoeken:
        #finds section from start till next bullet point
        (bp_content,bulletpoints) = PDFhelper.findBetweenFormat('','(' + str(bullet_count+1) +')',bulletpoints,False) 
        table['body']['P' + str(bullet_count)] = PDFhelper.filterFont([12],[],bp_content)
        
        #nothing more to be found or stuck in loop
        if bulletpoints == [] or bullet_count > 15:
            zoeken = False
        bullet_count += 1

    #decision
    (content,rem) = PDFhelper.findBetweenFormat('HAS ADOPTED THIS DECISION:','Article 1',rem,False)
    table['decision']['dec_text'] = PDFhelper.filterFont([],[],content)

    article_count = PDFhelper.countStr('Article','TimesNewRoman,Italic',rem)

    for arc in range(article_count):
        arc_num = arc + 1
        
        if arc_num == article_count:
            (content,rem) = PDFhelper.findBetweenFormat('Article ' + str(arc_num),'Done at',rem,False)
            table['decision']['A'+str(arc_num)] = PDFhelper.filterFont([12],[],content)
        else:    
            (content,rem) = PDFhelper.findBetweenFormat('Article ' + str(arc_num),'Article ' + str(arc_num + 1),rem,False)
            table['decision']['A'+str(arc_num)] = PDFhelper.filterFont([12],[],content)
    
    table['remaining'] = PDFhelper.filterFont([12], [], rem)
    
    return table

def tableEC_getDate(table):
    
    
    section = table['intro']['front_page']
    for txt in section:
        if 'of ' in txt:
            return helper.getDate(txt)
    return helper.getDate('')

def tableEC_getName(table):
    section = table['intro']['front_page']
    
    temp = ''
    for txt in section:
        temp += txt
        
    if '\"' in temp:
        try:
            section = re.search('"([^"]*)"',temp)[0]
            section = section.replace('"','')
            #gets only first section
            return section.split('-')[0].strip()
        except:
            pass
    if '“' in temp:
        try:
            section = re.search('“(.+?)”', temp)[0]
            section = section.split(' - ')
            section.pop()
            section = ''.join(section)
            section = section.replace('“','')
            section = section.replace('”','')
            return section
        except:
            pass
    return "Product name Not Found"

#active substance
def tableEC_getAS(table):
    section = table['intro']['front_page']
    
    temp = ''
    for txt in section:
        temp += txt
        
    #find normal quotes
    if '\"' in temp:
        try:
            section = re.search('"([^"]*)"',temp)[0]
            section = section.replace('"','')
            #gets only second section if present
            try:
                return section.split('-')[1].strip()
            except:
                pass
        except:
            pass
        
    #finds unicode quote
    if '“' in temp:
        try:
            section = re.search('“(.+?)”', temp)[0].split(' - ').pop()
            section = ''.join(section)
            section = section.replace('“','')
            section = section.replace('”','')
            return section
        except:
            pass
    return "Active substance Not Found"