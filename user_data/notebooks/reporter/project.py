import os 
import pathlib

import logging
import logging.handlers
import os
 
from datetime import datetime

__curr_dir=pathlib.Path(__file__).parent.resolve()


def userdata():
    return __curr_dir.parent.parent.resolve()

def userdata(sub):
    return __curr_dir.parent.parent.joinpath(sub).resolve()

def notebooks(subdir,filename = None):
    path = userdata('notebooks').joinpath(subdir).resolve()
    if not os.path.exists(path):
        os.mkdir(path)

    if filename:
        return path.joinpath(filename).resolve()
    else:
        return path

def backtest_results(subdir,filename = None):
    path = userdata('backtest_results').joinpath(subdir).resolve()
    if not os.path.exists(path):
        os.mkdir(path)

    if filename:
        return path.joinpath(filename).resolve()
    else:
        return path

def backtest_reports(subdir,filename = None):

    path = userdata('backtest_reports').joinpath(subdir).resolve()
    if not os.path.exists(path):
        os.mkdir(path)

    if filename:
        return path.joinpath(filename).resolve()
    else:
        return path

logger = logging.getLogger()

def init_log(enable):

    #init logging
    logfile =  datetime.now().strftime('mylogfile_%H_%M_%d_%m_%Y.log')

    handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", notebooks('logs').joinpath(logfile)))

    formatter = logging.Formatter(logging.BASIC_FORMAT)

    handler.setFormatter(formatter)

    logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    logger.addHandler(handler)
    logger.propagate = enable
