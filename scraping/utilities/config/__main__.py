import json
import os
from pathlib import Path


# File located at
#   (MediSee)/scraping/utilities/config.py
# We need to climb three folder
root_path: Path = Path(__file__).resolve().parent.parent.parent

scraping_path: Path = root_path / "scraping"
data_path: Path = root_path / "data"
logging_path: Path = root_path / "logs"

filename = "scraping_config.txt"

parallelized = "parallelized"
run_web = 'run_web'
run_xml = 'run_xml'
run_pdf = 'run_pdf'
run_annex_10 = 'run_annex_10'
run_combiner = 'run_combiner'
run_transformer = 'run_transformer'
run_db_com =  'run_db_communicator'
xml_convert_all = 'xml_convert_all'
pdf_parse_all = 'pdf_parse_all'
db_com_send_together = 'db_com_send_together'

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
    xml_convert_all: False,
    pdf_parse_all: False,
    db_com_send_together: True
}

def load_config():
    """
    loads config file, if file does not exist, creates file with default values.

    Returns:
    dict[bool]: dictionary containing bools to indicate on/off

    """

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    else:
        with open(filename, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
