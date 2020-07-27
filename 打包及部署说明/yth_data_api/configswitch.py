
_USE_CONSUL = False



def set_use_consul(use_consul):
    global _USE_CONSUL
    _USE_CONSUL = use_consul


def get_use_consul():
    return _USE_CONSUL