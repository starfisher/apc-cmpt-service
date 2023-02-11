# logger.py
# _*_ coding: utf-8 _*_
import logging
import os.path
import time
import yaml
import logging.config

project_path = 'apc-cmpt-service'  # 定义项目目录


class Logger(object):
    def __init__(self):
        # 获取当前文件所在目录路径
        current_path = os.path.dirname(os.path.abspath(project_path))
        # 指定分隔符对字符串进行切片
        path1 = current_path.split(project_path)
        path2 = [path1[0], project_path]
        # 日志目录路径
        log_path = ''.join(path2) + '/logs/'
        # 配置文件路径
        config_path = ''.join(path2) + '/config/config.yaml'

        # 获取当前时间(年月日)作为下级目录名称
        dir_time = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 获取当前时间作为日志文件名称
        current_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # 定义日志文件路径以及名称
        log_name = log_path + dir_time + '/' + current_time + '.log'

        if not os.path.exists(log_path + dir_time):
            os.makedirs(log_path + dir_time)

        try:
            with open(file=config_path, mode='r', encoding="utf-8") as file:
                logging_yaml = yaml.load(stream=file, Loader=yaml.FullLoader)
                logging_yaml['handlers']['file_handler']['filename'] = log_name
            # 配置logging日志
            logging.config.dictConfig(config=logging_yaml)
            # 创建一个logger(初始化logger)
            self.log = logging.getLogger()
        except Exception as e:
            print(e)

    # 日志接口
    def debug(cls, msg):
        cls.log.debug(msg)
        return

    def info(cls, msg):
        cls.log.info(msg)
        return

    def error(cls, msg):
        cls.log.error(msg)
        return


if __name__ == '__main__':
    logger = Logger()
    logger.info('This is info')
    logger.debug('This is debug')
    logger.error('This is error')
