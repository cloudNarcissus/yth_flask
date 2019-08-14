from app import app
from ls_etl import dataEtlThread

if __name__ == '__main__':

    # 开启dataetl线程,处理数据ETl
    det = dataEtlThread(1, "DataETL Thread", 1)
    det.start()


    app.run(host='0.0.0.0', port=10086,debug=True)
