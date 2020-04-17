from logging.handlers import QueueListener


class SeqPyLoggerQueueListener(QueueListener):
    def __init__(self, queue, handler):
        super().__init__(queue, handler)

    def prepare(self, record):
        return record
