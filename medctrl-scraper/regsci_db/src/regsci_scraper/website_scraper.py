# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
# Scraper for websites, download files automatically
# 1. First extract the EC table using extract_ec_table()
# 2. Second use execute_var_pooling(ec_df) to mine the variables from the EC individual product pages
# 3. Third use ema_doublecheck(ec_df) to correct the EMA numbers (check log file afterwards)
# 4. Fourth use execute_download_pooling(ec_df) to download the EPARs from the EMA website
# 5. Five retrieve SmPCs (to be implemented)

import requests
import bs4
from loguru import logger
import re
import os
from datetime import datetime
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from regsci_scraper import utils

debug_file = "./log/debug.log"
if os.path.exists(debug_file):
    os.remove(debug_file)
logger.add(debug_file, level="DEBUG", retention=True)


def scrape_website(url: str):
    """ Use requests to read URL (preferably EMA or EC website) and return BS4 soup object

    Parameters
    ----------
    url: The URL of the website you would like to create a BS4 object of

    Returns
    -------
    BS4 object
    """
    if "ema.europa.eu" not in url and "ec.europa.eu" not in url:
        logger.warning("You are not retrieving information from the EMA or EC websites, are you sure?")
    # try to retrieve information
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)  # if requests fails raise error

    return bs4.BeautifulSoup(r.text)


def download_minutes_prac_meetings(output_directory: str):
    """ Automatically download the minutes of the PRAC meetings. Uses the retieve_epars_automatically function.

    Parameters
    ----------
    output_directory: Give the path to the directory you would like to save the Minutes of the PRAC meetings to.

    Returns
    -------

    """
    url = "https://www.ema.europa.eu/en/committees/prac/prac-agendas-minutes-highlights"
    soup = scrape_website(url)

    # listings = soup.findAll('ul', attrs={'class': re.compile('ema-listings')})
    links = soup.findAll('a', attrs={'class': re.compile("ecl-link ecl-list-item__link")})

    for i, link in enumerate(links):
        url_name = re.match(r'.*/documents/minutes/(minutes-prac-meeting-.*.pdf)', link['href'])
        try:
            name = url_name[1]
            logger.debug(f"SUCCES: {name}")
            r = requests.get(link['href'])
            with open(f'{output_directory}{name}', 'wb') as f:
                f.write(r.content)
                f.close()
        except(TypeError, ValueError, IndexError):
            logger.debug(f"no regex match for {link['href']}")


def execute_download_pooling(ec_df: pd.DataFrame):
    """ Similar to execute_var_pooling(). Splits the DF and divides every part over a CPU for faster calculation

    Parameters
    ----------
    ec_df: the DataFrame

    Returns
    -------
    ec_df: the DataFrame with the updated data
    """
    ec_df['epar_doc'] = None
    pools = os.cpu_count() - 1  # check how many CPUs there are and use almost all of them
    logger.info(f"using {pools} CPUs")
    partial_dfs = np.array_split(ec_df, pools)  # split the DF based on the number of CPUs

    with ThreadPoolExecutor(max_workers=pools) as executor:
        df_generator = executor.map(pool_download_epar_ema, partial_dfs)  # appoint each pool to pool_download_epar_ema
    df_list = list(df_generator)
    ec_df = pd.concat(df_list)  # merge the pooled dfs together again

    correct_df = ec_df[~ec_df.epar_doc.isna()]
    redo_df = ec_df[ec_df.epar_doc.isna()]
    logger.info(f"Redoing search with product name for {len(redo_df)} products")
    partial_dfs = np.array_split(redo_df, pools)

    logger.info("joining EPAR pooling results...")
    with ThreadPoolExecutor(max_workers=pools) as executor:
        df_generator = executor.map(pool_download_epar_ema, partial_dfs)  # appoint each pool to pool_download_epar_ema
    df_list = list(df_generator)
    ec_df = pd.concat([correct_df] + df_list)  # merge the pooled dfs together again

    return ec_df


def pool_download_epar_ema(partial_df: pd.DataFrame):
    """ Similar to pool_var_extraction(). Obtains a partial df from execute_download_pooling() and
    executes the download_epars() function.

    Parameters
    ----------
    partial_df: Partial DF obtained from execute_download_pooling()

    Returns
    -------
    partial_df: Updated partial df to be merged later in execute_download_pooling()
    """
    partial_df['epar_doc'] = partial_df.apply(
        lambda x: download_epars(idx=x['emanumber_abb'], output_dir='regsci_db/data/epars/', typ='ema', name=x['emanumber_abb']), axis=1
    )
    return partial_df


def pool_download_epar_name(partial_df: pd.DataFrame):
    """ Same as pool_download_epar_ema but searches on product name instead of EMA number"""
    partial_df['epar_doc'] = partial_df.apply(lambda x: download_epars(
        idx=x['lname'], output_dir='regsci_db/data/epars/', typ='name', name=x['emanumber_abb'], initial_docs=False
    ), axis=1)
    return partial_df


def download_epars(idx: str, typ: str, output_dir: str, name: str,  initial_docs: bool = True):
    """ Uses the EMA number or otherwise the name of the medicinal product to search on
    https://www.ema.europa.eu/en/medicines for the EPAR of the particular product,
    but also the scientific discussion & procedural information PDFs

    Parameters
    ----------
    idx: The EMA number or product name
    typ: Indicator if EMA number of name is used, should be 'ema' or 'name'.
    output_dir: The location where to save the downloaded EPAR file
    name: the name to give the file

    Returns
    -------
    link: The URL to the online EPAR document location
    """
    if typ == 'ema':
        idx = "EMEA/H/C/" + idx.zfill(6)  # create the whole EMA number
    soup = scrape_website(f'https://www.ema.europa.eu/en/medicines?search_api_views_fulltext="{idx}"')

    # Try to find all links to EPAR pages in the search result, take the first one (most relevant)
    try:
        search_urls = soup.find_all(
            'a', attrs={'class': re.compile("ecl-link ecl-list-item__link")}
        )
        epar_url = ["https://ema.europa.eu" + hit['href'] for hit in search_urls if '/EPAR/' in hit['href']][0]

    except (IndexError, TypeError):
        logger.debug(f"Product not found in EMA search for: '{idx}'")
        return None

    # scrape EPAR website
    epar_soup = scrape_website(epar_url)

    # Only look at the 'Initial marketing-authorisation documents' part on the EPAR page
    initial_docs = epar_soup.find('div', attrs={'class': 'group-ema-med-init-mark-author field-group-html-element'})

    # If no initial market authorisation documents found, check all documents
    if not initial_docs:
        logger.info(f"'{idx}' has no initial marketing-authorisation documents")
        initial_docs = epar_soup

    docs = initial_docs.find_all('a', attrs={'class': 'ecl-link ecl-list-item__link'})
    docs = [doc['href'] for doc in docs if 'orphan' not in doc['href']]  # removes orphan reports

    # search the EPAR document & download:
    linka = [doc for doc in docs if 'report_en.pdf' in doc]
    if not linka:
        linka = [doc for doc in docs if "report_en-0.pdf" in doc]
    if not linka:
        linka = [doc for doc in docs if "report_.pdf" in doc]
    if not linka:
        linka = [doc for doc in docs if "public-assessment-report-withdrawn_en.pdf" in doc]
    if linka:
        if len(linka) > 1:
            logger.info(f"multiple docs found for '{idx}'")
        utils.download_files(url=linka[0], name=name + '.pdf', output_dir=output_dir)
        return linka[0]

    # search the scientific discussion & download
    linkb = [doc for doc in docs if "scientific-discussion_en.pdf" in doc]
    if not linkb:
        linkb = [doc for doc in docs if "scientific-discussion_.pdf" in doc]
    if not linkb:
        linkb = [doc for doc in docs if "scientific-discussion_en-0.pdf" in doc]
    if linkb:
        if len(linkb) > 1:
            logger.info(f"multiple docs found for '{idx}'")
        utils.download_files(url=linkb[0], name="s" + name + '.pdf', output_dir=output_dir)
        return linkb[0]

    # search the procedural information & download
    linkc = [doc for doc in docs if "steps-taken-authorisation_en.pdf" in doc]
    if not linkc:
        linkc = [doc for doc in docs if "steps-taken-authorisation_en-0.pdf" in doc]
    if not linkc:
        linkc = [doc for doc in docs if "steps-taken-authorisation_.pdf" in doc]
    if not linkc:
        logger.debug(f"No EPAR docs found for '{idx}'")
        return None
    else:
        if len(linkc) > 1:
            logger.info(f"multiple docs found for '{idx}'")
        utils.download_files(url=linkc[0], name="p" + name + '.pdf', output_dir=output_dir)
        return linkc[0]


def extract_ec_table():
    """ Run this function to extract the dataset from the EC Community register on
    https://ec.europa.eu/health/documents/community-register/

    Already mines the following variables:
    - EU Number
    - ID (based on EU number)
    - Company name
    - Product name
    - Decision (if refused)
    - inn (Active substance)
    Returns
    -------
    Dataframe containing mined vars
    """

    ec_df = pd.DataFrame(columns=utils.ec_colnames)  # create empty DF

    prod_types = ["ec_active", "ec_withdrawn", "ec_refused"]
    # iterate over product types (active, withdrawn or refused; each exists on different webpage)
    for t in prod_types:
        try:
            r = requests.get(utils.eurls[t][1])
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        # create a beatutifulsoup object to read the df
        soup = bs4.BeautifulSoup(r.text)
        df = pd.DataFrame(columns=utils.ec_colnames)

        # extract DF from html text
        listings = soup.findAll('script')
        data_id = "var dataSet = ["
        data = None

        # clean data
        for i, l in enumerate(listings):
            rawdata = str(l)
            if data_id in rawdata:
                r_idx = rawdata.rindex("]") + 1  # search for bracket closing the dataset
                l_idx = rawdata[::-1].rindex("[")  # search for bracket opening the dataset (rindex+reversed)
                l_idx = len(rawdata) - l_idx - 1  # correct for the reversal above
                rawdata = rawdata[l_idx:r_idx].replace("null", "None")  # select the dataset & replace null with None
                data = list(eval(rawdata))  # convert the raw text to a list of dictionaries
                break

        if data is None:  # if the dataset is not found raise Error
            raise ValueError(f"no dataset found which can be identified with '{data_id}'")

        # refusals have differently structured dicts
        if t != "ec_refused":  # thus active or withdrawn
            df["eunumber"] = [d["eu_num"]["display"] for d in data]
            df["eunumber_abb"] = [d["eu_num"]["id"] for d in data]
            df["name"] = [d["name"] for d in data]
            df["company"] = [d["company"] for d in data]

        else:  # refusals have differently structured dicts
            df["company"] = [d["company"] for d in data]  # Company name from EC ComReg website
            df["name"] = [d["name"]["display"] for d in data]
            df["eunumber_abb"] = [d["name"]["id"] for d in data]

        df["group"] = utils.eurls[t][0]  # this value will be overridden in extract_procedure_info
        df["url"] = utils.eurls[t][2] + df["eunumber_abb"].apply(str) + ".htm"
        ec_df = pd.concat([ec_df, df])

    return ec_df


def execute_var_pooling(ec_df: pd.DataFrame):
    """Using the result from the extract_ec_table() function, the DF is seperated
    accross the CPUs to pool the next step: searching the individual product webpages

    Parameters
    ----------
    ec_df: result of extract_ec_table() function

    Returns
    -------
    ec_df: the same as the input DF, but with vars mined from individual product webpages
    """
    pools = os.cpu_count() - 1  # check how many CPUs there are and use almost all of them
    logger.info(f"using {pools} CPUs")
    partial_dfs = np.array_split(ec_df, pools)  # split the DF based on the number of CPUs

    with ThreadPoolExecutor(max_workers=pools) as executor:
        df_generator = executor.map(pool_var_extraction, partial_dfs)  # appoint each pool to pool_var_extraction()
    df_list = list(df_generator)

    logger.info("joining Pooling results...")
    df_list = [x for x in df_list if x is not None]
    ec_df = pd.concat(df_list)  # merge the pooled dfs together again

    return ec_df


def pool_var_extraction(partial_df: pd.DataFrame):
    """Function to use with the multiprocessing Pool

    Parameters
    ----------
    partial_df: One of the split DFs

    Returns
    -------
    partial_df: The same split DFs, but with mined vars from extract_ema_data() function
    """
    partial_df.apply(lambda x: extract_ema_data(x) if 'url' in x.index and x.url is not None else None,
                     axis=1)
    return partial_df


def extract_ema_data(x: pd.Series):
    """ Requests the webpage from the EC, cleans the raw Beautifulsoup text and converts them to lists of dictionaries.
    Through the extract_data_var() function, the cleaned lists of dictionaries are searched on the variables.

    Parameters
    ----------
    x: Pandas series from the apply lambda function

    Returns
    -------
    x: Pandas Series with newly mined variables: mined in extract_data_var()
    """
    if 'url' not in x.index:
        raise ValueError(f"no 'url' column in DF: {x.index}")
    elif x.url is None:
        return x

    logger.debug(f"looking up'{x['name']}'")

    try:
        r = requests.get(x['url'], timeout=5)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.debug(e)
        return x

    soup = bs4.BeautifulSoup(r.text)

    listings = soup.findAll('script')

    # Find the first table with the product name, EU number, active substance etc.
    data_id = "var dataSet_product_information = ["
    data1 = None
    for i, l in enumerate(listings):
        rawdata = str(l)
        if data_id in rawdata:
            r_idx = rawdata.rindex("dataSet_proc") + 1  # there are two JSONs in this rawdata, only select first
            rawdata = rawdata[:r_idx]
            r_idx = rawdata.rindex("];")
            l_idx = rawdata[::-1].rindex("[")  # search for bracket opening the dataset (rindex+reversed)
            l_idx = len(rawdata) - l_idx - 1  # correct for the reversal above
            rawdata = rawdata[l_idx:r_idx + 1].replace("null", "None")  # select the dataset & replace null with None
            data1 = list(eval(rawdata))  # convert the raw text to a list of dictionaries
            break

    # Find the second table with the procedure information
    data_id = "var dataSet_proc = ["
    data2 = None
    for i, l in enumerate(listings):
        rawdata = str(l)
        if data_id in rawdata:
            l_idx = rawdata.rindex(data_id)
            rawdata = rawdata[l_idx:]
            r_idx = rawdata.rindex("];")
            l_idx = rawdata[::-1].rindex("[")  # search for bracket opening the dataset (rindex+reversed)
            l_idx = len(rawdata) - l_idx - 1  # correct for the reversal above
            rawdata = rawdata[l_idx - 1:r_idx + 1].replace("null",
                                                           "None")  # select the dataset & replace null with None
            data2 = list(eval(rawdata))  # convert the raw text to a list of dictionaries
            break

    if data1 is None:  # no product information found. Does the product even exist?
        logger.debug(x)
        logger.debug(soup)
        raise ValueError(f"no dataset found which can be identified")

    if data2 is None:  # product information is found, but seems to have no procedures.
        logger.debug(x)
        logger.debug(soup)
        x = extract_product_info(x, data1)
        return x

    x = extract_product_info(x, data1)
    x = extract_procedure_info(x, data2)

    return x


def extract_product_info(x: pd.Series, data1: list):
    """ Mines the individual product information on the EC website:

    - EMA link: the link to the EMA website of the corresponding product
    - ATC code & ATC name
    - Active substance: name of active substance

    Parameters
    ----------
    x: Pandas Series used by the apply lambda function (transposed columns through axis=1)
    data1: the cleaned dataset with information on the product

    Returns
    -------
    x: Pandas Series containing the newly mined variables
    """

    # EMA link
    ema_link = None
    # retrieve the product name to verify the right URL is taken
    product_name = [d['value'] for d in data1 if d['type'] == "name"][0]
    for i, d in enumerate(data1):
        if d["type"] == "ema_links":
            ema_link = [f["url"] for f in d["meta"] if product_name in f["description"]]  # retrieve correct URL
            ema_link = utils.try_block(ema_link, idx=0)
            break
        else:
            continue

    # Active substance
    act_sub = [d["value"] for d in data1 if d['type'] == "inn"][0]

    # ATC code & ATC name
    atccode, atcname = None, None

    # a few don't have ATC codes that go up to 3, take lower ones in that cases:
    for i, d in enumerate(data1):
        if data1[i]["type"] == "atc":
            # retrieve all levels and sort them from biggest to smallest
            levels = [f["level"] for f in d["meta"][0]]
            levels = sorted(levels)[::-1]

            for lvl in levels:
                if int(lvl) >= 3:  # take level 3 even if there are higher levels present
                    atccode, atcname = [
                        (f["code"], f["description"]) for f in d["meta"][0] if f["level"] == '3'
                    ][0]  # seems that meta has double brackets (redundent list in list)
                    break

                else:  # else take highest level (thanks to the reverse sorting), otherwise ATC is None
                    atc = utils.try_block([
                        (f["code"], f["description"]) for f in d["meta"][0] if f["level"] == lvl
                    ], idx=0)
                    if atc is not None:  # try_block returns None if out of index, else returns match (atc)
                        atccode, atcname = atc
                        break
                    else:
                        continue
            break
        # else continue the iteration to search for atc in data
        else:
            continue

    x["emalink"] = ema_link
    x["atccode"] = atccode
    x["atcname"] = atcname
    x["activesubstance"] = act_sub

    return x


def extract_procedure_info(x: pd.Series, data2: list, output_dir: str = "regsci_db/data/"):
    """ Mines the procedures on the individual product webpage:
    - EMA Number
    - Confidence level of EMA number (based on occurrence over all procedures)
    - Authorisation procedure: the procedure that is found representing authorisation
        could be a different procedure though
    - Authorisation date: the decision date related to the authorisation procedure
    - Authorisationdecurl: Authorisation decision URL
        Example: https://ec.europa.eu/health/documents/community-register/2004/200404287648/dec_7648_en.pdf
    - First procedure: the first procedure of the product

    Parameters
    ----------
    x: Pandas Series used by the apply lambda function (transposed columns through axis=1)
    data2: the cleaned dataset with information on the procedures
    output_dir: The path to the directory to save
        - the Authorisation Decisions (in output_dir/authorisation_decisions/
        - the SmPCs (in output_dir/smpcs/

    Returns
    -------

    """
    dates = []
    ema_numbers = []
    ema_numbers_abb = []

    data2 = [d for d in data2 if d['closed'] is not None]  # remove procedures without a closure date

    for i, d in enumerate(data2):
        # using closed instead of decision/date as does the EC (closed always has date, decision/date sometimes has None
        dates.append(d["closed"])  # d['decision']['date'])
        if d['ema_number'] is not None:  # catch all EMA numbers to later on extract number that occurs the most
            try:
                ema_numbers.append(d["ema_number"])
                ema_numbers_abb.append(re.match(r"EMEA\/H\/C\/(\d+)", d['ema_number'])[1].lstrip("0"))
            except TypeError:
                pass

    # Take most recent procedure and update status based on info from this procedure
    dates1 = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
    newest = max(dates1)  # find most recent
    oldest = min(dates1)  # find oldest, most likely the first occurence (not tested)
    newest_str = f'{newest:%Y-%m-%d}'  # convert date back to string to find it in the list 'dates' again
    oldest_str = f'{oldest:%Y-%m-%d}'
    idx_n = dates.index(newest_str)  # index only returns first occurence
    idx_o = dates.index(oldest_str)

    data2 = sorted(data2, key=lambda d: datetime.strptime(d['closed'], "%Y-%m-%d"))

    # Find oldest procedure, take only if type "Centralised - Authorisation"
    autprocedure = None
    if "Authorisation" in data2[idx_o]["type"]:
        autprocedure = data2[idx_o]["type"]
    # Sometimes the oldest procedure is not the authorisation procedure (decision to member states is),
    # therefore also look at the second oldest procedures
    else:
        for i in range(len(data2)):
            if i > 1:  # break after second procedure --> CONFIRM WITH LOURENS
                break
            elif "Authorisation" in data2[i]["type"]:
                autprocedure = data2[i]["type"]
                idx_o = i
                break
            # else no authorisation procedure found in first two (could be withdrawn or refused)

    # if no authorisation procedure found in first two procedures, check the rest
    # e.g. in case first refused, but later again accepted
    if autprocedure is None:
        if len([d for d in data2 if 'Authorisation' in d['type']]) > 0:
            idx_o, autprocedure = [(index, d) for (index, d) in enumerate(data2) if 'Authorisation' in d['type']][0]
        # if no authorisations found, there will only be a refusal procedure
        # or only withdrawal? --> https://ec.europa.eu/health/documents/community-register/html/ho25282.htm.
        elif len([d for d in data2 if 'Refusal' in d['type'] or 'Withdrawal' in d['type']]) > 0:
            try:
                idx_o, autprocedure = [
                    (index, d) for (index, d) in enumerate(data2) if 'Refusal' in d['type'] or 'Withdrawal' in d['type']
                ][0]
            except IndexError:
                raise IndexError(f"No Authorisation, nor Refusal, nor Withdrawal found for {x['url']}")

    if autprocedure is None:
        raise ValueError(f"No procedure found for {x['url']}. See {data2}")

    # decision date
    decision_date = data2[idx_o]['decision']['date']

    # procedure ID
    procedure_id = data2[idx_o]['id']

    # decision url, example: https://ec.europa.eu/health/documents/community-register/2004/200404287648/dec_7648_en.pdf
    if decision_date is not None:
        decision_date = decision_date.replace("-", "")  # date is 2006-12-25 and should be 20061225
        decision_url = \
            utils.eurls['ec_base'] + decision_date[
                              :4] + "/" + decision_date + procedure_id + "/dec_" + procedure_id + "_en.pdf"
        # smpc url, like decsion url but 'dec_' in URL -> 'anx_'
        smpc_url = decision_url.replace('/dec_', '/anx_')

    else:
        decision_url = None
        smpc_url = None

    # Find most recent procedure
    recentprocedure = data2[idx_n]["type"]

    # Product status taken from most recent procedure
    # (group: Active, Withdrawn, Refused --> Override value from extract_ec_table()
    if "Refusal" in data2[idx_n]['type']:
        group = "refused"
    elif "Withdrawal" in data2[idx_n]['type']:
        group = "withdrawn"
    else:
        group = "active"

    # Exceptional or conditional decision?
    procedures = [d['type'] for d in data2]
    excep = [x for x in procedures if "Annual reassessment" in x]
    cond = [x for x in procedures if "Annual renewal" in x]
    if len(excep) > 0:
        decision = "exceptional"
    elif len(cond) > 0:
        decision = "conditional"
    else:
        decision = None

    # EMA number: check the EMA number that occurs the most in the procedures:
    counter = [ema_numbers_abb.count(i) for i in ema_numbers_abb]
    max_count = max(counter)
    confidence = f"{max_count / len(counter) * 100}% ({len(counter)})"
    ema_idx = counter.index(max_count)
    ema_number = ema_numbers_abb[ema_idx]
    # ema_number = re.match(r"EMEA\/H\/C\/(\d+)", data2[idx_n]['ema_number'])[1].lstrip("0")

    # download and save the Authorisation Decisions and SmPC Annexes
    if decision_url is not None:
        utils.download_files(decision_url, f"{ema_number}.pdf", f"{output_dir}/authorisation_decisions/")
    if smpc_url is not None:
        utils.download_files(smpc_url, f"{ema_number}.pdf", f"{output_dir}/smpcs/")

    x["emanumber"] = "EMEA/H/C/" + f"{ema_number}"
    x['emanumber_abb'] = ema_number
    x["emanumber_confidence"] = confidence
    x['authorisationdate'] = decision_date
    x['authorisationprocedure'] = autprocedure
    x["auth_url"] = decision_url
    x['smpc_url'] = smpc_url
    x["recentprocedure"] = recentprocedure
    x['group'] = group
    x['decision_type (EC)'] = decision

    return x


def ema_doublecheck(ec_df: pd.DataFrame):
    """ Takes the Excel file from the EMA website and compares it to the database of the EC Community Register.
    1. Merges both DFs on EMA numbers and Product names (outer merge)
    2. Checks for product names that occur multiple times in the merged DF (indicating different EMA number):
        a. If authorisation date most recent procedure, only keep that hit (remove others)
        b. Elif authorisation procedure occuring, but not most recent procedure: keep all and check manually why newer
            procedures have other EMA number
        c. Else no authorisation procedure at all: keep all and check manually what is happening

    Parameters
    ----------
    ec_df: Database of EU community register from execute_pooling(extract_ec_table())

    Returns
    -------
    Returns the merged DF without the duplicate product names (the ones that should be manually checked are in debug.log
    """
    # extract excel file from website, first 0:7 rows from first sheet contain irrelevant information
    ema_df = pd.read_excel(
        "https://www.ema.europa.eu/sites/default/files/Medicines_output_european_public_assessment_reports.xlsx",
        sheet_name=0, header=8
    )
    ema_df = ema_df.loc[ema_df.Category == "Human"]  # only select Human medicines
    ema_df["emanumber_abb"] = ema_df["Product number"].apply(
        lambda x: re.match(r"EMEA\/H\/C\/(\d+)", x)[1].lstrip("0") if x is not None else None)  # strip EMA numbers

    # remove specifc product information in brackets and only keep general part of product name
    # also lower the name for comparison, remove tailing & leading spaces & remove spaces around slashes
    ema_df["lname"] = ema_df["Medicine name"].apply(
        lambda x: re.sub(r"\s*\/\s*", "/", re.sub(r"\(.*", "", x)).lower().strip().replace(".", "")
    )
    ec_df["lname"] = ec_df["name"]\
        .str.lower()\
        .str.strip()\
        .str.replace(r"\(.*", "")\
        .str.replace(r"\s*\/\s*", "/")\
        .str.replace(".", "", regex=False)  # remove dots in name for things like B.V. or ltd.

    # merge first on EMA number & product name
    ec_df = pd.merge(ec_df, ema_df, on=["emanumber_abb", "lname"], how="outer")
    ec_df["emanumber_doublecheck"] = "Succeeded"  # give default value (will be overwritten later on)
    logger.info(ec_df["Decision date"].dtypes)
    # create unrealistic date to replace with NaT values (missing dates):
    unreal_date = pd.to_datetime("1900-01-01")
    ec_df['Decision date'] = ec_df["Decision date"].fillna(unreal_date)
    logger.info("changed")
    logger.info(ec_df["Decision date"].dtypes)
    # get the ones with the double product names, but different EMA numbers:
    double_names = ec_df.loc[ec_df.duplicated(["lname"], keep=False)]
    double_names.to_csv("./log/double_names.csv", sep=";")
    logger.info(f"{len(double_names.lname.unique())} products will be extra checked due to multiple occurences..")

    checknames = list(double_names.lname.unique())
    # group on names and then check per product name what's happening
    keep_names = double_names.groupby("lname")

    for g in keep_names:
        df = g[1].sort_values(by="Decision date", ascending=False)  # sort g[1] on Decision dates

        # if authorisation is most recent, only take that one
        if df.iloc[0]["Authorisation status"] == "Authorised":
            to_remove = ec_df.loc[  # remove hits using the following filters:
                (ec_df.lname == g[0]) &  # loc on the product name
                ~(ec_df["Decision date"] == df.iloc[0]["Decision date"])  # skip where decision date differs
                ]

        # elif authorisation found, but not most recent:
        # keep both in database to manually search why it got a new EMA number
        elif "Authorised" in df["Authorisation status"].values:
            logger.debug(f"MANUALLY CHECK '{g[0]}' IN EC COMMUNITY REGISTER (authorisation not most recent")
            to_remove = ec_df.loc[  # remove hits using the following filters:
                ((ec_df.lname == g[0]) &  # loc on the product name
                 ~(ec_df["Decision date"] == df.iloc[0]["Decision date"])) |  # skip where decision date differs
                # OR
                ((ec_df.lname == g[0]) &  # loc on the product name
                 ~(ec_df["Authorisation status"] == "Authorised"))  # skip where the status is not 'authorised'
                ]

        # else no authorisation found: keep all in db
        else:
            logger.debug(f"MANUALLY CHECK '{g[0]}' IN EC COMMUNITY REGISTER (no authorisation)")
            to_remove = pd.DataFrame(columns=ec_df.columns)  # empty DF, nothing to remove

        # substract the to_remove hits from the EC df
        ec_df = ec_df[~ec_df["emanumber_abb"].isin(to_remove["emanumber_abb"])]

    # replace the value in the emalink col with the URL col from the ema_df if not empty
    ec_df["emalink"] = ec_df.apply(lambda x: x['URL'] if utils.isnan(x['URL']) else x['emalink'], axis=1)

    # remove unnecessary cols
    rmcols = [x for x in list(ema_df.columns) if x not in ["lname", "emanumber_abb"]]
    ec_df = ec_df.drop(labels=rmcols, axis=1)

    # override "succeeded" for names that were tested
    ec_df.loc[ec_df['lname'].isin(checknames), "emanumber_doublecheck"] = "Passed test"
    # override "passed test" for names that failed
    ec_df.loc[ec_df['lname'].duplicated(keep=False), "emanumber_doublecheck"] = "Failed test"

    return ec_df
