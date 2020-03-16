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
import os
import threading
import traceback
import time
import uuid
import re
from string import Formatter
from logging.handlers import QueueListener, QueueHandler, BufferingHandler

import requests

class SeqPyLogger:
    def __init__(self):
        pass

    @staticmethod
    def createQueueHandler(buffer_capacity=10):
        """createHandler
        
        Returns
        -------
        QueueHandler
            Handler for sending LogRecords to Seq
        """
        queue_handler = SeqPyLoggerQueueHandler(queue.Queue(-1))

        handler = SeqPyLogger.createBufferHandler(capacity=buffer_capacity)
        
        listener = SeqPyLoggerQueueListener(queue_handler.queue, handler)
        
        listener.start()
        
        return queue_handler

    @staticmethod
    def createBufferHandler(capacity=10):
        logger = SeqPyLoggerHandler(capacity=capacity)
        # formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
        # logger.setFormatter(formatter)
        return logger
    
class SeqPyLoggerHandler(BufferingHandler):
    def __init__(self, capacity=10):
        self.re_args = re.compile(r"\{.+\}")
        super().__init__(capacity=10)
    
    def flush(self):
        # for record in self.buffer:
        #     print(self.format(record))
        self.send_to_seq()
        return super().flush()
    
    def send_to_seq(self):
        batch_objects = []
        for record in self.buffer:
            record_object = {
                "@t": datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"),
                "@l": record.levelname,
                "@mt": record.msg,
                "@m": record.msg,
                "@@Logger": record.name,
                "@@Path": record.pathname,
                "@@Line": record.lineno,
                "@@Function": record.funcName,
                "@@Thread": record.threadName,
                "@@Pid": record.process,
                "@@Environement": os.getenv("Environment", "NOT-SET")
            }

            message = record.msg
            for i, match in enumerate(self.re_args.findall(record.msg)):
                try:
                    message = message.replace(match, record.args[i])
                    record_object.update({match[1:-1]: record.args[i]})
                except:
                    pass
            record_object.update({"@m": message})
            ex = self.add_exception(record)
            if ex is not None:
                record_object.update({"@x": ex})
            print(record_object)
            batch_objects.append(json.dumps(record_object, separators=(',', ':')))
            
        message_body = str.join("\n", batch_objects)
        headers = {
            "X-Seq-ApiKey": os.getenv("SEQ_APIKEY"),
            "Content-type": "application/vnd.serilog.clef"
        }
        server_url = os.getenv('SEQ_SERVER')
        if (server_url[-1] != "/"):
            server_url += "/"

        resonse = requests.post(f"{os.getenv('SEQ_SERVER')}api/events/raw", data=message_body, headers=headers)
        print(resonse.status_code, resonse.text)
    
    def add_exception(self, record):
        if record.exc_info and any(record.exc_info):
            return str.join('', traceback.format_exception(*record.exc_info))
        else:
            return None


class SeqPyLoggerQueueHandler(QueueHandler):
    def __init__(self, queue):
        super().__init__(queue)
    
    def prepare(self, record):
        return record
    
    def flush(self):
        return super().flush()


class SeqPyLoggerQueueListener(QueueListener):
    def __init__(self, queue, handler):
        super().__init__(queue, handler)
    
    def prepare(self, record):
        return record

