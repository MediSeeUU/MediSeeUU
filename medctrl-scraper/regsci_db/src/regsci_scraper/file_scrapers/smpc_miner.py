# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
# Contains the following variables mined in SmPC PDF files:
# 1 Decision Type

from datetime import datetime


def extract_decisiontype(text: str, decision_date: str = None):
    """ Extract the type of decision [categorical, exceptional, standard]

    Parameters
    ----------
    text: The raw text of the SmPC Annex PDF file
    decision_date: The result of the decision_date() func from the decision_miner.py script

    Returns
    -------
    one of the following [categorical, exceptional, standard]
    """
    # if no decision date is given, not sure if older than 2006; so could be exceptional or conditional
    if decision_date is None:
        year = 2006
    else:
        year = datetime.strptime(decision_date, "%d/%m/%Y").year

    # conditional did not exist before 2006
    if year < 2006 and "specific obligation" in text:
        return "exceptional"

    # after 2006 could be exceptional or conditional
    elif "specific obligation" in text:
        return "both"
    else:
        return None


