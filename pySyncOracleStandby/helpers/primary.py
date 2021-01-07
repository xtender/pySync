from .config import *
from .xtoracle import *
from .common import *
import cx_Oracle
import collections
import logging

mlog = logging.getLogger("pySyncOracleStandby.Primary")

SQL_ARCHIVE_LOG_CURRENT = 'sql/archive_log_current.sql'
SQL_PRIMARY_GET_NEW_ARCHIVELOGS='sql/primary_get_new_archivelogs.sql'
SQL_PRIMARY_GET_LAST_LOG='sql/standby_get_last_log.sql'

class Primary(XTOracle, object):
    def __init__(self):
        cfg_name='primary'
        super(Primary, self).__init__(cfg_name)
        with Config(r'config.cfg') as cfg:
            self.interval = cfg.get(cfg_name,'interval')
            self.download_command = cfg.get(cfg_name,'download_command')
            #self.ssh_user = cfg.get(cfg_name,'ssh_user')
            #self.ssh_pass = cfg.get(cfg_name,'ssh_pass')
            #self.ssh_port = cfg.get(cfg_name,'ssh_port')
        
        mlog.debug('Primary version: %s', self.db.version)

    def get_download_command(self):
        return self.download_command

    #def get_ssh(self):
    #    return ("sshpass -p '{0}' scp -p -P {1}  {2}@{3}:".format(self.ssh_pass, self.ssh_port, self.ssh_user, self.host))

    def get_last_log(self):
        cmd = get_file_contents(SQL_PRIMARY_GET_LAST_LOG)
        mlog.debug("Executing SQL_PRIMARY_GET_LAST_LOG: ")
        mlog.debug(cmd)
        cur = self.q_select(cmd)
        res = cur.fetchone()
        mlog.debug("PRIMARY LAST_SEQUENCE: " + str(res.LAST_SEQUENCE))
        return res.LAST_SEQUENCE

    def get_logs(self, last_log=None):
        if last_log is not None:
            logn = last_log
        else:
            from .standby import Standby
            logn = Standby().get_last_log()
        return self.q_select( get_file_contents(SQL_PRIMARY_GET_NEW_ARCHIVELOGS), {'seq':logn})

    def print_logs(self):
        from .standby import Standby
        res = self.get_logs(Standby().get_last_log())
        #mlog.debug(res)
        #pprint.pprint "========================================="
        
        n = 0
        for row in res:
            n+=1
            mlog.debug("ROW {0}( RECID={1}, SEQUENCE={2}, FIRST_TIME={3}, NEXT_TIME={4} ARCHIVED={5} APPLIED={6}) NAME={7}"
                        .format(n, row.RECID, row.SEQUENCE, row.FIRST_TIME, row.NEXT_TIME, row.ARCHIVED, row.APPLIED, row.NAME))
            mlog.debug("===========================================")

    def archive_log_current(self):
        try:
            cur = self.db.cursor()
            cmd = get_file_contents(SQL_ARCHIVE_LOG_CURRENT).format(interval = self.interval)
            
            mlog.debug("Executing archive_log_current: ")
            mlog.debug(cmd)
            cur.execute(cmd)
            mlog.info("archive_log_current has been finished successfully")
        except Exception as e:
            mlog.critical(e, exc_info=True)
        

