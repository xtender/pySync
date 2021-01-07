import ConfigParser
import logging

mlog = logging.getLogger("pySyncOracleStandby.Config")

class Config:
    def __init__(self, filename):
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(filename))
        mlog.debug('init')

    def __enter__(self):
        return self.config

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        mlog.debug('exit')
