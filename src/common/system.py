import os

from loguru import logger
import sys


def log_init():
    logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")
    logger.add("log/log_info.log", backtrace=True, diagnose=True, format="{time} {level}  {message}", level="INFO", rotation="11:45")
    logger.add("log/log_error.log", backtrace=True, diagnose=True, format="{time} {level} {message}", level="ERROR", rotation="11:45")


def get_root_path():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path[:cur_path.find("apc-cmpt-service\\") + len("apc-cmpt-service\\")]
    root_path = root_path.replace('\\', '/')
    return root_path
