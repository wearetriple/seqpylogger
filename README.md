# SeqPyLogger

## Usage

```
import os
import logging
from seqpylogger import SeqPyLogger

os.environ["SEQ_APIKEY"] = "xSxExQxAxPxIxKxExYx"
os.environ["SEQ_SERVER"] = "http://localhost:8794/"

root = logging.getLogger()
seqLogger = SeqPyLogger()
root.addHandler(seqLogger.get_handler())

logging.warning("User {Username} not found", "Unknown-User-1")

# Run manual flush with wait to prevent last messages not sending
seqLogger.flush(wait=5)
```

## Test install

```
sudo python3 -m pip install -U .
```
