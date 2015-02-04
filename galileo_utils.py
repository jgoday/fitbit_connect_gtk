import logging
import galileo
import galileo.main
import time

from galileo.config import Config

class GalileoLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

        self.error_message = None
        self.info_message = None

    def has_error(self):
        return self.error_message is not None

    def has_info(self):
        return self.info_message is not None

    def clean(self):
        self.error_message = None
        self.info_message = None

    def emit(self, record):
        if record.levelno == logging.ERROR :
            self.error_message = record.getMessage()
        elif record.levelno == logging.INFO :
            self.info_message = record.getMessage()

def galileo_start(log_handler):
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger()

    logging.getLogger(galileo.__name__).addHandler(log_handler)


    config = galileo_load_config()

    galileo.main.sync(config)


def galileo_load_config():
    config = Config()

    config.parseSystemConfig()
    config.parseUserConfig()

    # This gives us the config file name
    config.parseArgs()

    if config.rcConfigName:
        config.load(config.rcConfigName)
        # We need to apply our arguments as last
        config.applyArgs()

    return config