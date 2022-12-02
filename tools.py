import pandas as pd
import sys
import time
import redis
r = redis.Redis(host = 'localhost', port = 6379, db = 0, password = 'demaxiya')

def read_excel(f):
    try:
        dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        data = pd.read_excel(f, dtype = str).fillna("0")
        for index, row in data.iterrows():
            stu = row.tolist()[0]
            ky = f"polygon_{stu}"
            #print(row)
            detail = '|'.join([dt] + row.tolist())
            print(detail)
            r.lpush(ky, detail) 
        return True
    except Exception as e:
        raise e
        return False

if __name__ == '__main__':
    name = sys.argv[1]
    read_excel(name)
