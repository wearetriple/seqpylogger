"""
This class does not really assert anything but it just runs the basic functionalities of the package.
"""

import logging
import pytest

@pytest.fixture
def logger():
    from seqpylogger import SeqPyLogger

    root = logging.getLogger()
    seqLogger = SeqPyLogger()
    root.addHandler(seqLogger)
    logger = logging.getLogger('test_application')
    logger.setLevel(logging.INFO)
    return logger


def test_log_messages(logger: logging.Logger):
    logger.debug("Debug log message")
    logger.info("Informational log message")
    logger.warning("Warning log message")
    logger.error("Error log message")
    logger.critical("Critical log message")
    logger.fatal("Critical log message")

    logger.info("Test log message with argument %s", "dummy argument")
    logger.info("Test log message with arguments %s, %s", "dummy argument 1", "dummy argument 2")
    
    # This does still not log correctly
    logger.info("Test log message with arguments double decimal %d, %d", 123, 321)


def test_log_exception(logger: logging.Logger):
    try:
        raise Exception("Some issue")
    except:
        logger.exception("An error occured but now we have the stacktrace")
        # logging.error("There was an error", exc_info=1)  # alternative to .exception()

    try:
        raise Exception("Some issue")
    except:
        logger.fatal("This time no stacktrace")

    try:
        raise Exception("Some issue")
    except:
        logger.fatal("Stacktrace is not limited to ERROR", exc_info=1)

def test_log_invalid_log_format(logger: logging.Logger):
    with pytest.raises(TypeError):
        logger.info("A wrong formated message {test}", "Arg0")

def test_setup_dict_config():
    import os
    import logging.config

    os.environ["SEQ_APIKEY"] = "xSxExQxAxPxIxKxExYx"
    os.environ["SEQ_SERVER"] = "http://localhost:8794/"
    os.environ["Environment"] = "Staging"

    logger_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "root": {
            "level": logging.INFO,
            "handlers": ["seq"]
        },
        "handlers": {
            "seq": {
                "level": logging.INFO,
                "class": "seqpylogger.SeqPyLogger"
            },
        },
    }

    logging.config.dictConfig(logger_config)

    logging.info("Example message")