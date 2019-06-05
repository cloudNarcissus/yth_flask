import inspect
from functools import wraps


def addHead():
    """
    装饰器：添加error头部
    :return:
    """

    def invoke_addHead(func):
        @wraps(func)
        def addhead(self, params=None):
            params = inspect.getfullargspec(func)

            try:
                if len(params) == 1:
                    success, result = func(self)
                elif len(params) == 2:
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
