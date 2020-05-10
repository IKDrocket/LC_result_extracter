import logzero
import logging

LOG_FORMAT = '%(color)s[%(asctime)s %(levelname)s]%(end_color)s %(message)s'
FORMATTER = logzero.LogFormatter(fmt=LOG_FORMAT)

logger = logzero.setup_logger(
    level=logging.INFO,
    formatter=FORMATTER,
    disableStderrLogger=False
)
