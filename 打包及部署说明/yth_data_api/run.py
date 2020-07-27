import argparse

from configswitch import set_use_consul
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--configpath')
args = parser.parse_args()
if args.configpath:  # 使用本地配置
    set_use_consul(False)
else:  # 使用consul
    set_use_consul(True)

from app import app

from ls_etl import dataEtlThread



if __name__ == '__main__':


    # 开启dataetl线程,处理数据ETl
    det = dataEtlThread(1, "DataETL Thread", 1)
    det.start()

    app.run(host='0.0.0.0', port=10086, debug=True)
