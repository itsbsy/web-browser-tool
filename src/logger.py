import logging
from colorlog import ColoredFormatter

class Logger:
    '''
    A class to represent a more generic and flexible logger, reintegrating convenience methods.
    '''
    def __init__(self, name="DefaultLogger", level=logging.INFO, log_format=None, 
                 name_color='green', asctime_color='blue', levelname_color='red', message_color='reset', filename=None):
        '''
        Construct a new logger.
        
        Parameters:
            name (str): The name of the logger.
            level (int): The logging level.
            log_format (str): The format for the logging messages, with color customization.
            name_color (str), asctime_color (str), levelname_color (str), message_color (str): Custom colors.
        '''
        self.name = name
        self.level = level
        self.log_format = log_format or self.default_log_format(name_color, asctime_color, levelname_color, message_color)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        self.setup_logger()

    # Default log format
    def default_log_format(self, name_color, asctime_color, levelname_color, message_color):
        '''Generates a default log format string using specified colors.'''
        return f"%({name_color})s%(name)s%(reset)s | %({asctime_color})s%(asctime)s%(reset)s |     %({levelname_color})s%(levelname)-s%(reset)s     | %({message_color})s%(message)s%(reset)s"

    # Set up the logger
    def setup_logger(self):
        '''Sets up a logger with a colored formatter.'''
        formatter = ColoredFormatter(self.log_format)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.level)
        stream_handler.setFormatter(formatter)
        
        # Check if the handler is already added to avoid duplication
        if not any(isinstance(handler, logging.StreamHandler) for handler in self.logger.handlers):
            self.logger.addHandler(stream_handler)

    # Convenience methods
    def debug(self, message):
        '''Log a debug message.'''
        self.logger.debug(message)

    def info(self, message):
        '''Log an informational message.'''
        self.logger.info(message)

    def warning(self, message):
        '''Log a warning message.'''
        self.logger.warning(message)

    def error(self, message):
        '''Log an error message.'''
        self.logger.error(message)

    def critical(self, message):
        '''Log a critical message.'''
        self.logger.critical(message)

logger = Logger(name="Group Chat", level=logging.DEBUG)
