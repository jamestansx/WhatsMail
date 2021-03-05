import logging
import os

import config
import setting

userLog_path = ""
logger = None


def loggerConfig():
    global userLog_path, logger
    dirs = setting.getLogDir(config.appname, config.appauthor)
    userLog_path = os.path.join(dirs, "log.log")
    logging.basicConfig(
        filemode="w",
        format="%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s",
        encoding="utf-8",
        level=logging.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
        filename=userLog_path,
    )


def stopLogging():
    logging.shutdown()
