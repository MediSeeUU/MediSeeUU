# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
# Reads the tables from PDF files.

import pandas as pd
import tabula
import camelot
import numpy as np
import re
from loguru import logger

# REGULAR EXPRESSIONS for the EU Procedure Numbers
EMA_Markers = [
    "/0000",
    r"N\/\d{4}",
    r"IA\/\d{4}",
    r"IAIN\/\d{4}",
    r"IB\/\d{4}",
    r"II\/\d{4}",
    r"X\/\d{4}",
    r"S\/\d{4}",
    r"T\/\d{4}",
    r"R\/\d{4}",
    r"Z\/\d{4}",
    r"IG\/\d{4}",
    "/G",
    "WS",
    r"A-\d\d\(\d\)\/\d{4}",
    r"PSUSA\/\d{5}\/\d{6}"
]

# Change the order of cols (old columns)
EPAR_cols_old = [
    "Application number",
    "Scope",
    "Opinion/ Notification issued on",
    "Commission Decision Issued / amended on",
    "Product Information affected",
    "Summary",
]

# Change the order of cols (new columns)
EPAR_cols_new = [
    "Product",
    "Application number",
    "Opinion/ Notification issued on",
    "Commission Decision Issued / amended on",
    "Product Information affected",
    "Summary",
    "Scope"
]


def epar_pdf2df(filepath: str):
    """ Converts tables in the 'Procedural steps taken after authorizxation' EPAR PDF documents to Pandas DataFrames

    Parameters:
    ----------
    filepath: string of the path to the PDF file

    Returns
    -------
    product_name: Name of the medicinal product addressed in the EPAR (taken from the EMA document name)
    df: Pandas DataFrame of the tables in the EPAR document
    """
    logger.info(f"filepath: {filepath}")  # log the filepath

    # Tabula checks all pages and creates one consecutive table; converts it to DF
    df = tabula.read_pdf(filepath, pages="all", multiple_tables=False)[0]

    # search product name
    if not re.search("(\w+)-epar-", filepath) is None:
        product_name = re.search("(\w+)-epar-", filepath)[1].capitalize()
        logger.info(f"product name: {product_name}")
    else:
        raise ValueError("No product_name found in filename: check if product_name right before '-epar'.")

    return product_name, df


def check_epar_cols(df: pd.DataFrame):
    """ Checks the columns of the previous aquired DF on the column names, based on the column names described above

    Parameters
    ----------
    df: Result from epar_pdf2df function

    Returns
    -------
    df: df with corrected columns
    """

    # check if length of columns is ok (SHOULD ALSO LOOK AT COL NAMES...)
    if len(df.columns) != len(EPAR_cols_old):
        raise ValueError(f"The columns of the DF do not correspond with EPAR headers: "
                         f"{len(df.columns)}-{len(EPAR_cols_old)}")
    df.columns = EPAR_cols_old
    df['Product'] = None
    df = df[EPAR_cols_new]

    # probably first 5 rows are always wrongly read by Tabula
    df = df.drop(df.index[0:4])
    df = df.reset_index(drop=True)
    logger.info("correct headers added")
    return df


def filter_epar_df(product_name: str, df: pd.DataFrame):
    """ Tabula wrongly reads headers and takes into account footers.
    Possibly redundant function when using additional parameters in Tabula or Camelot read_pdf function

    Parameters
    ----------
    product_name: Name of the product for the EPAR
    df: Result from epar_pdf2df function

    Returns
    -------
    df: df with corrected information
    """

    ix = 0
    del_rows = []

    # add correct headers:
    df = check_epar_cols(df)
    # remove footer wrongly incorporated by Tabula
    df = df.loc[
        (~df[EPAR_cols_new[1]].str.contains("EMA/", na=False)) &
        (~df[EPAR_cols_new[1]].str.contains(product_name, na=False))
        ]
    df = df.reset_index(drop=True)
    logger.info("wrongly incorporated footers removed")

    # Correct the information in the lines
    for i, v in enumerate(df[EPAR_cols_new[1]]):
        # skip first hit
        if i == 0:
            continue
        # check for EMA marker in the form */xxxx* or */G*
        elif isinstance(v, str):
            # if v very long, it's probably not a marker
            if len(str(v)) > 18:
                del_rows.append(i)
            # if v not very long, check with RegEx for EU procedure number
            elif not re.search(r"\/\d{4}", v) is None or "/G" in v:
                # PSUSA Markers are wrongly read by Tabula over two lines, this part corrects that:
                # if /xxxxxx in value (PSUSA):
                if not re.search(r"\/\d{6}", v) is None:
                    # if PSUSA/ is not in the row right before /xxxxxx: search in more previous rows:
                    if "PSUSA/" not in str(df[EPAR_cols_new[1]][i - 1]):
                        for j in range(0, i):
                            # avoid hits that are PSUSA/xxxxx/xxxxxx
                            if "PSUSA/" in str(
                                    df[EPAR_cols_new[1]][i - j]
                            ):
                                if re.search(r"PSUSA\/\d{5}\/\d{6}", str(df[EPAR_cols_new[1]][i - j])
                                             ) is None:
                                    xj = j  # xj found
                                    break
                        # now concat all rows between i-xj and i
                        if xj is None or xj != j:
                            xj = 0
                        for col in df.columns:
                            psusa = df[col][i - xj:i + 1].str.cat(sep='')
                            df[col][i - xj] = psusa
                        del_rows.extend([x for x in range(i, i - xj, -1)])
                    # if PSUSA/ is in row right before /xxxxxx, it's simple:    
                    else:
                        for col in df.columns:
                            psusa = df[col][i - 1:i + 1].str.cat(sep='')
                            df[col][i - 1] = psusa
                        del_rows.append(i)

                # all other markers and sequential nan lines should be merged:
                else:
                    new_ix = i
                    # merge values of rows from previous marker to current marker at the previous marker cell
                    for col in df.columns:
                        if not df[col][ix:new_ix].isnull().all():  # if all nan, skip
                            value = df[col][ix:new_ix].str.cat(sep=' ')
                            if "PSUSA" in value:
                                pass
                            else:
                                df[col][ix] = value
                    ix = new_ix  # update old marker

        # all nan lines at marker col should be deleted after concatenation            
        elif isinstance(v, float):
            if np.isnan(v):
                del_rows.append(i)

    logger.info("EMA markers filtered")
    # reindex
    df = df.drop(df.index[del_rows])
    df = df.dropna(subset=[EPAR_cols_new[2]])  # drop nan's at date
    df = df.reset_index(drop=True)

    for i, v in enumerate(df[EPAR_cols_new[1]]):
        if len(str(v)) > 18:
            if not re.search(r"PSUSA\/\d{5}\/\d{6}", v) is None:
                df[EPAR_cols_new[1]][i] = v[0:18]
            elif not re.search(r"\/\d{4}", v) is None:
                if "/G" in v:
                    df[EPAR_cols_new[1]][i] = v[0:9]
                else:
                    df[EPAR_cols_new[1]][i] = v[0:7]
    for i, v in enumerate(df[EPAR_cols_new[2]]):
        df[EPAR_cols_new[2]][i] = str(v)[0:10]
    df['Product'] = product_name
    logger.info("dates corrected, data ready")
    return df