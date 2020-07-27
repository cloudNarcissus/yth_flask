
import logging

import happybase

from app.config import Config
from app.utils.common import addHead


logger = logging.getLogger(__name__)


class HbaseConnect(object):
    def __init__(self):
        self.log = logger

        # try:
        #     self.hb_pool = happybase.ConnectionPool(size=5,host=Config.hb_hosts,port=Config.hb_port,table_prefix='wdp',autoconnect=True,)
        # except Exception as e:
        #     self.hb_pool = None
        #     self.log.error('hb_pool init failed,%s' % str(e))

    def get_conn(self):
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
        conn = self.get_conn()
        if conn is None:
            self.log.error(u'hbase 连接失败')
            return False, 'hbase 连接失败'

        self.log.debug(u'开始下载文件:%s', md5)
        try:
            files = conn.table(b'wdp_files')
            row = files.row(md5)
            seg_count = int(row[b'info:seg_count'])
            filename = row[b'info:filename']

            for i in range(0, seg_count):
                column_name = bytes("content:content" + str(i),encoding="utf8")
                content += row[column_name]

        except Exception as e:
            self.log.error(u'获取文件<Md5:%s>失败,因conn异常:%s', md5, e)
            return False,str(e)
        finally:
            if conn is not None:
                conn.close()

        return True , {"filename" : filename , "content" : content}

    @addHead()
    def upload_wdp_files(self, params):
        """
        上传文件到hbase
        :param params: 
        :return: 
        """
        conn = self.get_conn()
        if conn is None:
            self.log.error(u'hbase 连接失败')
            return False, 'hbase 连接失败'

        try:
            table = conn.table(b'wdp_files')

            filename = params.get('filename')
            type = params.get('__type')
            md5 = params.get('__md5')
            content = params.get('content')

            seg_count = 0
            columns = {
                b'info:filename': filename,
                b'info:type': str(type)
            }
            seg_size = 512 * 1024  #分区大小
            remain_size = seg_size #初始化剩下待读的大小
            while remain_size == seg_size:
                content = content.read(seg_size)
                remain_size = len(content)
                column_name = "content:content" + str(seg_count)
                columns[column_name] = content
                seg_count += 1

            columns[b'info:seg_count'] = str(seg_count)
            columns[b'info:size'] = str(seg_size*(seg_count-1)+remain_size)

            table.put(md5, columns)
            return True,"上传成功"

        except Exception as e:
            self.log.error(u'上传文件<%s>失败:%s', filename, e)
            return False,str(e)
        finally:
            if conn is not None:
                conn.close()

    @addHead()
    def getinfo_wdp_files(self, params):
        """
        获取文件信息（包括 文件名、size、type， 但不包含文件本体或文件流）
        :param params: __md5
        :return: 
        """
        md5 = params.get('__md5')
        conn = self.get_conn()
        if conn is None:
            self.log.error(u'hbase 连接失败')
            return False, 'hbase 连接失败'

        try:
            table = conn.table(b'wdp_files')
            row = table.row(md5,columns=[b"info:filename",b"info:type",b"info:size"])
            row_str = {}
            for key in row:
                row_str[bytes.decode(key)]=bytes.decode(row[key])

            return True,row_str
        except Exception as e:
            self.log.error(u'查询文件%s的信息失败:%s', md5, e)
            return False,str(e)
        finally:
            if conn is not None:
                conn.close()



hbc = HbaseConnect()

