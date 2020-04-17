"""
This module returns a Handler

inside the module the follwing happens
Handler is a queueHandler and can add LogRecords to a queue
Next a queueListener(handler)
Gets items from this queue and passes them to a BufferHandler (with a 10 item capacity)
After capacity the BufferHandler flushes the log messages to a custom http sender, for seq
"""

from .seqpylogger import SeqPyLogger
