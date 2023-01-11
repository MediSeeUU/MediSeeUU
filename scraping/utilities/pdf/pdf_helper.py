import fitz


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


def get_text(blocks: list[dict], results: list[(str, int, str)], lower: bool):
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

# Given a pdf, returns one long string of text
def get_text_str(pdf: fitz.Document) -> str:
    """Returns the plain text of a fitz pdf, removing all \\n that are present.

    Args:
    pdf (fitz.Document): The opened pdf document to extract text from

    Returns:
        txt (str): The plain text of a pdf document, without \\n
    """
    pdf_format = get_text_format(pdf)
    txt = format_to_string(pdf_format)
    return txt.replace('\n', '')


def combine_text(lines: dict, lower: bool, old_font: str, old_size: int, old_text: str, results: list[tuple]):
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
    #TODO: more complex splitting needed
    if old_text.strip() != "" and text.strip() != "" and len(old_text.split()) > 1:
        return all((n.isdigit() or n == '.') for n in old_text.split()[0]) and \
               all((n.isdigit() or n == '.') for n in text.split()[0]) and \
               not old_text.split()[1][0].isdigit()
    return False


def is_page_number(char_dict: dict[str, any], page_height: int) -> bool:
    footer_start_height = page_height - (page_height * 0.065)
    char_bbox = char_dict["bbox"]
    return min(char_bbox[1], char_bbox[3]) > footer_start_height  # and char_dict["c"].isdigit()

def span_in_footer(span_dict: dict[str, any], page_height: int) -> bool:
    footer_start_height = page_height - (page_height * 0.065)
    span_bbox = span_dict["bbox"]
    return min(span_bbox[1], span_bbox[3]) > footer_start_height

def filter_page_footer(text_blocks: list[dict[str, any]], page_height: int) -> list[dict[str, any]]:
    for text_block in text_blocks:
        if text_block["type"] != 0:  #skip non text-blocks
            continue

        for line in text_block["lines"]:
            for span in line["spans"]:
                old_text = "".join([char["c"] for char in span["chars"]])
                # new_text = "".join([char["c"] for char in span["chars"] if not is_page_number(char, page_height)])
                # span["text"] = new_text
                span["text"] = old_text

                # split_text = span["text"].split("/")
                # if not span["text"].isdigit() and not (all(map(lambda x: x.isdigit(), split_text)) and len(split_text) == 2):
                #     span["text"] = old_text

                # if old_text != new_text:
                #     print("old", old_text)
                #     print("new", new_text)
            
            line["spans"] = [span for span in line["spans"] if not span_in_footer(span, page_height)]
    
    return text_blocks


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
        dict_ = page.get_text("rawdict")
        page_height = dict_["height"]
        blocks = dict_["blocks"]
        blocks = filter_page_footer(blocks, page_height)
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
    if '_h_' in filename:
        res_to_file("../logs/txt_files/human_initial_dec.txt", res, filename)
    elif '_o_' in filename:
        res_to_file("../logs/txt_files/orphan_initial_dec.txt", res, filename)


def res_to_file(output_path: str, res: dict, filename: str):
    """
    Args:
        output_path (str): Path of the outputfile
        res (dict): dictionary containing all attributes of the PDF file
        filename (str): Name of the PDF file
    """
    write_string = filename
    for value in res.values():
        write_string = f"{write_string}@{str(value)}"
    outputfile = open(output_path, 'a', encoding="utf-8")  # open/clean output file
    outputfile.writelines(write_string)
    outputfile.writelines('\n')
    outputfile.close()
