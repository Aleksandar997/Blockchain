from logging import *
from environment import DATA_FOLDER_PATH

class BaseLogger:
    logger: Logger

    def log_debug(self, message):
        self.logger.debug(message + '\\n')

    def log_info(self, message):
        self.logger.info(message + '\\n')

    def log_warning(self, message):
        self.logger.warning(message + '\\n')

    def log_exception(self, message):
        self.logger.exception(message + '\\n')

    def log_critical(self, message):
        self.logger.critical(message + '\\n')

    def init_logger(self):
        basicConfig(filename=DATA_FOLDER_PATH + "\exception.log", 
                        format='%(asctime)s %(message)s', 
                        filemode='w') 

        self.logger = getLogger()

        self.logger.setLevel(DEBUG)

        return self


class LoggerService:
    logger = BaseLogger().init_logger()
