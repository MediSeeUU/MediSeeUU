import logging


default_path_logging: str = "./logs"
default_path_data: str = "./data"

logging_level: int = logging.INFO


class WebConfig:
    # Tasks
    # Do not change values in this file to affect behaviour! Use the methods supplied
    run_scrape_ec: bool = False
    run_scrape_ema: bool = False
    run_download: bool = False
    run_download_refused: bool = False
    run_download_annex10: bool = False
    run_filter: bool = False

    # Arguments for tasks
    parallelized: bool = False
    medicine_list: (list[(str, str, int, str)] | None) = None

    # Paths
    path_logging = default_path_logging
    path_data = default_path_data

    def __init__(self):
        """
        The initialization of this class should be handled by `run_all` or `run_custom`.
        This method is here because adjusting the values of `web_default_path_...`
        does not adjust the values in the class
        """
        self.path_logging = default_path_logging
        self.path_data = default_path_data

    def run_all(self):
        """
        Sets all tasks to run to true. This is the safest way to run the program.

        Returns: Modified Config class

        """
        self.run_scrape_ec = True
        self.run_scrape_ema = True
        self.run_download = True
        self.run_download_refused = True
        self.run_download_annex10 = True
        self.run_filter = True
        return self

    def run_custom(self,
                   scrape_ec: bool = False,
                   scrape_ema: bool = False,
                   download: bool = False,
                   download_refused: bool = False,
                   download_annex10: bool = False,
                   filtering: bool = False):
        """
        Method to set up a config class with the desired functions to run.
        By default, no functions will execute. We recommend enabling specific elements using `kwargs`
        So for example, run the function as `run_custom(scrape_ec=True)` for extra clarity.

        Args:
            scrape_ec:
                Scrape the list of all medicines from the EC, and all individual medicine pages
            scrape_ema:
                Scrape the individual medicine pages from the EMA. This has no effect when scrape_ec has not been run
            download:
                Download all the saved links. This has no effect when one of the previous tasks has not been run.
            download_refused:
                Refused files are an edge case, and can slow us down. They are not parsed by the PDF module.
            download_annex10:
                Annex10 is
            filtering:
                Retry failed downloads. This has no effect is download has not been run.

        Returns: Modified config class

        """
        self.run_scrape_ec = scrape_ec
        self.run_scrape_ema = scrape_ema
        self.run_download = download
        self.run_download_refused = download_refused
        self.run_download_annex10 = download_annex10
        self.run_filter = filtering
        return self

    def set_parallel(self, enabled: bool = True):
        """
        Sets the parallelized flag to true. Simply here to allow Config class oneliners.

        Returns: Modified Config class

        """
        self.parallelized = enabled
        return self

    def supply_medicine_list(self, medicine_list: list[(str, str, int, str)]):
        """
        Instead of having the code gather all medicines from the EC website itself,
        we can supply a list of medicines for the code to use.
        Comes in handy if you want to test a smaller set of medicines.

        Args:
            medicine_list: A list of medicines, structured as `{url, eu_num_full, medicine_type, eu_num_short}`

        Returns: Modified Config class

        """
        self.medicine_list = medicine_list
        return self
