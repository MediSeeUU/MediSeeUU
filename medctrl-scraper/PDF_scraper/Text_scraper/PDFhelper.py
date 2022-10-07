# pdf helper functions

# Returns the textsize and font of every line in a pdf.

def get_text(data, results, lower):
    for lines in data:
        text = lines['text']
        size = lines['size']
        font = lines['font']
        if lower:
            results.append(text.lower(), size, font)
        else:
            results.append(text, size, font)


def getTextFormat(pdf, lower=False):
    results = []
    for page in pdf:
        dict = page.get_text("dict")
        blocks = dict["blocks"]
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                for span in spans:
                    data = span['spans']
                    get_text(data, results, lower)
    return results


def GetSection(pdf, start, stop, fontSize, fonts):
    section = findBetween(start, stop, pdf)
    clean = filterFont(fontSize, fonts, section)

    text = ""
    for line in clean:
        text += line + "\n"
        continue

    return text


def filterFont(fontSize, fontList, section):
    res = []
    for (txt, size, font) in section:
        # remove empty txt or only spaces
        if txt == " " or txt.count(' ') == len(txt):
            continue

        if round(size, 1) in fontSize or fontSize == []:
            if font in fontList or fontList == []:
                res.append(txt)
    return res


# returns all lines from and including start till stop for a given pdf
def findBetween(start, stop, pdf):
    results = []
    save = False
    for page in pdf:
        dict = page.get_text("dict")
        blocks = dict["blocks"]
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                for span in spans:
                    data = span['spans']
                    for lines in data:
                        if start in lines['text']:
                            save = True
                        if save:
                            results.append((lines['text'], lines['size'], lines['font']))
                        if stop in lines['text'] and save:
                            return results
    return results


# returns all lines from and including start till stop for a given format
def findBetweenFormat(start, stop, form, inclusive):
    results = []
    save = False
    index = 0
    for (txt, size, font) in form:
        if start in txt or start == '':
            save = True
        if stop in txt and save:
            if inclusive:
                # includes stop as tail, remainder is without stop
                results.append((txt, size, font))
            else:
                index -= 1  # returns stop as header for remainder
            return results, form[index + 1:]
        if save:
            results.append((txt, size, font))
        index += 1
    # stop not found
    return results, []


def findFromFormat(start, form, inclusive):
    findBetweenFormat(start, 'something_that_will_never_be_found', form, inclusive)


# counts for every text CONTAINING the search string
def countStr(string, searchFont, section):
    count = 0
    for (txt, size, font) in section:
        if string in txt and font == searchFont:
            count += 1
    return count
