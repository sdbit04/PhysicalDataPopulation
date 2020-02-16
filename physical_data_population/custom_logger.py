import logging
import inspect
import os


def create_custom_logger(logging_level=logging.DEBUG):
    logging_level = logging_level
    logger_name = inspect.stack()[1][3]
    logger_ob = logging.getLogger(logger_name)
    logger_ob.setLevel(logging.DEBUG)
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    file_handler_ob = logging.FileHandler(filename="logs/{}.log".format(logger_name), mode='w')
    file_handler_ob.setLevel(logging_level)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
    file_handler_ob.setFormatter(formatter)
    logger_ob.addHandler(file_handler_ob)
    return logger_ob
