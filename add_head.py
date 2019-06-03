
from functools import wraps

def addHead():
    """
    装饰器：添加error头部
    :return:
    """

    def invoke_addHead(func):
        @wraps(func)
        def addhead(request):
            success, result = func(request)
            if success:
                data = {
                    'err': None,
                    'data': result
                }
            else:
                data = {
                    'err': result,
                    'data': None
                }

            return data
        return addhead

    return invoke_addHead