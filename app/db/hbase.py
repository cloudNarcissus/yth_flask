import logging

import happybase

from app.config import Config


logger = logging.getLogger(__name__)


class HbaseConnect(object):
    def __init__(self):
        self.hb_pool = happybase.ConnectionPool(size=5,host=Config.hb_hosts,table_prefix='wdp')
        self.log = logger

    def dowmload_wdp_files(self, params):
        """
        下载hbase中的文件
        :param params: __md5
        :return: 
        """
        md5 = params.get('__md5')
        content = b''

        try:
            with hbc.hb_pool.connection() as conn:
                files = conn.table(b'files')
                row = files.row(md5)

                seg_count = int(row[b'info:seg_count'])
                filename = row[b'info:filename']

                for i in range(0, seg_count):
                    column_name = bytes("content:content" + str(i),encoding="utf8")
                    content += row[column_name]

        except Exception as e:
            self.log.error(u'获取文件<Md5:%s>失败,%s', md5, e)
            return False,str(e)

        return True , {"filename" : filename , "content" : content}


hbc = HbaseConnect()

