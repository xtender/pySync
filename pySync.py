import logging
import logging.config
import threading, time, signal

from datetime import timedelta


from helpers.config import Config
from helpers.xtoracle import *
from helpers.standby import *
from helpers.primary import *
from helpers.syncjob import *

# logging:
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger("pySync")

####################################################
# Exception for service stop
class ServiceExit(Exception):
    pass

def signal_handler(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

####################################################

def testConfig():
    cfg_name='standby'
    with Config(r'config.cfg') as cfg:
        print cfg.get(cfg_name,'username')

def sync_standby():
    Primary().archive_log_current()
    Primary().print_logs()
    logs_number = Standby().download_all()
    if logs_number>0:
        Standby().catalog_archivelogs()
    else:
        mlog.info("There is no new logs on Primary. Last sequence on Primary: {}".format(Primary().get_last_log()))
    Primary().print_logs()

def test1():
    print Primary().q_select('select database_role from v$database').DATABASE_ROLE
    
    #res = Standby().q_select('select level a from dual connect by level<10')
    #for result in res:
    #    print result[0]
    

def test2():
    #res = Primary().get_logs()
    #for archivelog in res:
    #    print archivelog.NAME
    #Standby().download_all()
    
    Standby().catalog_archivelogs()


def test3():
    print time.ctime()
    print Standby().get_last_log()
    print Standby().get_last_applied_log()

def main():

    logger.info("Service started")
    #test1()
    #test2()
    #test3()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT , signal_handler)
    with Config(r'config.cfg') as cfg:
        SYNC_CHECK_WAIT_TIME_SECONDS = cfg.getint('main', 'SYNC_CHECK_WAIT_TIME_SECONDS')
    
    try:
        #syncjob = SyncJob(interval=timedelta(seconds=SYNC_CHECK_WAIT_TIME_SECONDS), execute=test3)
        syncjob = SyncJob(interval=timedelta(seconds=SYNC_CHECK_WAIT_TIME_SECONDS), execute=sync_standby)
        syncjob.start()
        while True:
            time.sleep(0.5)
        
    except ServiceExit:
        print "Service killed: running cleanup code"
        syncjob.stop()
    
    logger.info("Exiting main program")


main()