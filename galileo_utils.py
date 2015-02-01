import logging
import galileo
import galileo.main

class GalileoLogHandler(logging.Handler):
    def __init__(self, error_fn):
        logging.Handler.__init__(self)

        self.error_fn = error_fn

    def emit(self, record):
        if record.levelno == logging.ERROR :
            self.error_fn(record.getMessage())

def start_galileo(error_fn):
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger()

    handler = GalileoLogHandler(error_fn)

    logging.getLogger(galileo.__name__).addHandler(handler)

    galileo.main.main()
    return galileo.main