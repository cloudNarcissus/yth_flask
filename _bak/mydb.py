import config
import pymysql


class MYDB():
    conf = None

    def __init__(self, config_path):
        self.conf = config.Config(config_path)

    def _connect(self, encoding='utf8'):
        """
        连接数据库
        :param encoding:
        :return:
        """
        conn = None
        conn_err = None
        try:
            conn = pymysql.connect(
                # connect_timeout=int(self.conf.timeout),
                host=self.conf.mysql_host,
                port=int(self.conf.mysql_port),
                user=self.conf.mysql_user,
                password=self.conf.mysql_pwd,
                database=self.conf.mysql_db,
                charset=self.conf.mysql_encode
            )
            return conn, conn_err
        except pymysql.Error as e:
            conn_err = repr(e)
            # log.error(conn_err)
            return conn, conn_err

    def execute(self, proc, args=None, output_args=None):
        """
        执行SQL
        :param proc:
        :param args:
        :param output_args:
        :return:
        """
        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return err

        has_output = output_args is not None
        try:
            sql = 'call ' + proc

            cur = conn.cursor()
            cur.execute(sql, args) if args is not None else cur.execute(sql)
            # 这句需要写到最后  不然前一句不能取不到输出参数
            conn.commit()
            if has_output:
                # sql.insert(0, self._build_output_param(output_args))
                cur.execute(self._build_output_query(output_args))

            data = self.parse_data(cur)
            return data[0] if data is not None and len(data) > 0 else None
        except Exception as e:
            err = self._get_exception_msg(e)
            return err

        finally:
            cur.close()
            conn.close()

    def execute_sql(self, sql):
        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return err
        try:

            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            return 0
        except Exception as e:
            err = self._get_exception_msg(e)
            return -1

        finally:
            cur.close()
            conn.close()

    def insert_many(self, sql, tuples):
        """
        执行SQL(批量插入)
        :param sql:
        :param tuples:元组列表[(),()]
        :return:
        """
        if len(tuples) < 1:
            return -1

        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return err

        try:
            sql += 'values(' + ('%s,' * len(tuples[0]))[:-1] + ')'  # 构造(%s,%s,...)
            cur = conn.cursor()
            cur.executemany(sql, tuples)
            conn.commit()
            return 0
        except Exception as e:
            err = self._get_exception_msg(e)
            return err

        finally:
            cur.close()
            conn.close()

    def insert_many_dumplicate(self, sql, tuples, dump_keys):
        """
        执行SQL(批量插入)带去重
        :param sql:
        :param tuples:元组列表[(),()]
        :param dump_key：发生重复的时候，需要替换的值(是一个元组)
        :return:
        """
        if len(tuples) < 1 or len(dump_keys) < 1:
            return -1

        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return err

        try:
            #sql += 'values'
            #tuples = map(lambda x: '(' + ','.join(map(lambda y: "'" + y + "'", x)) + ')', tuples)
            #sql += ','.join(tuples)

            sql +='values(' + ('%s,' * len(tuples[0]))[:-1] + ')'  # 构造(%s,%s,...)

            dumpupdate = ' on duplicate key update '
            for col in dump_keys:
                if col == 'count_':
                    dumpupdate += 'count_ = count_+values(count_),'
                else:
                    dumpupdate += '%s = values(%s),' % (col, col)
            sql += dumpupdate[:-1]
            print(sql)

            cur = conn.cursor()
            cur.executemany(sql, tuples)
            #cur.execute(sql)
            conn.commit()
            return 0
        except Exception as e:
            err = self._get_exception_msg(e)
            return err

        finally:
            cur.close()
            conn.close()

    def query(self, proc, args=None, output_args=None, prefix=''):
        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return err
        conn.autocommit(True)
        has_output = output_args is not None
        try:
            sql = ['call ' + proc]
            if has_output:
                sql.insert(0, self._build_output_param(output_args))
                sql.append(self._build_output_query(output_args))

            sql = '\n'.join(sql)

            cur = conn.cursor()
            cur.execute(sql, args) if args is not None else cur.execute(sql)
            return self.parse_data(cur,prefix)
        except Exception as e:
            err = self._get_exception_msg(e)
            return err

        finally:
            cur.close()
            conn.close()

    def query_sql(self, sql, prefix='a.'):
        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return err
        conn.autocommit(True)

        try:
            cur = conn.cursor()
            cur.execute(sql)
            return self.parse_data(cur, prefix)
        except Exception as e:
            err = self._get_exception_msg(e)
            return err

        finally:
            cur.close()
            conn.close()

    # 把查询出来的数据搞成  列表->字典 结构
    def parse_data(self, cur, prefix='a.'):
        result = []
        data = []

        if cur.description is not None:
            columns = [None if desc is None or not desc or len(desc) == 1 else desc[0] for desc in
                       cur.description]
            for row in cur:
                temp = dict()
                for i in range(len(columns)):
                    val = row[i]
                    # ignore None value, otherwise you'll get a 'None' string
                    if val is not None:
                        val = str(val)
                    key = prefix + columns[i]
                    temp[key] = val
                data.append(temp)
            result.append(data)

        return result[0] if len(result) == 1 else result

    def _build_output_param(self, output_args):
        temp = []
        for name in output_args:
            temp.append('declare @{name} {type}'.format(name=name, type=output_args[name]))

        return '\n'.join(temp)

    def _build_output_query(self, output_args):
        temp = []
        for name in output_args:
            temp.append('@{name} as {name}'.format(name=name))

        return 'select ' + str.join(',', temp)

    def _get_exception_msg(self, e):

        if len(e.args) < 2:
            err = 'unknown db error'
            return err
        msg = e.args[1]
        idx = msg.find('DB-Lib')
        if idx != -1:
            msg = msg[0:idx]
        err = msg
        return err

    def handle_connect_err(self, conn_err):
        msg = conn_err
        print('无法连接到数据库: {err}'.format(err=msg))
        return msg

# 测试
# if __name__ == '__main__':
#     mydb = MYDB()
#     sql = 'select * from help_topic'
#     mydb.query(sql)
