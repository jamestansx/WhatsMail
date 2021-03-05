import logging
import os

import config
import setting

userLog_path = ""
logger = None


def loggerConfig():
    global userLog_path, logger
    dirs = setting.getDirs(config.appname, config.appauthor)
    userLog_path = os.path.join(dirs["userLog"], "log.log")
    logging.basicConfig(
        filename=userLog_path,
        filemode="w",
        format="%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s",
        encoding="utf-8",
        level=logging.DEBUG,
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logger = logging.get_logger()


def stopLogging():
    logging.shutdown()
