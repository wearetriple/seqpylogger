"""
A QueueListener that does nothing to the logrecord
and passes it to its handler
"""

import logging
from queue import Queue
from logging.handlers import QueueListener


class SeqPyLoggerQueueListener(QueueListener):
    """
    A QueueListener that does nothing to the logrecord
    and passes it to its handler
    """

    def __init__(self, queue: Queue, handler: logging.Handler):
        super().__init__(queue, handler)

    def prepare(self, record: logging.LogRecord) -> logging.LogRecord:
        """Pass trough for LogRecord

        Parameters
        ----------
        record : LogRecord

        Returns
        -------
        LogRecord
        """
        return record
