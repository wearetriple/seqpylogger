import logging
import time
import datetime
import os
import dotenv
from seqpylogger import SeqPyLogger

if __name__ == "__main__":
    dotenv.load_dotenv()

    os.environ["Environment"] = "Staging"

    root = logging.getLogger()
    seqLogger = SeqPyLogger()
    root.addHandler(seqLogger)
    logger = logging.getLogger('test_application')
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    logger.debug("Debug log message")
    logger.info("Informational log message")
    logger.warning("Warning log message")
    logger.error("Error log message")
    logger.critical("Critical log message")
    logger.fatal("Critical log message")

    logger.info("Test log message with argument %s", "dummy argument")
    logger.info("Test log message with arguments %s, %s", "dummy argument 1", "dummy argument 2")

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

    while True:
        try:
            logger.info("Logging the time: %s", datetime.datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S UTC"))
            time.sleep(4)
        except KeyboardInterrupt:
            break
            
    
    # Run manual flush with wait to prevent last messages not sending when program ends
    logger.info("Bye")
    seqLogger.manual_flush(wait=5)