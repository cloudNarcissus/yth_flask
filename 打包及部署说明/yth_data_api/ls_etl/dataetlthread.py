import logging

import threading
import time

from app.db.myls import mc

logger = logging.getLogger(__name__)

class dataEtlThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)

        while True:
            logger.debug("开始执行数据导入")
            print("开始执行数据导入")

            mc.job_import_ls_alarm()

            time.sleep(30)


        print("退出线程：" + self.name)



def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1