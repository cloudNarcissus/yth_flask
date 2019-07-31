import calendar
import inspect
from functools import wraps

import datetime
import time

def addHead():
    """
    装饰器：添加error头部
    :return:
    """

    def invoke_addHead(func):
        @wraps(func)
        def addhead(self, params=None):
            params_ = inspect.getfullargspec(func)[0]

            try:
                if len(params_) == 1:
                    success, result = func(self)
                elif len(params_) == 2:
                    success, result = func(self, params)
            except Exception as e:
                success = False
                result = str(e)

            if success:
                data = {
                    'message': None,
                    'data': result
                }
            else:
                data = {
                    'message': result,
                    'data': None
                }

            return data

        return addhead

    return invoke_addHead



def today():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d')


def yesterday():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=-1)
    yesterday = now + delta
    return yesterday.strftime('%Y-%m-%d')

def monday():
    now = datetime.datetime.now()
    oneday = datetime.timedelta(days = 1)

    m1 = calendar.MONDAY

    while now.weekday() != m1:
        now -= oneday

    monday = now.strftime('%Y-%m-%d')

    return monday

def firstdayofmonth():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-01')


def diffday(begin_day,end_day):
    """
    计算后者减去前者相差的天数
    :param begin_day: 形如2019-07-09的字符串
    :param end_day: 同上
    :return: int
    """
    date1 = time.strptime(begin_day, "%Y-%m-%d")
    date2 = time.strptime(end_day, "%Y-%m-%d")
    #根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推
    date1 = datetime.datetime(date1[0],date1[1],date1[2])
    date2 = datetime.datetime(date2[0],date2[1],date2[2])
    # 返回两个变量相差的值，就是相差天数
    return (date2 - date1).days



def isIP(str):
    import re
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False


def isMac(str):
    import re
    if re.match(r"(([a-f0-9]{2}:)|([a-f0-9]{2}-)){5}[a-f0-9]{2}", str,re.IGNORECASE):
        return True
    return False


def del_teshu_char(str):
    newstr = ''
    for i in str:
        if ord(i) not in (ord('!'),ord('^'),ord('('),ord(')'),ord('~'),ord('-'),ord('+'),ord('"'),ord('\'')):
            newstr += i
    return newstr


if __name__ == '__main__':

    print(del_teshu_char("^192.1~~68.(0).1"))

