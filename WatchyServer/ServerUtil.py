import sys
import logging

version = '@VERSION@'

def info (message): logging.info (message)

def debug (message): logging.debug (message)

def warning (message): logging.warning (message)

def error (message): logging.error (message)

def fatal (message, _exit=True):
    logging.fatal (message)
    if _exit is True:
        sys.exit (1)
