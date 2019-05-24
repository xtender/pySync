from .config import *
from .xtoracle import *
from .common import *
import cx_Oracle
import collections
import logging
import os
import subprocess

mlog = logging.getLogger("pySync.Standby")

SQL_STANDBY_GET_LAST_LOG = 'sql/standby_get_last_log.sql'
SQL_STANDBY_GET_LAST_APPLIED_LOG = 'sql/standby_get_last_applied_log.sql'

class Standby(XTOracle, object):
    def __init__(self):
        cfg_name='standby'
        super(Standby, self).__init__(cfg_name)
        with Config(r'config.cfg') as cfg:
            self.archivelog_dest = cfg.get(cfg_name,'archivelog_dest')
            self.catalog_command = cfg.get(cfg_name,'catalog_command')

        mlog.debug("Standby version: " + self.db.version)

    def get_last_log(self):
        cmd = get_file_contents(SQL_STANDBY_GET_LAST_LOG)
        mlog.debug("Executing SQL_STANDBY_GET_LAST_LOG: ")
        mlog.debug(cmd)
        cur = self.q_select(cmd)
        res = cur.fetchone()
        mlog.info("LAST_SEQUENCE: " + str(res.LAST_SEQUENCE))
        return res.LAST_SEQUENCE

    def get_last_applied_log(self):
        cmd = get_file_contents(SQL_STANDBY_GET_LAST_APPLIED_LOG)
        mlog.debug("Executing SQL_STANDBY_GET_LAST_APPLIED_LOG: ")
        mlog.debug(cmd)
        cur = self.q_select(cmd)
        res = cur.fetchone()
        mlog.debug("SQL_STANDBY_GET_LAST_APPLIED_LOG: " + str(res.LAST_SEQUENCE))
        return res.LAST_SEQUENCE

    def get_logs(self):
        #'CATALOG START WITH \'/opt/oracle/ARCHIVE/COEUSL\''
        print 'a'

    def download_archivelog(self, archivelog):
        from .primary import Primary
        #cmd = Primary().get_ssh() + archivelog + " " + self.archivelog_dest
        mlog.info("Copying {} from Primary to Standby {}...".format(archivelog, self.archivelog_dest))
        cmd = Primary().get_download_command().format(logname = archivelog, logdest = self.archivelog_dest)
        mlog.debug("Executing " + cmd)
        #os.system(cmd)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        mlog.debug(output)
        mlog.info("{} copied successfully".format(archivelog))

    def download_all(self):
        from .primary import Primary
        mlog.debug("download_all: start")
        cur = Primary().get_logs()
        res = cur.fetchall()
        mlog.info("{} new logs found.".format(len(res)))
        for archivelog in res:
            mlog.debug("SEQUENCE={0}, FIRST_TIME={1}, NEXT_TIME={2} ARCHIVED={3} APPLIED={4}) NAME={5}"
                        .format(archivelog.SEQUENCE, archivelog.FIRST_TIME, archivelog.NEXT_TIME, archivelog.ARCHIVED, archivelog.APPLIED, archivelog.NAME))
            self.download_archivelog(archivelog.NAME)
        mlog.debug("download_all: completed")
        mlog.debug("{} archivelogs downloaded".format(cur.rowcount))
        return cur.rowcount

    def catalog_archivelogs(self, cmd=None):
        mlog.debug("catalog_archivelogs: start")
        #cmd = "echo \"catalog start with '{0}' noprompt;\" | rman target sys/{1}@{2} ".format(self.archivelog_dest, self.password, self.tnsname)
        cmd = self.catalog_command.format(archivelog_dest = self.archivelog_dest, password = self.password, tnsname = self.tnsname)
        mlog.debug(cmd)
        #os.system("ls -l " + self.archivelog_dest)
        #os.system(cmd)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        mlog.debug(output)
        #os.system("chown oracle:oinstall {0}/*".format(self.archivelog_dest))
        #os.system("ls -l " + self.archivelog_dest)
        mlog.info("catalog_archivelogs: completed")
