import fitz
# PDF Helper functions

def append_text(text: str, size: int, font: str, results: [(str, int, str)], lower: bool):
    """
    Returns the text size and font of every line in a pdf.
    Args:
        text (str): The text to append to the list of results
        size (int): The font size
        font (str): The font of the text to append
        results ([(str, int, str)]): The final results list of tuples of texts, font sizes, and font names
        lower (bool): Determines whether the text should be lowercase or not

    Returns:
        None

    """
    if lower:
        results.append((text.lower(), size, font))
    else:
        results.append((text, size, font))


def get_text(blocks: [dict], results: ([(str, int, str)]), lower: bool):
    """
    Main function to combine text with same size and font, combine headers, and add them to results

    Args:
        blocks ([dict]): Some section of a PDF document, containing spans that contain lines
        results ([(str, int, str)]): The final results list of tuples of texts, font sizes, and font names
        lower (bool): Determines whether the text should be lowercase or not

    Returns:
        None

    """
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


def combine_text(lines: dict, lower: bool, old_font: str, old_size: int, old_text: str, results: ([(str, int, str)])):
    """
    Helper function that actually combines text with same size and font, combines headers, and adds them 2to results

    Args:
        lines (dict): Line of text to add to the results
        lower (bool): Determines whether the text should be lowercase or not
        old_font (str): The font of current text to which lines['font'] can be added
        old_size (int): The font size of current text to which lines['size'] can be added
        old_text (str): The current text to which lines['text'] can be added
        results ([(str, int, str)]): The final results list of tuples of texts, font sizes, and font names

    Returns:
        None

    """
    text = lines['text']
    size = lines['size']
    font = lines['font']
    # Start new line when a header number is found after
    # another header number with text behind it
    if header_split_check(old_text, text):
        append_text(old_text.replace("\\\\", "\\"), old_size, old_font, results, lower)
        old_font, old_size, old_text = font, size, text
    # Combine text that has the same size and font
    # Also combine text that has the same size and is Bold
    elif round(old_size) == round(size) and \
            (old_font == font or 'Bold' in old_font and 'Bold' in font):
        old_text += text + '\n '
        old_size, old_font = size, font
    # Add all spaces at the end
    # Sometimes, spaces are of a different font randomly
    elif text.isspace():
        old_text += text
    # Old text becomes new text to be added in a next iteration
    elif old_text == '':
        old_font, old_size, old_text = font, size, text
    # Text is different format, add old_text to results and replace it with new text
    else:
        append_text(old_text.replace("\\\\", "\\"), old_size, old_font, results, lower)
        old_font, old_size, old_text = font, size, text
    return old_font, old_size, old_text


def header_split_check(old_text: str, text: str) -> bool:
    """
    Checks whether two header texts should be split or combined
    Splits when old_text contains header number and header text, and
    text contains a header number.
    Append text to old_text otherwise.

    Args:
        old_text (str): The current built-up text or line to which text can be added
        text: The new text to concatenate to old_text

    Returns:
        bool: True if old_text should be split from text, False otherwise
    """
    if old_text.strip() != "" and text.strip() != "" and len(old_text.split()) > 1:
        return all((n.isdigit() or n == '.') for n in old_text.split()[0]) and \
               all((n.isdigit() or n == '.') for n in text.split()[0]) and \
               not old_text.split()[1][0].isdigit()
    return False


def get_text_format(pdf: fitz.Document, lower: bool = False) -> [(str, int, str)]:
    """
    Returns formatted text from PDF document, optionally lowered

    Args:
        pdf (fitz.Document): PDF document
        lower (bool): Whether text should be lowercase

    Returns:
        ([(str, int, str)]): Formatted text as a list of tuples of text, font size, and font name
    """
    results = []
    for page in pdf:
        dict_ = page.get_text("dict")
        blocks = dict_["blocks"]
        get_text(blocks, results, lower)
    return results


def format_to_string(section: [(str, int, str)]) -> str:
    """
    Converts a formatted text to normal string

    Args:
        section ([(str, int, str)]): Formatted PDF document, list of tuples of text, font size, and font name
    Returns:
        str: All text in document

    """
    res = ''
    for (txt, _, _) in section:
        res += txt     
    return res


def find_between_format(start: str, stop: str, form, inclusive: bool, minimum_size: int = 0):
    """
    returns all lines from and including start till stop for a given format
    with an optional minimum_size for both start and stop values

    Args:
        start (str):
        stop(str):
        form:
        inclusive (booL):
        minimum_size (int):

    Returns:

    """
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
    for (txt, _, font) in section:
        if string in txt and font == search_font:
            count += 1
    return count
