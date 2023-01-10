import json
import os
from pathlib import Path


# File located at
#   (MediSee)/scraping/utilities/config.py
# We need to climb three folder
root_path: Path = Path(__file__).resolve().parent.parent.parent.parent

scraping_path: Path = root_path / "scraping"
data_path: Path = root_path / "data"
logging_path: Path = root_path / "logs"

filename = "scraping_config.txt"
log = logging.getLogger("config")

parallelized = "parallelized"
run_web = 'run_web'
run_xml = 'run_xml'
run_pdf = 'run_pdf'
run_annex_10 = 'run_annex_10'
run_combiner = 'run_combiner'
run_transformer = 'run_transformer'
run_db_com = 'run_db_communicator'
run_annex_comparer = "run_annex_comparer"
xml_convert_all = 'xml_convert_all'
pdf_parse_all = 'pdf_parse_all'
db_com_send_together = 'db_com_send_together'
web_config = 'web_config'
web_scrape_ec = 'web_scrape_ec'
web_scrape_ema = 'web_scrape_ema'
web_download = 'web_download'
web_download_refused = 'web_download_refused'
web_download_annex10 = 'web_download_annex10'
web_download_ema_excel = 'web_download_ema_excel'
web_run_filter = 'web_run_filter'


# if no config found, use default values
default_config = {
    parallelized: True,
    run_web: True,
    run_xml: True,
    run_pdf: True,
    run_annex_10: True,
    run_combiner: True,
    run_transformer: True,
    run_db_com: True,
    run_annex_comparer: True,
    xml_convert_all: False,
    pdf_parse_all: False,
    db_com_send_together: True,
    web_config: [
        {
            web_scrape_ec: True,
            web_scrape_ema: True,
            web_download: True,
            web_download_refused: True,
            web_download_annex10: True,
            web_download_ema_excel: True,
            web_run_filter: True
        }
    ]
}


def load_config():
    """
    loads config file, if file does not exist, creates file with default values.

    Returns:
    dict[bool]: dictionary containing bools to indicate on/off

    """
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            log.warning("Config file has incorrect syntax, using default configuration instead")
    else:
        with open(filename, 'w') as f:
            json.dump(default_config, f, indent=4)
    return default_config
