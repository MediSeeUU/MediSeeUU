import logging
import requests
from scraping.utilities.web import json_helper


# This method makes use of Decorators.
# Read up on what this entails here:
# https://docs.python.org/3/glossary.html#term-decorator
# https://realpython.com/primer-on-python-decorators/
def exception_retry(max_attempts: int = 4, logging_instance: logging.getLoggerClass() = None):
    """
    Decorator function to make a function parallelized. The function will have the code retry if it throws an exception.

    Args:
        max_attempts: The amount of times a function can be retried. The default value is 4.
        logging_instance: If errors need to be reported, the logging instance from the caller can be attached

    Returns: The result of func. Returns None when the function did not return after the maximum attempts.
    """
    # Decorators are a little tricky. if you want to pass arguments to a function with the @exception_retry notation,
    # You need to split the decorator into two functions. The first function catches the arguments, and returns a
    # function. The second calls the first function with the argument of the function that has to be retried.
    # A bit messy, but it is what it is with Python.
    def decorator(func: callable):
        def wrapper(*args, **kwargs):
            exception_names: list[str] = []
            if func is None:
                return None

            for _ in range(max_attempts):
                try:
                    return func(*args, **kwargs)

                except (OSError, requests.HTTPError) as e:
                    exception_names.append(type(e).__name__)
                    if logging_instance is not None:
                        logging_instance.debug(f"Function {func.__name__} failed with {type(e).__name__}")
                    continue

                # TODO: remove eventually. Left here to make running code easy while allowing easier debugging
                except Exception as e:
                    if logging_instance is not None:
                        logging_instance.error(f"TODO: {func.__name__}({', '.join(map(str, args))}) "
                                               f"failed... {e}")
                    return None

            if logging_instance is not None:
                logging_instance.warning(f"Retry failed after {max_attempts} attempts. {count_unique(exception_names)} "
                                         f"{func.__name__}({', '.join(map(str, args))}) ")
            return None

        return wrapper

    return decorator


def count_unique(input_list: list):
    return dict(
        zip(list(input_list), [list(input_list).count(i) for i in list(input_list)])
    )


def get_html_object(url: str) -> requests.Response:
    """ Fetches the html from a website.

    Args:
        url (str): The link to the page where the html is needed from.

    Returns:
        requests.Response: Returns a Response object that contains the response to the HTTP request.
    """
    html_active: requests.Response = requests.get(url)

    # If a http error occurred, throw error
    html_active.raise_for_status()

    return html_active


def init_ema_dict(eu_n: str, file: json_helper.JsonHelper):
    """
    Set default empty values for if website does not exist

    Args:
        eu_n (str): eu_number of medicine
        file (json_helper.JsonHelper): Dictionary that is being initialized
    """
    ema_urls: dict[str, str | list[list[str]]] = {
        "epar_url": "",
        "omar_url": "",
        "odwar_url": "",
        "other_ema_urls": []
    }
    pdf_url: dict[str, dict] = {
        eu_n: ema_urls
    }
    file.add_to_dict(pdf_url)
