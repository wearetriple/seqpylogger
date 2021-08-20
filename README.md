# SeqPyLogger

[![PyPI version](https://img.shields.io/pypi/v/seqpylogger)](https://pypi.org/project/seqpylogger/)

SeqPyLogger is a python loghandler for [seq](https://datalust.co/seq).

## Usage

```python
import os

os.environ["SEQ_APIKEY"] = "xSxExQxAxPxIxKxExYx"
os.environ["SEQ_SERVER"] = "http://localhost:8794/"
os.environ["Environment"] = "Staging"

import logging
from seqpylogger import SeqPyLogger

root = logging.getLogger()
root.setLevel(logging.INFO)
seqLogger = SeqPyLogger(buffer_capacity=10)
root.addHandler(seqLogger)

logger = logging.getLogger("MyLogger")

logger.debug("Debug log message")
logger.info("Informational log message")
logger.warning("Warning log message")
logger.error("Error log message")
logger.critical("Critical log message")
logger.fatal("Critical log message")

logger.info("Test log message with argument %s", "dummy argument")
logger.info("Test log message with arguments %s, %s", "dummy argument 1", "dummy argument 2")

try:
    raise Exception("Some issue")
except:
    logging.exception("An error occured but now we have the stacktrace")
    # logging.error("There was an error", exc_info=1)  # alternative to .exception()

# logs are flushed every 10 seconds and every 10 logs
```

An alternative way of setting the handler is using the dictConfig

```python
import os
import time
import logging
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
```

## Installation

```bash
pip install seqpylogger
```

## Test install

Used for development on the package.

```bash
sudo python3 -m pip install -U .
```

## Examples

```python
try:
    raise Exception("Some issue")
except:
    logging.exception("An error occured but now we have the stacktrace")
    # logging.error("There was an error", exc_info=1)  # alternative to .exception()

try:
    raise Exception("Some issue")
except:
    logging.fatal("This time no stacktrace")

try:
    raise Exception("Some issue")
except:
    logging.fatal("Stacktrace is not limited to ERROR", exc_info=1)
```

## Images

![Screenshot image](https://github.com/wearetriple/seqpylogger/raw/master/assets/screenshot.png)

# Changelog

inspired by [Keep a changelog](https://keepachangelog.com/en/1.0.0/)

## [2021-08-20]
- [Fixed] Version file removed as this broke pip installation
- ~~[Fixed] Missing .version file in MANIFEST.md broke pip installation~~

## [2021-08-13]
- [Fixed] Replaced badge.fury.io pypi badge with shields.io
- [Changed] Added tagging in create_release.sh
- [Changed] Used `atexit` to register flush on exit
- [Fixed] Fixed issue of duplicate logs when doing a manualflush

## [2021-03-22]
- [Fixed] Update dependencies in Pipfile.lock

## [2020-12-29]
- [Fixed] old dependencies for development

## [2020-07-17]
- [Fixed] .msg and arg objects always converted to str
- [Changed] internal logs nolonger use root logger

## [2020-05-13]
- [Fixed] Removed print line when adding seq url without trailing slash
- [Changed] README example to fully work if copied
- [Added] changelog to README

## [Unreleased]
- String formatting only works for `%s` not for `%d`, the argument is stil available but the message misses the value 
- Environment variable only works using `Environment` while full uppercase is the best practice for environment variables