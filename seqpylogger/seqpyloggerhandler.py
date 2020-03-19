import datetime
import json
import logging
import queue
import os
import re
import threading
import traceback
import requests
from logging.handlers import BufferingHandler



class SeqPyLoggerHandler(BufferingHandler):
    def __init__(self, capacity=10):
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