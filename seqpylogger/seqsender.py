"""
Handels seq http call
"""
from typing import List
import logging
import datetime

import requests

from . import utils, config

LOG = logging.getLogger(config.LOGGER_NAME)


class SeqSender:
    """
    Handels seq http call
    """

    @staticmethod
    def send(batch_objects: List[str]):
        """Sends and setups call to seq

        Parameters
        ----------
        batch_objects : List[str]
            seq log data
        """

        message_body = str.join("\n", batch_objects)
        headers = {
            "X-Seq-ApiKey": config.SEQ_APIKEY,
            "Content-type": "application/vnd.serilog.clef",
        }
        server_url = utils.url_add_trailing_slash(config.SEQ_SERVER)

        ok_result = SeqSender._send_call(server_url, headers, message_body)
        if not ok_result:
            SeqSender._fallback(message_body)

    @staticmethod
    def _send_call(server_url: str, headers: dict, message_body: str) -> bool:
        """Does http call to seq

        Parameters
        ----------
        server_url : str
            seq server
        headers : dict
            http call headers with api key
        message_body : str
            data to send

        Returns
        -------
        bool
            ok status
        """
        ok_status = True
        try:
            resonse = requests.post(
                f"{server_url}api/events/raw", data=message_body, headers=headers
            )
            resonse.raise_for_status()
        except Exception:
            LOG.exception("SeqPyLogger sending raised exception")
            ok_status = False
        return ok_status

    @staticmethod
    def _fallback(message_body: str):
        """Handels fallback when sending failed

        Parameters
        ----------
        message_body : str
            data meant to be send to seq
        """
        # Complete fallback
        with open("seqpylogger_error.log", "a", encoding="utf-8") as fstream:
            fstream.write(
                datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f%Z") + "\n"
            )
            fstream.write("Seq sending had an unhandeled exception\n")
            fstream.write(f"Failed to send the following log data:\n{message_body}\n")
        LOG.error(
            "SeqPyLogger failed to send messages to seq, see seqpylogger_error.log"
        )
