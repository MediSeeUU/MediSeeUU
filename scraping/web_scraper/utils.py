import logging


# This method makes use of Decorators.
# Read up on what this entails here:
# https://docs.python.org/3/glossary.html#term-decorator
# https://realpython.com/primer-on-python-decorators/
def exception_retry(func: callable, max_attempts: int = 4, logging_instance: logging.getLoggerClass() = None):
    """
    Decorator function to make a function parallelized. The function will have the code retry if it throws an exception.

    Args:
        func: the function that will be retried when an exception is thrown
        max_attempts: The amount of times a function can be retried. The default value is 4.
        logging_instance: If errors need to be reported, the logging instance from the caller can be attached

    Returns: The result of func. Returns None when the function did not return after the maximum attempts.

    """
    def wrapper(*args, **kwargs):
        exception_names: list[str] = []
        if func is None:
            return None

        for _ in range(max_attempts):
            try:
                return func(*args, **kwargs)

            except Exception as e:
                exception_names.append(type(e).__name__)
                if logging_instance is not None:
                    logging_instance.debug(f"Function {func.__name__} failed with {type(e).__name__}")
                continue

        if logging_instance is not None:
            logging_instance.warning(f"Retry failed after {max_attempts} attempts. {count_unique(exception_names)} "
                                     f"{func.__name__}({', '.join(map(str, args))}) ")
        return None  # Func threw an exception, return None

    return wrapper


def count_unique(input_list: list):
    return dict(
        zip(list(input_list), [list(input_list).count(i) for i in list(input_list)])
    )
