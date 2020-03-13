"""
This module returns a Handler

inside the module the follwing happens
Handler is a queueHandler and can add LogRecords to a queue
Next a queueListener(handler)
Gets items from this queue and passes them to a memory handler (with a 10 item capacity)
After capacity the memoryHandler passes its batch to a custom http sender, for seq
"""

import datetime
import json
import logging
import queue
import threading
import traceback
import time
import uuid
from logging.handlers import QueueListener, QueueHandler, BufferingHandler

import requests

class SeqPyLogger:
    def __init__(self):
        pass

    @staticmethod
    def createQueueHandler():
        """createHandler
        
        Returns
        -------
        QueueHandler
            Handler for sending LogRecords to Seq
        """
        queue_handler = QueueHandler(queue.Queue(-1))

        handler = SeqPyLogger.createBufferHandler()
        listener = QueueListener(queue_handler.queue, handler)
        
        listener.start()
        
        return queue_handler

    @staticmethod
    def createBufferHandler():
        logger = SeqPyLoggerHandler(10)
        formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
        logger.setFormatter(formatter)
        return logger
    
class SeqPyLoggerHandler(BufferingHandler):
    def __init__(self, capacity=10):
        super().__init__(capacity=10)
    
    def flush(self):
        # for record in self.buffer:
        #     print(self.format(record))
        self.send_to_seq()
        return super().flush()
    
    def send_to_seq(self):
        batch_objects = []
        for record in self.buffer:
            # print(dir(record))
            record_object = {
                "@t": datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"),
                "@m": record.message,
                # "@mt": "",
                "@l": record.levelname,
                #"@x": record.exception,
                "@i": uuid.uuid4().hex
            }
            ex = self.add_exception(record)
            if ex is not None:
                record_object.update({"@e": ex})
            batch_objects.append(json.dumps(record_object, separators=(',', ':')))
        message_body = str.join("\n", batch_objects)
        print(message_body)
        headers = {
            "X-Seq-ApiKey": os.getenv("SEQ_APIKEY"),
            "Content-type": "application/vnd.serilog.clef"
        }
        resonse = requests.post(f"{os.getenv('SEQ_SERVER')}api/events/raw", data=message_body, headers=headers)
        print(resonse.status_code)
        print(resonse.text)
    
    def add_exception(self, record):
        if record.exc_info and any(record.exc_info) and record.levelno == logging.ERROR:
            return str.join('', traceback.format_exception(*record.exc_info))
        else:
            return None




def init():
    # queue_handler = SeqPyLogHandler()
    # handler = logging.StreamHandler()
    # listener = QueueListener(queue_handler.queue, handler)
    # root = logging.getLogger()
    # formatter = logging.Formatter('%(threadName)s: %(message)s')
    # handler.setFormatter(formatter)
    # root.addHandler(queue_handler)
    # listener.start()
    # The log output will display the thread which generated
    # the event (the main thread) rather than the internal
    # thread which monitors the internal queue. This is what
    # you want to happen.

    root.warning('Look out!')
    listener.stop()


        # handler = logging.StreamHandler()
        # formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
        # handler.setFormatter(formatter)\
# def callback():
#     queue_handler = SeqPyLogHandler()
    
#     handler = logging.StreamHandler()
#     formatter = logging.Formatter('%(threadName)s: %(message)s')
#     handler.setFormatter(formatter)
    
#     listener = QueueListener(queue_handler.queue, handler)
    
#     root = logging.getLogger()
#     root.addHandler(queue_handler)

#     listener.start()

#     # while 1:
#     #     record = listener.dequeue(block=True)
#     #     listener.handle(record)
#     #     print(record)
#     #     time.sleep(1)
#     #     print(1)



# def initialize():
#     thread = threading.Thread(target=callback, args=tuple())
#     thread.daemon = True  # Daemonize thread ## Nice explantion about daemon threads : https://stackoverflow.com/a/190017
#     thread.start()        # Start the execution
#     print("started")