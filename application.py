"""
This is a sample application that demonstrates how to use the SeqPyLogger library.
"""

import logging
import time
import datetime
import os
import uuid
import dotenv

import threading

globalobj = threading.local()


def spawn_thread():
    globalobj.request_id = str(uuid.uuid4())
    for i in range(10):
        logger.info("Thread log message %d", i)
        time.sleep(1)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(globalobj, "request_id", "N/A")
        return True


class NonSerializableObject:
    def __init__(self) -> None:
        self.a = "a"
        self.b = "b"


if __name__ == "__main__":
    dotenv.load_dotenv()

    os.environ["Environment"] = "Staging"
    os.environ["SEQ_SERVER"] = "http://localhost:5341/"
    os.environ["SEQ_APIKEY"] = "xxx"

    from seqpylogger import SeqPyLogger

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    seqLogger = SeqPyLogger()
    seqLogger.addFilter(RequestIdFilter())
    root.addHandler(seqLogger)
    logger = logging.getLogger("test_application")

    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    root.addHandler(ch)

    logger.info("starting", extra={"banana": "pie"})

    logger.info(
        "with nested extra", extra=dict(level1=dict(level2=dict(level3="hello")))
    )

    logger.info(
        "Object logging %s",
        NonSerializableObject(),
        extra={"object": NonSerializableObject()},
    )

    logger.debug("Debug log message")
    logger.info("Informational log message")
    logger.warning("Warning log message")
    logger.error("Error log message")
    logger.critical("Critical log message")
    logger.fatal("Critical log message")

    logger.info("Test log message with argument %s", "dummy argument")
    logger.info(
        "Test log message with arguments %s, %s", "dummy argument 1", "dummy argument 2"
    )

    # This does still not log correctly
    logger.info("Test log message with arguments double decimal %d, %d", 123, 321)

    try:
        raise Exception("Some issue")
    except:
        logger.exception("An error occured but now we have the stacktrace")
        # logging.error("There was an error", exc_info=1)  # alternative to .exception()

    try:
        raise Exception("Some issue")
    except:
        logger.fatal("This time no stacktrace")

    try:
        raise Exception("Some issue")
    except:
        logger.fatal("Stacktrace is not limited to ERROR", exc_info=1)

    logger.info("A wrong formated message {test}", "Arg0")

    for _ in range(3):
        threading.Thread(target=spawn_thread).start()

    while True:
        try:
            nowstr = datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H-%M-%S UTC"
            )
            logger.info("Logging the time: %s", nowstr)
            time.sleep(4)
        except KeyboardInterrupt:
            break

    logger.info("Bye")
