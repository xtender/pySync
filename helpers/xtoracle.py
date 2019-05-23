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
            #self.db = cx_Oracle.connect(user=self.username, password=self.password, dsn=self.tnsname,mode=cx_Oracle.SYSDBA)
            self.db = Connection(user=self.username, password=self.password, dsn=self.tnsname,mode=cx_Oracle.SYSDBA)
        except cx_Oracle.DatabaseError as e:
            # Log error as appropriate
            raise

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        pass

    def execute(self, sql, binds=None):
        cursor = self.db.cursor()
        if binds is not None:
            cursor.execute(sql, binds)
        else:
            cursor.execute(sql)
        return cursor


    #def q_select(self, sql):
    #    cur = self.execute(sql)
    #    names = [c[0] for c in cur.description]
    #    cur.rowfactory = collections.namedtuple("ResultSet",names)
    #    res = cur.fetchall()
    #    cur.close()
    #    return res[0]

    def q_select(self, sql, binds=None):
        cur = self.execute(sql, binds)
        #try:
        #    names = [c[0] for c in cur.description]
        #    cur.rowfactory = collections.namedtuple("ResultSet",names)
        #except ValueError as e:
        #    mlog.error("Value error: {0}".format( str(e)))
        
        return cur
        #res = cur.fetchall()
        #cur.close()
        #for row in res:
        #    print row
        #print "============================="
        #return res[0]


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
