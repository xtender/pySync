from .config import *
from .xtoracle import *
import cx_Oracle
import collections
import logging
import pprint

mlog = logging.getLogger("pySync.Primary")

class Primary(XTOracle, object):
    def __init__(self):
        cfg_name='primary'
        super(Primary, self).__init__(cfg_name)
        with Config(r'config.cfg') as cfg:
            self.interval = cfg.get(cfg_name,'interval')
            self.ssh_user = cfg.get(cfg_name,'ssh_user')
            self.ssh_pass = cfg.get(cfg_name,'ssh_pass')
            self.ssh_port = cfg.get(cfg_name,'ssh_port')
        
        mlog.info('Primary version: %s', self.db.version)

    def get_ssh(self):
        return ("sshpass -p '{0}' scp -p -P {1}  {2}@{3}:".format(self.ssh_pass, self.ssh_port, self.ssh_user, self.host))

    def get_logs(self, last_log=None):
        #cur = self.db.cursor()
        #cur.execute('select * from v$archived_log where dest_id=1 and sequence#=:seq',{'seq':last_log})
        #res = cur.fetchall()
        #cur.close()
        #return res
        
        if last_log is not None:
            logn = last_log
        else:
            from .standby import Standby
            logn = Standby().get_last_log()
        return self.q_select("""
            select
                    recid
                    ,name
                    ,sequence# as sequence
                    ,dest_id
                    ,resetlogs_change# as resetlogs_change
                    ,resetlogs_time
                    ,first_change# as first_change
                    ,first_time
                    ,next_change# as next_change
                    ,next_time
                    ,blocks
                    ,block_size
                    ,creator
                    ,standby_dest
                    ,archived
                    ,applied
                    ,deleted
                    ,status
                    ,completion_time
                    ,backup_count
            from v$archived_log
            where dest_id=1
              and sequence#>:seq""", {'seq':logn})
        
        #'CATALOG START WITH \'/opt/oracle/ARCHIVE/COEUSL\''
        #return self.q_select(

    def print_logs(self):
        from .standby import Standby
        res = self.get_logs(Standby().get_last_log())
        mlog.debug(res)
        #pprint.pprint "========================================="
        
        pp = pprint.PrettyPrinter(indent=4)
        n = 0
        for row in res:
            n+=1
            print n
            #pp.pprint(row)
            print ("ROW( RECID={0}, SEQUENCE={1}, FIRST_TIME={2}, NEXT_TIME={3} ARCHIVED={4} APPLIED={5})".format(row.RECID, row.SEQUENCE, row.FIRST_TIME, row.NEXT_TIME, row.ARCHIVED, row.APPLIED))
            print "==========================================="

    def archive_log_current(self):
        cur = self.db.cursor()
        cur.execute("""
                begin
                   for r in (select case when sysdate > next_time +interval '""" + self.interval + """' minute then 1 else 0 end flag
                             from v$archived_log 
                             where dest_id=1
                             order by first_time desc
                             fetch first 1 rows only
                            ) 
                   loop
                      if r.flag=1 then
                         execute immediate 'alter system archive log current';
                      end if;
                   end loop;
                end;
        """)

if __name__ == "__main__":
    from .standby import Standby
    res = Standby().execute_fetch_all('select level a from dual connect by level<10')
    res = list(res)[0]
    for result in res:
        print result
    #result = list(res)
    #print result
