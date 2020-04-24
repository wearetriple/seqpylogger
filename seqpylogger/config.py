"""config file for project"""

import os


def raise_missing(msg: str):
    """Raises Exception if environment variable is missing

    Parameters
    ----------
    msg : str
        Message saying whats missing

    Raises
    ------
    KeyError
        Exception with msg
    """
    raise KeyError(msg)


SEQ_SERVER = os.getenv("SEQ_SERVER") or raise_missing(
    "Missing SEQ_SERVER environment variable"
)
SEQ_APIKEY = os.getenv("SEQ_APIKEY") or raise_missing(
    "Missing SEQ_APIKEY environment variable"
)
ENVIRONMENT = os.getenv("Environment", "NOT-SET")
LOGGER_NAME = "seqpylogger"
