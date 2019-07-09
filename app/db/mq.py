import json
import pika

from app.config import Config


class MqConnect(object):
    def __init__(self):
        self.mq_credentials = pika.PlainCredentials(Config.mq_user, Config.mq_pwd)
        self.mq_conn_params = pika.ConnectionParameters(host=Config.mq_host, port=Config.mq_port,
                                                        credentials=self.mq_credentials, heartbeat=0)
        self.mq_conn = pika.BlockingConnection(parameters=self.mq_conn_params)
        self.mq_channel = self.mq_conn.channel()

    def send_msg(self,mq_msg):
        self.mq_channel.basic_publish(exchange='main', routing_key='keyword_rule_update',
                                      body=json.dumps(mq_msg, ensure_ascii=False))

mq = MqConnect()


# 1.连接到MQ
# mq_credentials = pika.PlainCredentials(config.mq_user, config.mq_pwd)
# mq_conn_params = pika.ConnectionParameters(host=config.mq_host, port=config.mq_port,
#                                            credentials=mq_credentials, heartbeat=0)
# mq_conn = pika.BlockingConnection(parameters=mq_conn_params)
# mq_channel = mq_conn.channel()
#
# # 2.发送消息
# mq_channel.basic_publish(exchange='main', routing_key='keyword_rule_update',
#                          body=json.dumps(mq_msg, ensure_ascii=False))
