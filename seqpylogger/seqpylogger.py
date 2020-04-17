import functools
import time
import queue
import threading
from logging import Handler
from logging.handlers import QueueHandler
from .seqpyloggerhandler import SeqPyLoggerHandler
from .seqpyloggerqueuelistener import SeqPyLoggerQueueListener
from .utils import setInterval

lock = threading.Lock()


class SeqPyLogger(QueueHandler):
    def __init__(self, buffer_capacity=10):
        self.log_queue = queue.Queue(-1)
        self.log_handler = SeqPyLoggerHandler(capacity=buffer_capacity)

        queue_listener = SeqPyLoggerQueueListener(self.log_queue, self.log_handler)

        queue_listener.start()

        self.timout_flush()

        super().__init__(self.log_queue)

    def manual_flush(self, wait=0):
        with lock:
            self.flush()
            self.log_handler.flush()
        if wait > 0:
            time.sleep(wait)

    def prepare(self, record):
        return record

    @setInterval(10)
    def timout_flush(self):
        self.manual_flush()
