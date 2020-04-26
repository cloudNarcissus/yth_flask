self.conn = pymysql.connect(
          connect_timeout=int(self.conf.timeout),
          host=self.conf.host,
          port=int(self.conf.port),
          user=self.conf.user,
          password=self.conf.pswd,
          database=self.conf.name,
          charset=encoding
      )
      self.cur = self.conn.cursor() 
      
      self.cur.execute(sql, args) 
      
       self.cur.close()
      self.conn.close()
      
      
          def parse_data(self):
        result = []

        data = []
        if self.cur.description is not None:
            columns = [None if desc is None or not desc or len(desc) == 1 else desc[0] for desc in
                       self.cur.description]
            for row in self.cur:
                temp = dict()
                for i in range(len(columns)):
                    val = row[i]
                    # ignore None value, otherwise you'll get a 'None' string
                    if val is not None:
                        val = str(val)
                    temp[columns[i]] = val
                data.append(temp)
            result.append(data)

        return result[0] if len(result) == 1 else result