#EC parser
import re
import helper
import PDFhelper 

#EC document 

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

    (content,rem) = PDFhelper.findBetweenFormat('(1)','(2)',rem,False)
    table['body']['P1'] = PDFhelper.filterFont([],[],content)

    (content,rem) = PDFhelper.findBetweenFormat('(2)','(3)',rem,False)
    table['body']['P2'] = PDFhelper.filterFont([],[],content)

    (content,rem) = PDFhelper.findBetweenFormat('(3)','HAS ADOPTED THIS DECISION:',rem,False)
    table['body']['P3'] = PDFhelper.filterFont([],[],content)

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
    for txt in section:
        if '\"' in txt:
            return(re.search('"([^"]*)"',txt)[0])
    return "Name Not Found"