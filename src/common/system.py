import os

import configparser
from loguru import logger
import sys
import platform
import socket


class System:
    conf = configparser.ConfigParser()
    __root_path = None

    @staticmethod
    def log_init():
        logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")
        logger.add("log/log_info.log", backtrace=True, diagnose=True, format="{time} {level}  {message}",
                   level="INFO", rotation="11:45")
        logger.add("log/log_error.log", backtrace=True, diagnose=True, format="{time} {level} {message}",
                   level="ERROR", rotation="11:45")

    @staticmethod
    def get_root_path():
        if System.__root_path is None:
            cur_path = os.path.abspath(os.path.dirname(__file__))
            plat = platform.system().lower()
            if plat == 'windows':
                System.__root_path = cur_path[:cur_path.find("apc-cmpt-service\\") + len("apc-cmpt-service\\")]
                System.__root_path = System.__root_path.replace('\\', '/')
                return System.__root_path
            elif plat == 'linux':
                System.__root_path = cur_path[:cur_path.find("apc-cmpt-service/") + len("apc-cmpt-service/")]
                return System.__root_path
        else:
            return System.__root_path


    @staticmethod
    def get_context():
        return sys.modules['__main__'].__dict__

    @staticmethod
    def set_context(key, value):
        sys.modules['__main__'].__dict__[key] = value

    @staticmethod
    def read_config(file):
        System.conf.read(file, encoding="utf-8-sig")

    @staticmethod
    def get_local_ip():
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)
        return ip
