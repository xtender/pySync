from .config import *

from .xtoracle import *
import cx_Oracle
import collections
import logging
import os

mlog = logging.getLogger("pySync.Standby")

class Standby(XTOracle, object):
    def __init__(self):
        cfg_name='standby'
        super(Standby, self).__init__(cfg_name)
        with Config(r'config.cfg') as cfg:
            self.archivelog_dest = cfg.get(cfg_name,'archivelog_dest')

        mlog.info("Standby version: " + self.db.version)

    def get_last_log(self):
        cur = self.q_select('select max(sequence#) last_sequence from v$archived_log')
        res = cur.fetchone()
        return res.LAST_SEQUENCE

    def get_logs(self):
        #'CATALOG START WITH \'/opt/oracle/ARCHIVE/COEUSL\''
        print 'a'

    def download_archivelog(self, archivelog):
        from .primary import Primary
        cmd = Primary().get_ssh() + archivelog + " " + self.archivelog_dest
        mlog.info(cmd)
        os.system(cmd)

    def download_all(self):
        from .primary import Primary
        res = Primary().get_logs()
        for archivelog in res:
            self.download_archivelog(archivelog.NAME)

    def catalog_archivelogs(self, cmd=None):
        cmd = "echo \"catalog start with '{0}' noprompt;\" | rman target sys/{1}@{2} ".format(self.archivelog_dest, self.password, self.tnsname)
        mlog.info(cmd)
        os.system("ls -l " + self.archivelog_dest)
        os.system(cmd)
        os.system("chown oracle:oinstall {0}/*".format(self.archivelog_dest))
        os.system("ls -l " + self.archivelog_dest)

if __name__ == "__main__":
    res = Standby().execute_fetch_all('select level a from dual connect by level<10')
    res = list(res)[0]
    for result in res:
        print result
    #result = list(res)
    #print result
