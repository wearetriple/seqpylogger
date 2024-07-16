import logging
from seqpylogger.seqpyloggerhandler import SeqPyLoggerHandler


def test_url_add_trailing_slash():
    # Arrange
    record = logging.LogRecord(
        "RecordName",
        logging.INFO,
        "pathename",
        1,
        "logmessage",
        args=(),
        exc_info=(),
        func="funcstr",
        sinfo="sinfostr",
    )
    logging.Formatter(fmt=None, datefmt=None, style="%").format(record)

    # Act
    result = SeqPyLoggerHandler.format_record_for_seq(record)

    # Assert
    assert result["@l"] == logging.getLevelName(logging.INFO)
    assert result["@mt"] == "logmessage"
    assert result["@m"] == "logmessage"


def test_format_message():
    # Arrange
    record = logging.LogRecord(
        "RecordName",
        logging.INFO,
        "pathename",
        1,
        "logmessage %s",
        args=("foo",),
        exc_info=(),
        func="funcstr",
        sinfo="sinfostr",
    )
    logging.Formatter(fmt=None, datefmt=None, style="%").format(record)

    # Act
    result = SeqPyLoggerHandler.format_message(record, formatter_style="%")

    # Assert
    assert record.message == "logmessage foo"
    assert record.msg == "logmessage {arg_0}"
    assert result == {"arg_0": "foo"}


def test_format_message_numbers():
    # Arrange
    record = logging.LogRecord(
        "RecordName",
        logging.INFO,
        "pathename",
        1,
        "logmessage %d",
        args=(123,),
        exc_info=(),
        func="funcstr",
        sinfo="sinfostr",
    )
    logging.Formatter(fmt=None, datefmt=None, style="%").format(record)

    # Act
    result = SeqPyLoggerHandler.format_message(record, formatter_style="%")

    # Assert
    assert record.message == "logmessage 123"
    assert record.msg == "logmessage {arg_0}"
    assert result == {"arg_0": "123"}


def test_extra_properties():
    # Arrange
    record = logging.LogRecord(
        "RecordName",
        logging.INFO,
        "pathename",
        1,
        "logmessage %d",
        args=(123,),
        exc_info=(),
        func="funcstr",
        sinfo="sinfostr",
    )
    record.uniqueprop = "uniquevalue"

    # Act
    result = SeqPyLoggerHandler().parse_record(record)

    # Assert
    assert record.message == "logmessage 123"
    assert record.msg == "logmessage {arg_0}"
    assert result["arg_0"] == "123"
    assert result["uniqueprop"] == "uniquevalue"
