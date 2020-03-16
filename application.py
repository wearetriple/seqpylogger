import logging
import time
import dotenv
from seqpylogger import SeqPyLogger

dotenv.load_dotenv()

root = logging.getLogger()
log_handler = SeqPyLogger.createQueueHandler(buffer_capacity=1)
root.addHandler(log_handler)

# for i in range(15):
#     logging.warning("Test warning")
#     time.sleep(0.1)

# root = logging.getLogger()
# root.addHandler(SeqPyLogger.createBufferHandler())

try:
    logging.warning("Trying")
    raise Exception("It works")
except Exception as e:
    logging.error("There was an error", exc_info=1)

logging.warning("Nice {work}", "work")
# logging.warning("Nice {thing}", thing="verse")

# for i in range(15):
#     logging.warning("Test warning")
#     time.sleep(0.1)

time.sleep(1)