from .config import *
from .cursor import *
#import cx_Oracle
import collections
import logging

mlog = logging.getLogger("pySync.XTOracle")

class XTOracle:
    def __init__(self, cfg_name):
        with Config(r'config.cfg') as cfg:
            self.username = cfg.get(cfg_name,'username')
            self.password = cfg.get(cfg_name,'password')
            self.host     = cfg.get(cfg_name,'host')
            self.port     = cfg.get(cfg_name,'port')
            self.service  = cfg.get(cfg_name,'service_name')
            self.tnsname  = cfg.get(cfg_name,'tnsname')

        try:
            self.db = Connection(user=self.username, password=self.password, dsn=self.tnsname, mode=cx_Oracle.SYSDBA)
        except Exception as e:
            mlog.critical(e, exc_info=True)
            raise
        finally:
            mlog.debug("Connected to {} successfully".format(self.tnsname))

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        pass

    def execute(self, sql, binds=None):
        cursor = self.db.cursor()
        if binds is not None:
            cursor.execute(sql, binds)
        else:
            cursor.execute(sql)
        return cursor

    def q_select(self, sql, binds=None):
        cur = self.execute(sql, binds)
        return cur


    def execute_fetch_all_y(self, sql):
        try:
            cur = self.execute(sql)
            yield cur.fetchall()
        finally:
            cur.close()

    def prettyprint_namedtuple(namedtuple,field_spaces):
        assert len(field_spaces) == len(namedtuple._fields)
        string = "{0.__name__}( ".format(type(namedtuple))
        for f_n,f_v,f_s in zip(namedtuple._fields,namedtuple,field_spaces):
            string+= "{f_n}={f_v!r:<{f_s}}".format(f_n=f_n,f_v=f_v,f_s=f_s)
        return string+")"
