# pdf helper functions

# Returns the text size and font of every line in a pdf.

def append_text(text, size, font, results, lower):
    if lower:
        results.append((text.lower(), size, font))
    else:
        results.append((text, size, font))


# Combine text with same size and font, combine headers, and add them to results
def get_text(blocks, results, lower):
    old_text = old_font = ''
    old_size = 0
    for block in blocks:
        if "lines" in block.keys():
            spans = block['lines']
            for span in spans:
                data = span['spans']
                for lines in data:
                    old_font, old_size, old_text = combine_text(lines, lower, old_font, old_size, old_text, results)
    append_text(old_text, old_size, old_font, results, lower)


def combine_text(lines, lower, old_font, old_size, old_text, results):
    text = lines['text']
    size = lines['size']
    font = lines['font']
    # Combine text that has the same size and font
    # Also combine text that has the same size and is Bold
    if round(old_size) == round(size) and \
            (old_font == font or 'Bold' in old_font and 'Bold' in font):
        old_text += text
        old_size = size
        old_font = font
    # Old text becomes new text to be added in a next iteration
    elif old_text == '':
        old_text = text
        old_size = size
        old_font = font
    # Text is different format, add old_text to results and replace it with new text
    else:
        append_text(old_text, old_size, old_font, results, lower)
        old_text = text
        old_size = size
        old_font = font
    return old_font, old_size, old_text


# returns formatted text from PDF document, optionally lowered
def get_text_format(pdf, lower=False):
    results = []
    for page in pdf:
        dict_ = page.get_text("dict")
        blocks = dict_["blocks"]
        get_text(blocks, results, lower)
    return results


# filters text on certain fonts or font types
# returns all text when empty font lists are given
def filter_font(font_size, font_list, section):
    res = []
    for (txt, size, font) in section:
        # remove empty txt or only spaces
        if txt == " " or txt.count(' ') == len(txt):
            continue

        if round(size, 1) in font_size or font_size == []:
            if font in font_list or font_list == []:
                res.append(txt)
    return res


# returns all lines from and including start till stop for a given format
# with an optional minimum_size for both start and stop values
def find_between_format(start, stop, form, inclusive, minimum_size=0):
    results = []
    save = save_last_true = False
    index = 0
    for (txt, size, font) in form:
        save = start_found(save, start, txt, size, minimum_size)
        if stop in txt and save_last_true and size > minimum_size:
            return get_until_stop(font, form, inclusive, index, results, size, txt)
        if save:
            save_last_true = True
        if save_last_true:
            results.append((txt, size, font))
        index += 1
    # stop not found
    return results, []


# Return results and the last line if inclusive is true to find_between_format
def get_until_stop(font, form, inclusive, index, results, size, txt):
    if inclusive:
        # includes stop as tail, remainder is without stop
        results.append((txt, size, font))
    else:
        index -= 1  # returns stop as header for remainder
    return results, form[index + 1:]


def start_found(save, start, txt, size, minimum_size):
    if start == '':
        return True
    if start in txt and size > minimum_size:
        save = True
    return save


# returns all lines from and including start till the end of the format
def find_from_format(start, form, inclusive, minimum_size=0):
    return find_between_format(start, 'something_that_will_never_be_found', form, inclusive, minimum_size)


# counts for every text CONTAINING the search string
def count_str(string, search_font, section):
    count = 0
    for (txt, size, font) in section:
        if string in txt and font == search_font:
            count += 1
    return count
