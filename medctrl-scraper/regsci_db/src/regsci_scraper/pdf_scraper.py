import PyPDF4  # for reading text in PDF
from PyPDF4 import PdfFileReader
import fitz  # PyMuPDF for extracting images from PDF
from PIL import Image  # for reading images from bytes
import pytesseract  # for extracting text from images
import pdfkit
from pdf2image import convert_from_path

from loguru import logger

import os
import re
import shutil
import io
import pandas as pd

from regsci_scraper import utils
from regsci_scraper.file_scrapers import decision_miner as dm
from regsci_scraper.file_scrapers import epar_miner as em
from regsci_scraper.file_scrapers import smpc_miner as sm
from regsci_scraper import website_scraper as ws


class RegSciDB(object):
    """ This class contains the whole Database in self.ec_df

    """
    def __init__(self, directory_path: str):  # path to all PDF data (EPAR, SmPC, decision etc.)
        self.dir = directory_path
        self.ec_df = self.update_ec_df()  # ws.ema_doublecheck(ws.execute_var_pooling(ws.extract_ec_table()))

    def update_ec_df(self):
        """ Update the EC DF by
        1) Extracting data from the EC website (ec_df)
        2) Extract variables from decision PDFs (dec_vars) using the underlying DecisionMiner class
        3) Extract variables from EPARs, scientific discussions & procedural step files using self.get_epar_vars()

        Returns
        -------
        ec_df: the above three steps merged into one dataframe
        """
        # Extract info from EC community register and download Decisions and SmPCs

        # TEST
        #ec_df = ws.extract_ec_table()
        #ec_df = ec_df.loc[ec_df.eunumber_abb.isin(["288", "171", "1181", "1249"])]
        #ec_df = ws.ema_doublecheck(ws.execute_var_pooling(ec_df))

        # REAL
        ec_df = ws.ema_doublecheck(ws.execute_var_pooling(ws.extract_ec_table()))

        ec_df.emanumber_abb = ec_df.emanumber_abb.astype("str")

        # read filepaths and filenames
        decision_names, decision_files = utils.read_filenames(f"{self.dir}/authorisation_decisions/")
        smpc_names, smpc_files = utils.read_filenames(f"{self.dir}/smpcs/")

        # Extract the decision vars from the downloaded Decision files
        i = 0
        col_vals_list = []
        for n, f in zip(decision_names, decision_files):
            decision_file = DecisionMiner(name=n, file=f)
            col_vals = pd.DataFrame(decision_file.variables, index=[i])
            col_vals['emanumber_abb'] = decision_file.id
            col_vals_list.append(col_vals)
            i = i + 1

        dec_vars = pd.concat(col_vals_list)
        dec_vars['emanumber_abb'] = dec_vars.emanumber_abb.astype("str")

        # Extract the decision type from the downloaded SmPC
        i = 0
        col_vals_list = []
        for n, f in zip(smpc_names, smpc_files):
            ema_n = n.strip(".pdf")

            try:  # for some cases no decision date is found
                decision_date = dec_vars.loc[dec_vars.emanumber_abb == ema_n, "decision_date"].iloc[0]
            except IndexError:  # no decision date found for the ema number, use impossible dec date:
                logger.debug(f"{n}: No decision date found in the authorisation decision file")
                decision_date = "01/01/1900"

            try:  # same for the decision type: if not found set decision type to None
                decision_type = dec_vars.loc[dec_vars.emanumber_abb == ema_n, "decision_type"].iloc[0]
            except IndexError:  # no decision type found, take standard?
                logger.debug(f"{n}: No decision type found in the authorisation decision file")
                decision_type = None

            smpc_file = SmPCMiner(name=n, file=f, decision_date=decision_date, decision_type=decision_type)
            col_vals = pd.DataFrame(smpc_file.variables, index=[i])
            col_vals['emanumber_abb'] = smpc_file.id
            col_vals_list.append(col_vals)
            i = i + 1

        smpc_vars = pd.concat(col_vals_list)
        smpc_vars['emanumber_abb'] = smpc_vars.emanumber_abb.astype("str")

        # rm the decision_type col from the Decision variables as this col is overwritten in the SmPC variables
        dec_vars = dec_vars.drop('decision_type', 1)

        # Merge everything
        ec_df = pd.merge(ec_df, dec_vars, on="emanumber_abb", how='left')
        ec_df = pd.merge(ec_df, smpc_vars, on="emanumber_abb", how="left")
        ec_df = pd.merge(ec_df, self.get_epar_vars(), on="emanumber_abb", how='left')

        return ec_df

    def get_epar_vars(self):
        """ Extracts the Legal Basis and PRIority MEdicine from the EPARs
        - If legal basis not found in EPAR --> check scientific discussion file
        - If legal basis not found in scientific discussion file --> check procedural steps file
        - If no EPAR --> check scientific discussion file
        - If no scientific discussion file  --> check procedural steps file

        Returns
        -------
        DataFrame which can be merged with ec_df
        """
        dirpath = f"{self.dir}/epars/"
        epar_names, epar_files = utils.read_filenames(dirpath)
        # separate EPARs from scientific discussions from Procedural Steps files
        sci_disc_names = [n for n in epar_names if n.startswith('s')]  # starts with s  = scientific discussion
        proc_names = [n for n in epar_names if n.startswith('p')]  # every file that starts with p  =Procedural steps
        epar_names = [n for n in epar_names if n not in proc_names and n not in sci_disc_names]
        
        # do the same for the filepaths
        sci_disc_files = [f for f in epar_files if os.path.basename(f).startswith('s')]
        proc_files = [f for f in epar_files if os.path.basename(f).startswith('p')]
        epar_files = [f for f in epar_files if f not in proc_files and f not in sci_disc_files]

        checked_procs = checked_sci_discs = []  # create empty lists for the next for loop
        epar_dict = {}  # create dict to store variables
        
        # Check in EPARs if you can find Legal Basis & PRIME
        for n, f in zip(epar_names, epar_files):
            # add key to dict & add emanumber_abb as key-var
            epar_dict[n.strip(".pdf")] = {
                "emanumber_abb": n.strip(".pdf")
            }
            
            legal_basis = None
            prime = "no"
            text = extract_data(name=n, file_path=f)
            for t in text:
                if legal_basis is None:  # if legal_basis not found try again
                    legal_basis = em.extract_legalbasis(text=t)
                if prime == "no":  # if prime not found try again
                    prime = em.extract_prime(text=t)
                elif legal_basis is not None and prime == "yes":  # if both found break the loop, otherwise continue
                    break

            epar_dict[n.strip(".pdf")]["prime"] = prime  # add prime to dict

            # IF legal_basis not found in EPAR, check scientific discussions
            if legal_basis is None:
                sci_disc_name = "s" + n
                sci_disc_file = [f for f in sci_disc_files if sci_disc_name in f]
                if len(sci_disc_file) > 1:  # if multiple discussions found raise error, this should not be possible!
                    raise ValueError(f"Duplicate files found for '{sci_disc_name}'.")
                elif len(sci_disc_file) == 1:
                    text = extract_data(name=n, file_path=f)
                    for t in text:
                        legal_basis = em.extract_legalbasis(text=t)
                        if legal_basis is not None:  # if legal basis found break loop
                            break

                else:  # else no sci_disc file found and legal_basis is thus None
                    legal_basis = None
                checked_sci_discs.append(sci_disc_name)  # add checked sci_disc to list to later substract from all

            # IF not found in EPAR nor in scientific discussion, check Procedural steps taken before authorisation file
            if legal_basis is None:
                proc_name = "p" + n
                proc_file = [f for f in proc_files if proc_name in f]
                if len(proc_file) > 1:  # Should only be one Procedural steps file with this filepath+name
                    raise ValueError(f"Duplicate files found for '{proc_name}'.")  # multiple files found with same name
                elif len(proc_file) == 1:
                    text = extract_data(name=n, file_path=f)
                    for t in text:
                        legal_basis = em.extract_legalbasis(text=t)
                        if legal_basis is not None:  # if legal basis found break loop
                            break
                else:  # else no procedural steps file found and legal_basis is thus None
                    legal_basis = None
                checked_procs.append(proc_name)  # add checked Proc file to list to later substract from all Proc files

            # add the legal basis to the dict
            epar_dict[n.strip(".pdf")]["legal_basis"] = legal_basis

        # Some scientific discussions and Procedural steps files are skipped, since they don't have a corresponding EPAR
        # e.g. (s212.pdf but no 212.pdf)
        remaining_sci_discs = [n for n in sci_disc_names if n not in checked_sci_discs]
        for n in remaining_sci_discs:
            # add key to dict & add emanumber_abb as key-var
            epar_dict[n[1:].strip(".pdf")] = {
                "emanumber_abb": n[1:].strip(".pdf")
            }
            
            legal_basis = None
            text = extract_data(name=n, file_path=dirpath + n)
            for t in text:
                legal_basis = em.extract_legalbasis(text=t)
                if legal_basis is not None:  # if no legal basis found continue for loop, else break
                    break
            if legal_basis is None:  # if legal basis not found in scientific discussion, check Procedural steps file
                proc_name = "p" + n[1:]
                proc_file = [f for f in proc_files if proc_name in f]
                if len(proc_file) > 1:  # There should only be one procedural steps file!
                    raise ValueError(f"Duplicate files found for '{proc_name}'.")
                elif len(proc_file) == 1:
                    text = extract_data(name=n, file_path=proc_file[0])
                    for t in text:
                        legal_basis = em.extract_legalbasis(text=t)
                        if legal_basis is not None:  # if legal basis found break loop
                            break
                else:  # no procedural steps file, legal_basis is thus None
                    legal_basis = None
                checked_procs.append(proc_name)

            epar_dict[n[1:].strip(".pdf")]["legal_basis"] = legal_basis

        # Some PROC files do not correspond with a scientific discussion nor EPAR
        # e.g. (p212.pdf but no s212.pdf nor 212.pdf
        remaining_procs = [n for n in proc_names if n not in checked_procs]
        for n in remaining_procs:
            epar_dict[n[1:].strip(".pdf")] = {
                "emanumber_abb": n[1:].strip(".pdf")
            }
            legal_basis = None
            text = extract_data(name=n, file_path=dirpath + n)
            for t in text:
                legal_basis = em.extract_legalbasis(text=t)
                if legal_basis is not None:  # if legal basis found break loop
                    break
            epar_dict[n[1:].strip(".pdf")]["legal_basis"] = legal_basis

        return pd.DataFrame.from_dict(epar_dict, orient="index")  # return a DF (from epar_dict)


class DecisionMiner(object):
    """ The DecisionMiner class mines Decision PDFs
    - Needs the name of the file (e.g. '282.pdf')
    - Needs the filelocation (e.g. ~/Documents/282.pdf) 
    """
    def __init__(self, name: str, file: str):
        self.name = name
        self.file = file
        self.id = name.strip(".pdf")  # emanumber_abb
        self.text = extract_data(name, file)
        self.variables = self.get_decision_vars()

    def get_decision_vars(self):
        brand_name = legal_scope = decision_type = decision_date = odd = atmp = new_as = None
        for t in self.text:
            if t is None:
                continue
            if brand_name is None:
                brand_name = dm.extract_brandname_1(t)
            if legal_scope is None:
                legal_scope = dm.extract_legalscope(t)
            if decision_type is None:
                decision_type = dm.extract_decisiontype(t)
            if decision_date is None:
                decision_date = dm.extract_decisiondate(t)
            if odd is None or odd == "no" or odd == "appointed":
                odd = dm.extract_odd(t, odd)
            if atmp is None or atmp == "no":
                atmp = dm.extract_atmp(t)
            if new_as is None or new_as == "no":
                new_as = dm.extract_new_as(t)

        decision_vars = {
            "brand_name": brand_name,
            "legal_scope": legal_scope,
            "decision_type": decision_type,
            "decision_date": decision_date,
            "orphan_drug": odd,
            "ATMP": atmp,
            "new_active_substance": new_as
        }
        return decision_vars


class SmPCMiner(object):
    """ The SmPCMiner class mines the SmPC annexes downloaded from the EC Com Reg website
    - Needs the name of the file (e.g. '282.pdf')
    - Needs the filelocation (e.g. ~/Documents/282.pdf)
    - Needs the Decision Date obtained from the DecisionMiner class
    """
    def __init__(self, name: str, file: str, decision_type: str, decision_date: str):
        self.name = name
        self.file = file
        self.id = name.strip(".pdf")  # emanumber
        self.text = extract_data(name, file)
        self.dec_date = decision_date
        self.dec_type = decision_type
        self.variables = self.get_smpc_vars()

    def get_smpc_vars(self):
        decision_smpc = None
        for t in self.text:
            if t is None:
                continue
            if decision_smpc is None:
                decision_smpc = sm.extract_decisiontype(t, self.dec_date)

        cond = "conditional"
        excp = "exceptional"

        # Exceptional in decision and exceptional in SmPC (<2006)
        if self.dec_type == excp and decision_smpc == excp:
            decision_type = f"{excp} (SmPC confirmed)"
        # Exceptional in decision and exceptional in SmPC (>2006)
        elif self.dec_type == excp and decision_smpc == "both":
            decision_type = f"{excp} (SmPC confirmed)"
        # Exceptional in decision, but exceptional not found in SmPC
        elif self.dec_type == excp and decision_smpc is None:
            decision_type = excp
        # Conditional in decision, conditional in SmPC (>2006)
        elif self.dec_type == cond and decision_smpc == "both":
            decision_type = f"{cond} (SmPC confirmed)"
        # Conditional in decision, but conditional not found in SmPC
        elif self.dec_type == cond and decision_smpc is None:
            decision_type = cond
        # Conditional in decision, but exceptional in SmPC (<2006) -> ERROR!
        elif self.dec_type == cond and decision_smpc == excp:
            decision_type = "error (conflicting SmPC and Decision)"
        # No conditional nor exceptional in Decision, no conditional nor exceptional in SmPC
        elif self.dec_type is None and decision_smpc is None:
            decision_type = "standard (SmPC confirmed)"
        # No conditional nor exceptional in Decision, but exceptional in SmPC
        elif self.dec_type is None and decision_smpc == excp:
            decision_type = f"{excp} (conflicting SmPC and Decision)"
        # No conditional nor exceptional in Decision, but conditional or exceptional in SmPC
        elif self.dec_type is None and decision_smpc == "both":
            decision_type = f"{excp} or {cond} (conflicting SmPC and Decision)"
        else:
            decision_type = None

        return {
            "decision_type": decision_type
        }


def text_from_pdf(name: str, file_path: str):
    """ Extracts text from PDF

    Parameters
    ----------
    name: name of the decision PDF document
    file_path: path to the decision PDF document

    Returns
    -------
    text: raw text of PDF file
    true_path: the true path name in case the file has been fixed
    """
    html_path = file_path.replace(".pdf", ".html")
    fixed_path = file_path.rstrip(".pdf")+"_fixed.pdf"

    # if os.path.getsize(file_path) < 8500:  # corrupted files are ~8300 bytes
    #     return [], file_path
    with open(file_path, 'rb') as f:
        logger.info(f"opening file '{name}'..")
        try:
            pdf = PdfFileReader(f)
        # Except PDF read error: can be EOF error or corrupted HTML file
        except PyPDF4.utils.PdfReadError:
            contents = f.read()

            # If contents is a HTML Webpage:
            if contents[-8:] == b"</html>\n":
                logger.info(f"File corrupted: {name} is HTML file")
                f.close()  # close file
                # copy corrupt .pdf file and rename to .html file
                shutil.copy(file_path, html_path)
                # transpose html to readable PDF
                try:
                    pdfkit.from_file(html_path, fixed_path)
                except OSError:  # pdfkit is a wrapper for wkhtmltopdf, which throws an OSError that can be ignored
                    pass

            # Else probably a EOF error:
            else:
                logger.info(f"File corrupted: {name} (EOF error)")
                f.close()
                logger.info(f"closing file and rewriting EOF..")
                utils.reset_eof(file_path, fixed_path)
            
            logger.info(f"cleaned file, opening again..")

    if os.path.isfile(fixed_path):  # if fixed_path exists, use fixed file
        logger.debug(f"Fixed file found for {fixed_path}")
        true_path = fixed_path
    else:  # if not use normal file
        true_path = file_path

    # try to open (fixed) PDF again, if it fails skip reading this file!
    with open(true_path, 'rb') as f:
        try:
            pdf = PdfFileReader(f)
        except PyPDF4.utils.PdfReadError:  # again PDF read error --> return empty text
            return [], true_path

        number_of_pages = pdf.getNumPages()
        logger.info(f"{name}: file contains {len(range(number_of_pages))} pages")

        # create and cleanse the text object per page (brandname is found on different pages)
        all_text = []
        for n in range(number_of_pages):
            page_obj = pdf.getPage(n)
            text = page_obj.extractText()
            text = correct_chars(text)
            all_text.append(text)

    return all_text, true_path


def pdf_pictures2text(name: str, file_path: str):
    """ Read pictures in PDF files and convert them to text

    Parameters
    ----------
    name: The name of the PDF file
    file_path: path to the PDF document

    Returns
    -------
    all_text: A list containing strings (each picture is converted to a string)
    """

    # open PDF
    try:
        pdf_file = fitz.open(file_path)
    except RuntimeError:
        logger.info(f"Most likely corrupted file: '{name}'")
        return []

    image_list = []

    # Extract images
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list.extend(page.get_images())

    if len(image_list) == 0:
        logger.info(f"no images found in {name}")
        return None
    else:
        logger.info(f"{name}: found {len(image_list)} images on {pdf_file.pageCount} pages")

    # For each picture in image_list, convert it to text with pytesseract
    all_text = []
    for img in image_list:
        # get the XREF of the image
        xref = img[0]

        # extract the image bytes
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))
        try:
            text = pytesseract.image_to_string(image)
        except TypeError:
            logger.debug(f"{name}: filetype '{base_image['ext']}' not supported")
            text = ""
        text = correct_chars(text)
        all_text.append(text)

    return all_text  # list


def extract_data(name: str, file_path: str):
    """ Combine results from pdf_pictures2text & text_from_pdf

    Parameters
    ----------
    name: name of PDF file
    file_path: path to PDF file

    Returns
    -------
    all_text: list containing text string from text & picture mining
    """
    text, true_path = text_from_pdf(name, file_path)

    # if not many chars are read from the text extraction read images:
    # if len("".join(text)) < 150:
    all_text = pdf_pictures2text(name, true_path)
    # else:
    #     all_text = None

    # if no images read in PDF:
    if all_text is None or len(all_text) == 0:
        # if no useful text extracted either, convert whole pdf into img and read:
        if len("".join(text)) < 150:
            return convert_pdf2img(name, true_path)
        else:  # else text is useful and return only text
            return text
    else:  # else both images read in PDF and text are useful
        all_text.extend(text)
        return all_text


def convert_pdf2img(name: str, file_path: str):
    """ Converts a whole PDF into images to be read with pytesseract

    Parameters
    ----------
    name: name of PDF file
    file_path: path to PDF file

    Returns
    -------
    all_text: list containing text mined from the images with pytesseract
    """
    try:
        imgs = convert_from_path(file_path, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
    except:
        return []

    all_text = []
    for img in imgs:
        try:
            text = pytesseract.image_to_string(img)
        except TypeError:
            logger.debug(f"{name}: not supported by pytesseract")
            text = ""

        text = correct_chars(text)
        all_text.append(text)

    return all_text


def correct_chars(text: str):
    """ Correct charactes in string (read with PyPDF4 and pytesseract)

    Parameters
    ----------
    text: string to be corrected

    Returns
    -------
    text: corrected string
    """
    text = re.sub(r'\n', ' ', text)  # some PDF's contain random \n (newline) chars in sentences
    text = re.sub(r' +', ' ', text)  # remove double spaces
    text = text.replace('ﬁ', '"')  # adjust wrongly read left " character
    text = text.replace('ﬂ', '"')  # adjust wrongly read right " character
    text = text.replace('Œ', '-')  # adjust wrongly read - character

    return text
