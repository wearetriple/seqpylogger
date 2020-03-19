import time
import queue
from .seqpyloggerhandler import SeqPyLoggerHandler
from .seqpyloggerqueuehandler import SeqPyLoggerQueueHandler
from .seqpyloggerqueuelistener import SeqPyLoggerQueueListener

class SeqPyLogger:
    def __init__(self):
        self.log_handler = None

    def get_handler(self, buffer_capacity=10):
        """get_handler
        
        Returns
        -------
        SeqPyLoggerQueueHandler
            Handler for sending LogRecords to Seq
        """
        queue_handler = SeqPyLoggerQueueHandler(queue.Queue(-1))

        self.log_handler = SeqPyLoggerHandler(capacity=buffer_capacity)
        
        queue_listener = SeqPyLoggerQueueListener(queue_handler.queue, self.log_handler)
        
        queue_listener.start()
        
        return queue_handler

    def flush(self, wait=0):
        self.log_handler.flush()
        if wait > 0:
            time.sleep(wait)