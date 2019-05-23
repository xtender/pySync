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
# sleep interval:
WAIT_TIME_SECONDS = 1

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
    #print Primary().q_select('select 123 a, 456 b from dual').B
    Primary().print_logs()
    Primary().archive_log_current()
    Standby().download_all()
    Standby().catalog_archivelogs()
    Primary().print_logs()

def test1():
    res = Standby().execute_fetch_all('select level a from dual connect by level<10')
    res = list(res)[0]
    for result in res:
        print result[0]
    #result = list(res)
    #print result

def test2():
    #res = Primary().get_logs()
    #for archivelog in res:
    #    print archivelog.NAME
    #Standby().download_all()
    
    Standby().catalog_archivelogs()


def test3():
    print time.ctime()

def main():

    logger.info("Service started")
    #test1()
    #test2()
    #test3()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT , signal_handler)
    
    try:
        syncjob = SyncJob(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=test3)
        syncjob.start()
        while True:
            time.sleep(0.5)
        
    except ServiceExit:
        print "Service killed: running cleanup code"
        syncjob.stop()
    
    logger.info("Exiting main program")


main()