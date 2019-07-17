import logging

import happybase

from app.config import Config


logger = logging.getLogger(__name__)


class HbaseConnect(object):
    def __init__(self):
        self.log = logger

        try:
            self.hb_pool = happybase.ConnectionPool(size=5,host=Config.hb_hosts,port=Config.hb_port,table_prefix='wdp',autoconnect=True,)
        except Exception as e:
            self.hb_pool = None
            self.log.error('hb_pool init failed,%s' % str(e))

    def get_conn(self):
        if self.hb_pool is not None:
            conn = hbc.hb_pool.connection()
        else:
            try:
                conn = happybase.Connection(host=Config.hb_hosts, port=Config.hb_port, autoconnect=True)
            except Exception as e:
                conn = None
                self.log.error('happybase.Connection failed,%s' % str(e))
        return conn

    def dowmload_wdp_files(self, params):
        """
        下载hbase中的文件
        :param params: __md5
        :return: 
        """
        md5 = params.get('__md5')
        content = b''

        try:
            with self.get_conn() as conn:
                files = conn.table(b'files')
                row = files.row(md5)

                seg_count = int(row[b'info:seg_count'])
                filename = row[b'info:filename']

                for i in range(0, seg_count):
                    column_name = bytes("content:content" + str(i),encoding="utf8")
                    content += row[column_name]

        except Exception as e:
            self.log.debug(u'获取文件<Md5:%s>失败,因conn异常:%s', md5, e)
            return False,str(e)

        return True , {"filename" : filename , "content" : content}


hbc = HbaseConnect()

