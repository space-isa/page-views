import logging
import sys


def exception_handler(function):
    """
    Wrap the function passed in, and log exceptions if they occur.
    PARAMETERS
    ----------
    function : object
        A user-defined function.
    RETURNS
    -------
    wrapper : object
        If an exception occurs, display a log with a traceback
        of the error.
    """
    def wrapper(*args, **kwargs):
        try:
            #  Call the function
            return function(*args, **kwargs)

        except FileNotFoundError as error:
            #  Print exception and exit code
            print("File not found. {}".format(error))

        except Exception as error:
            #  Log exception traceback and exit code
            logging.exception(error)
            print("Code failed. See traceback log for details.")
            sys.exit(1)

    return wrapper