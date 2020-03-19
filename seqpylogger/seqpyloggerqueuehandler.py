from logging.handlers import QueueHandler


class SeqPyLoggerQueueHandler(QueueHandler):
    def __init__(self, queue):
        super().__init__(queue)
    
    def prepare(self, record):
        return record
