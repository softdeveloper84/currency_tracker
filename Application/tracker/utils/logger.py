import logging


class Logger():
    """
    Logger class
    """
    logger_dict = dict()

    def __init__(cls, name):
        """ Init logger with name=name
        :param name: name of logger
        """
        PATH_TO_LOG = '/home/user/currTracker/Application/log/tracker.log'

        if not name in cls.logger_dict:
            cls.logger = logging.getLogger(name)
            cls.logger.setLevel(logging.DEBUG)
            filehandler = logging.FileHandler(PATH_TO_LOG)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            filehandler.setFormatter(formatter)
            cls.logger.addHandler(filehandler)
            cls.logger_dict[name] = cls.logger
        cls.logger = cls.logger_dict[name]

    def get_instance(cls):
        """
        :return: logger instance
        """
        return cls.logger
