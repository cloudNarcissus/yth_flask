import redis



if __name__ == '__main__':
    r = redis.StrictRedis(host='192.168.40.163', port=6379,db=0)
    r.set('name', 'zhangsan')   #添加
    print (r.get('name'))   #获取