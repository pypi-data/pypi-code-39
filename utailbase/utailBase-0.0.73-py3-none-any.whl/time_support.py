# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import maya
from time import mktime

from bs4 import BeautifulSoup
import requests

def timeOffset(localDateTime, offsetMinutes = -540, offsetSecs = 0):
    lts = int(mktime(localDateTime.timetuple())) + int(offsetMinutes * 60) + int(offsetSecs)
    return datetime.fromtimestamp(lts)


def toDt(dateStr:str) -> datetime:
    # try:
        return maya.parse(dateStr).datetime()
    # except Exception:
    #     print('error! test')
    #     quit(1)


# dateStr( ex> 14:14. 금일 0시 0분. 한국시간 ) 
# return : datetime(UTC)
def korDatedateHM_toUTC(dateStr):
    timeSplits = dateStr.split(':')
    nowKor = datetime.utcnow() + timedelta(hours=9)
    outTime = nowKor.replace( hour=int(timeSplits[0]), minute=int(timeSplits[1]), second=0, microsecond=0)
    return timeOffset(outTime)


def _win_set_time(time_tuple):
    pass
    # import pywin32
    # # http://timgolden.me.uk/pywin32-docs/win32api__SetSystemTime_meth.html
    # # pywin32.SetSystemTime(year, month , dayOfWeek , day , hour , minute , second , millseconds )
    # dayOfWeek = datetime.datetime(time_tuple).isocalendar()[2]
    # pywin32.SetSystemTime( time_tuple[:2] + (dayOfWeek,) + time_tuple[2:])

def _linux_set_time(time_tuple):
    import ctypes
    import ctypes.util
    import time

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int( time.mktime( datetime( *time_tuple[:6]).timetuple() ) )
    ts.tv_nsec = time_tuple[6] * 1000000 # Millisecond to nanosecond

    # http://linux.die.net/man/3/clock_settime
    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))


def _syncTimeFrom_timeanddate(log):
    responseDate = requests.request('GET', 'http://free.timeanddate.com/clock/i4ii3urt/n235/tlkr47/fs20/tct/pct/tt1/tw0/tm3/td2', timeout=15)
    if 200 != responseDate.status_code:
        return None
    responseTime = requests.request('GET', 'http://free.timeanddate.com/clock/i4ii3urt/n235/fs20/tct/pct/ta1', timeout=15)
    if 200 != responseTime.status_code:
        return None

    try:
        dateStr = BeautifulSoup( responseDate.content, 'html.parser').find('span', {'id': 't1'}).get_text() + ' ' + BeautifulSoup( responseTime.content, 'html.parser').find('span', {'id': 't1'}).get_text()

        print(dateStr)

        currentTime = toDt(dateStr)
        currentTime = timeOffset(currentTime)
    except Exception as inst:
        log.error('failed syncTime(ewha). err:{}'.format(inst.args))
        return None

    return currentTime


def timeSyncNTP(log, platform):
    if not platform.startswith('linux'):
        return

    log.info('start syncTime for LINUX by NTP')

    import ntplib
    from time import ctime
    from datetime import datetime
    
    c = ntplib.NTPClient()
    # r = c.request('kr.pool.ntp.org', version=3)
    try:
        r = c.request('europe.pool.ntp.org', version=3)
        dt = datetime.fromtimestamp(r.tx_time)

    except ntplib.NTPException as inst:
        log.error('failed timeSync(timed-out). msg:{}'.format(inst.args))
        return

    log.info('current time(prev sync): {}'.format(datetime.now() ) )
    _linux_set_time(dt.timetuple())
    log.info('current time(after sync): {}'.format(datetime.now() ) )


def timeSyncHttp(log):
    dt = _syncTimeFrom_timeanddate(log)

    if dt is None:
        log.error('failed timeSync(by Http).')
        return


    log.info('current time(prev sync): {}'.format(datetime.now() ) )
    _linux_set_time(dt.timetuple())
    log.info('current time(after sync): {}'.format(datetime.now() ) )
