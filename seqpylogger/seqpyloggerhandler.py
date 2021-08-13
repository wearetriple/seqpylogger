"""
Handles incomming log records with buffer
"""
import datetime
import json
import logging
import traceback
from typing import Optional, Dict
from logging.handlers import BufferingHandler
from . import config, seqsender


LOG = logging.getLogger(config.LOGGER_NAME)


class SeqPyLoggerHandler(BufferingHandler):
    """
    Handles incomming log records with buffer
    """

    def __init__(self, capacity=10, formatter_style="%"):
        self.formatter_style = formatter_style
        super().__init__(capacity=capacity)

    def flush(self):
        try:
            self.acquire()
            if len(self.buffer) > 0:
                self.send_to_seq()
                super().flush()
        finally:
            self.release()

    def send_to_seq(self):
        """Prepares record for sending to seq"""
        batch_objects = []
        for record in self.buffer:
            # format_message monkey patchs LogRecord with .message
            record_args = SeqPyLoggerHandler.format_message(
                record, self.formatter_style
            )
            record_object = SeqPyLoggerHandler.format_record_for_seq(record)
            record_object.update(record_args)

            ex = SeqPyLoggerHandler.add_exception(record)
            if ex is not None:
                record_object.update({"@x": ex})

            batch_objects.append(json.dumps(record_object, separators=(",", ":")))

        seqsender.SeqSender.send(batch_objects)

    @staticmethod
    def format_record_for_seq(record: logging.LogRecord) -> dict:
        """Creates seq record object

        Parameters
        ----------
        record : logging.LogRecord
            Record to handle

        Returns
        -------
        dict
            formatted according to seq specs
        """
        record_object = {
            "@t": datetime.datetime.fromtimestamp(record.created).strftime(
                "%Y-%m-%dT%H:%M:%S.%f%Z"
            ),
            "@l": record.levelname,
            "@mt": record.msg,
            "@m": record.message,
            "@@Logger": record.name,
            "@@Path": record.pathname,
            "@@Line": record.lineno,
            "@@Function": record.funcName,
            "@@Thread": record.threadName,
            "@@Pid": record.process,
            "@@Environment": config.ENVIRONMENT,
        }

        return record_object

    @staticmethod
    def add_exception(record: logging.LogRecord) -> Optional[str]:
        """Addeds traceback data to log message

        Parameters
        ----------
        record : logging.LogRecord
            LogMessage to handle

        Returns
        -------
        Optional[str]
            Returns message with added traceback or None
        """
        if record.exc_info and any(record.exc_info):
            return str.join("", traceback.format_exception(*record.exc_info))
        return None

    @staticmethod
    def format_message(
        record: logging.LogRecord, formatter_style: str
    ) -> Dict[str, str]:
        """Prepares message shape for sending to seq as this requires a different syntax

        Parameters
        ----------
        record : logging.LogRecord
            LogMessage to handle

        formatter_style : str
            Log message formatting style should be "%"

        Returns
        -------
        dict
            dict of extra arguments in message
        """
        record_args: Dict[str, str] = {}
        if formatter_style != "%":
            logging.warning("SeqPyLogger Unimplemented formatting style")
            return record_args

        # Prevent logging not str type
        if not isinstance(record.msg, str):
            record.msg = str(record.msg)

        try:
            record.message = record.msg % record.args
        except TypeError:
            LOG.warning("SeqPyLogger message formatting failed - (%s)", record.msg)
            record.message = record.msg
        for i, arg in enumerate(record.args):
            record_args.update({"arg_%d" % i: str(arg)})
            record.msg = record.msg.replace("%s", "{arg_%d}" % i, 1)

        return record_args
