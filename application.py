import logging
import time
from seqpylogger import SeqPyLogger

root = logging.getLogger()
root.addHandler(SeqPyLogger.createQueueHandler())

# for i in range(15):
#     logging.warning("Test warning")
#     time.sleep(0.1)

try:
    logging.warning("Trying")
    raise Exception("It works")
except Exception as e:
    logging.error(e)
    print(e)