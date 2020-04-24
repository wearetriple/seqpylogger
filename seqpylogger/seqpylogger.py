"""
Main module for referencing handler
"""

import time
import queue
import threading
from logging import getLogger, NullHandler, LogRecord
from logging.handlers import QueueHandler
from .seqpyloggerhandler import SeqPyLoggerHandler
from .seqpyloggerqueuelistener import SeqPyLoggerQueueListener
from .utils import set_interval
from . import config


LOG = getLogger(config.LOGGER_NAME)
LOG.addHandler(NullHandler())
LOCK = threading.Lock()


class SeqPyLogger(QueueHandler):
    """"LogHandler for seq"""

    def __init__(self, buffer_capacity: int = 10):
        self.log_queue: queue.Queue = queue.Queue(-1)
        self.log_handler = SeqPyLoggerHandler(capacity=buffer_capacity)

        queue_listener = SeqPyLoggerQueueListener(self.log_queue, self.log_handler)

        queue_listener.start()

        self.timout_flush()

        super().__init__(self.log_queue)

    def manual_flush(self, wait: int = 0):
        """flushes buffer

        Parameters
        ----------
        wait : int, optional
            seconds to wait if wait > 0, by default 0
        """
        with LOCK:
            self.log_handler.flush()
        if wait > 0:
            time.sleep(wait)

    def prepare(self, record: LogRecord) -> LogRecord:
        """Pass trough for LogRecord

        Parameters
        ----------
        record : LogRecord

        Returns
        -------
        LogRecord
        """
        return record

    @set_interval(10)
    def timout_flush(self):
        """Runs flush every 10 seconds
        """
        self.manual_flush()
