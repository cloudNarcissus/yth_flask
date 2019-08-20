from configswitch import get_use_consul


if get_use_consul():
    from .consulconfig import Config

    print("使用consul配置")
else:
    from .localconfig import Config

    print("使用本地配置")