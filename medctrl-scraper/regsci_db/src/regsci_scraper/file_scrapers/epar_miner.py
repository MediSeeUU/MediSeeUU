# Contains the following variables mined in EPAR PDF files:
# 1 Legal Basis
# 2 PRIME: Priority Medicine

from regsci_scraper import utils
from loguru import logger


def extract_legalbasis(text: str):
    lb = "legal basis"
    legal_bases = None
    text = text.lower()
    if lb in text.lower():
        lbidx = text.rindex(lb)
        target = text[lbidx:lbidx + 100].lower()
        legal_bases = [b for b in utils.lbases if b in target or b.replace(",", ")") in target]
        legal_bases = list(set(legal_bases))

    if not legal_bases or legal_bases is None:
        return None
    else:
        if len(legal_bases) > 1:
            logger.info(f"Multiple legal bases found: {legal_bases}")
        return legal_bases


def extract_prime(text: str):
    """ Check if medicines is part of PRIME (Priority Medicine)

    Parameters
    ----------
    text: The raw text of the decision PDF file

    Returns
    -------
    prime: Boolean value stating if the product is a priority medicine
    """
    if "priority medicine" in text or " prime " in text:
        prime = "yes"
    else:
        prime = "no"

    return prime
