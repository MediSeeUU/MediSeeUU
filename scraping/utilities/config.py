from pathlib import Path


# File located at
#   (MediSee)/scraping/utilities/config.py
# We need to climb three folder
root_path: Path = Path(__file__).resolve().parent.parent.parent

scraping_path: Path = root_path / "scraping"
data_path: Path = root_path / "data"
logging_path: Path = root_path / "logs"

# TODO: Make decisions about architecture.
#       Possibilities are to
#       1. Load one global dict, and define variables in the code that other modules use
#       2. Load one global dict, and give this to the other modules
#       3. Load one global dict, split to smaller dicts and pass them to specified modules
"""
web_config = {
    "scrape_ec": False,
    "scrape_ema": False,
    "download": False,
    "download_refused": False,
    "download_annex10": False,
    "download_ema_excel": False,
    "filter": False,

    "parallelized": False
}
"""
