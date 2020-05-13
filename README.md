# SeqPyLogger

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

# logs are flushed every 10 seconds

# Run manual flush with wait to prevent last messages not sending when program ends
seqLogger.manual_flush(wait=5)
```

## Test install

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

## Changelog

[2020-05-13]
- [Fixed] Removed print line when adding seq url without trailing slash
- [Changed] README example to fully work as if copied
- [Added] changelog to README