import fitz
import io


# PDF Helper functions

def append_text(text: str, size: int, font: str, results: list[(str, int, str)], lower: bool):
    """
    Returns the text size and font of every line in a pdf.

    Args:
        text (str): The text to append to the list of results
        size (int): The font size
        font (str): The font of the text to append
        results (list[(str, int, str)]): The final results list of tuples of texts, font sizes, and font names
        lower (bool): Determines whether the text should be lowercase or not
    """
    if lower:
        results.append((text.lower(), size, font))
    else:
        results.append((text, size, font))


def get_text(blocks: list[dict], results: (list[(str, int, str)]), lower: bool):
    """
    Main function to combine text with same size and font, combine headers, and add them to results

    Args:
        blocks (list[dict]): Some section of a PDF document, containing spans that contain lines
        results (list[(str, int, str)]): The final results list of tuples of texts, font sizes, and font names
        lower (bool): Determines whether the text should be lowercase or not
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


def combine_text(lines: dict, lower: bool, old_font: str, old_size: int, old_text: str, results: (list[tuple])):
    """
    Helper function that actually combines text with same size and font, combines headers, and adds them to results

    Args:
        lines (dict): Line of text to add to the results
        lower (bool): Determines whether the text should be lowercase or not
        old_font (str): The font of current text to which lines['font'] can be added
        old_size (int): The font size of current text to which lines['size'] can be added
        old_text (str): The current text to which lines['text'] can be added
        results (list[tuple]): The final results list of tuples of texts, font sizes, and font names
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


def get_text_format(pdf: fitz.Document, lower: bool = False) -> list[(str, int, str)]:
    """
    Returns formatted text from PDF document, optionally lowered

    Args:
        pdf (fitz.Document): PDF document
        lower (bool): Whether text should be lowercase

    Returns:
        (list[(str, int, str)]): Formatted text as a list of tuples of text, font size, and font name
    """
    results = []
    for page in pdf:
        dict_ = page.get_text("dict")
        blocks = dict_["blocks"]
        get_text(blocks, results, lower)
    return results


def format_to_string(section: list[(str, int, str)]) -> str:
    """
    Converts a formatted text to normal string

    Args:
        section (list[(str, int, str)]): Formatted PDF document, list of tuples of text, font size, and font name
    Returns:
        str: All text in document

    """
    res = ''
    for (txt, _, _) in section:
        res += txt
    return res


def create_outputfile_dec(filename: str, res: dict):
    """
    Args:
        filename (str): Name of the PDF file
        res (dict): dictionary containing all attributes of the PDF file
    """
    write = False
    if '_h_' in filename:
        f = open('human_initial_dec.txt', 'a', encoding="utf-8")  # open/clean output file
        write = True
    elif '_o_' in filename:
        f = open('orphan_initial_dec.txt', 'a', encoding="utf-8")  # open/clean output file
        write = True
    if write:
        res_to_file(f, res, filename)
        f.close()


def create_outputfile(filename: str, outputname: str, res: dict):
    """
    Args:
        filename (str): Name of the PDF file
        outputname (str): Name to be written to
        res (dict): dictionary containing all attributes of the PDF file
    """
    f = open(outputname, 'a', encoding="utf-8")  # open/clean output file
    res_to_file(f, res, filename)
    f.close()


def res_to_file(f: io.TextIOWrapper, res: dict, filename: str):
    """
    Args:
        f (io.TextIOWrapper): File to write results to for visualisation of the attributes
        res (dict): dictionary containing all attributes of the PDF file
        filename (str): Name of the PDF file
    """
    write_string = filename
    for value in res.values():
        write_string += '@'
        write_string += str(value)
    f.writelines(write_string)
    f.writelines('\n')
