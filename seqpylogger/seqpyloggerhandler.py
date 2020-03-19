import datetime
import json
import logging
import queue
import os
import re
import threading
import traceback
from string import Formatter
import requests
from logging.handlers import BufferingHandler



class SeqPyLoggerHandler(BufferingHandler):
    def __init__(self, capacity=10, formatter_style='%'):
        self.formatter_style = formatter_style
        self.re_args = re.compile(r"\{.+\}")
        super().__init__(capacity=10)
    
    def flush(self):
        # for record in self.buffer:
        #     print(self.format(record))
        if len(self.buffer) > 0:
            self.send_to_seq()
        return super().flush()
    
    def send_to_seq(self):
        batch_objects = []
        for record in self.buffer:
            record_args = self.format_message(record)

            record_object = {
                "@t": datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%dT%H:%M:%S.%f%Z"),
                "@l": record.levelname,
                "@mt": record.msg,
                "@m": record.message,
                "@@Logger": record.name,
                "@@Path": record.pathname,
                "@@Line": record.lineno,
                "@@Function": record.funcName,
                "@@Thread": record.threadName,
                "@@Pid": record.process,
                "@@Environment": os.getenv("Environment", "NOT-SET")
            }

            record_object.update(record_args)
            
            ex = self.add_exception(record)
            if ex is not None:
                record_object.update({"@x": ex})
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
    
    def add_exception(self, record):
        if record.exc_info and any(record.exc_info):
            return str.join('', traceback.format_exception(*record.exc_info))
        else:
            return None
    
    def format_message(self, record):
        if (self.formatter_style != "%"):
            print("Unimplemented formatting style")

        record_args = {}
        record.message = record.msg % record.args
        for i, arg in enumerate(record.args):
            record_args.update({"arg_%d" % i: arg})
            record.msg = record.msg.replace("%s", "{arg_%d}" % i , 1)
        
        return record_args