import calendar
import inspect
from functools import wraps

import datetime


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


def yestoday():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=-1)
    yestoday = now + delta
    return yestoday.strftime('%Y-%m-%d')

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

if __name__ == '__main__':

    print(firstdayofmonth())
