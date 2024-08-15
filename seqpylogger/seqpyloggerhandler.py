"""
Handles incomming log records with buffer
"""

import datetime
import logging
import traceback

from typing import Optional, Dict
from logging.handlers import BufferingHandler

from seqpylogger import config, seqsender
from seqpylogger.serialization import json_serialize


LOG = logging.getLogger(config.LOGGER_NAME)


class SeqPyLoggerHandler(BufferingHandler):
    """
    Handles incomming log records with buffer
    """

    # These are the standard log record attributes
    RECORD_KEYS = set(
        [
            x
            for x in logging.LogRecord(
                "name", 0, "pathname", 0, "msg", None, None
            ).__dict__.keys()
            if x[0] != "_"
        ]
    )

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
            try:
                record_object = self.parse_record(record)
            except Exception as ex:
                LOG.debug("SeqPyLogger failed to parse record", exc_info=ex)
                record_object = self.fallback_parse(record)
            batch_objects.append(json_serialize(record_object))

        seqsender.SeqSender.send(batch_objects)

    def parse_record(self, record: logging.LogRecord):
        # format_message monkey patchs LogRecord with .message
        record_args = self.format_message(record, self.formatter_style)

        record_object = self.format_record_for_seq(record)
        record_extras = self.get_extra_properties(record)

        record_object.update(record_args)
        record_object.update(record_extras)

        ex = self.add_exception(record)
        if ex is not None:
            record_object.update({"@x": ex})

        return record_object

    @staticmethod
    def fallback_parse(record: logging.LogRecord) -> dict:
        """Fallback for parsing record, uses plain string message and no extra properties"""
        record.msg = f"{str(record.msg)} - [{str(record.args)}]"
        record.message = record.msg
        return SeqPyLoggerHandler.format_record_for_seq(record)

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
    def get_extra_properties(record: logging.LogRecord) -> dict:
        """Returns non standard log record properties

        Parameters
        ----------
        record : logging.LogRecord
            initial log record

        Returns
        -------
        dict
            non standard log record properties
        """

        # get all record attributes
        record_keys = set([x for x in record.__dict__.keys() if x[0] != "_"])
        extra_keys = record_keys.difference(SeqPyLoggerHandler.RECORD_KEYS)

        return {key: getattr(record, key, None) for key in extra_keys}

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
            LOG.debug("SeqPyLogger Unimplemented formatting style")
            return record_args

        # Prevent logging not str type
        if not isinstance(record.msg, str):
            record.msg = str(record.msg)

        try:
            record.message = record.msg % record.args
        except TypeError as ex:
            msg = str(record.msg)
            LOG.debug(
                "SeqPyLogger message formatting failed",
                extra={"msg_template": msg},
                exc_info=ex,
            )
            record.message = record.msg

        # Fixes %d not being replaced
        record.msg = record.msg.replace("%d", "%s")

        for i, arg in enumerate(record.args):
            record_args.update({"arg_%d" % i: str(arg)})
            record.msg = record.msg.replace("%s", "{arg_%d}" % i, 1)

        return record_args
