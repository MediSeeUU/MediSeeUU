# This method makes use of Decorators.
# Read up on what this entails here:
# https://docs.python.org/3/glossary.html#term-decorator
# https://realpython.com/primer-on-python-decorators/
def exception_retry(func, max_attempts: int = 4) -> bool:
    """ Abstract function that retries a function a maximum of four times if it throws an exception

    Args:
        func: Function to retry
        max_attempts (int, optional): Maximum number of attempts that the function is called. Defaults to 4.

    Returns:
        bool: Function passed without exception, return true. Function threw an exception, return false
    """
    def wrapper(*args, **kwargs):
        for _ in range(max_attempts):
            try:
                func(*args, **kwargs)
            except Exception:
                continue
            else:
                return True  # Func passed without exception, return true
        return False         # Func threw an exception, return false

    return wrapper()
