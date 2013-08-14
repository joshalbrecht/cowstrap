
import sys
import logging

#configure log formatting
DEFAULT_FORMAT = "%(asctime)s %(name)s [%(levelname)s]:%(message)s"
formatter = logging.Formatter(DEFAULT_FORMAT)

#set up the root logger
log = logging.getLogger('cowstrap')
log.setLevel(logging.WARN)

#configure logging to stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
log.addHandler(stdout_handler)
