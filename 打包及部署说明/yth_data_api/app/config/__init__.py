from configswitch import get_use_consul

from app.utils.log import logger

if get_use_consul():
    from .consulconfig import Config
    logger.info("使用consul配置")
    print("使用consul配置")
else:
    from .localconfig import Config
    logger.info("使用本地配置")
    print("使用本地配置")