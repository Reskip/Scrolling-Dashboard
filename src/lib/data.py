#_*_coding:utf-8_*_
import pymysql
from lib.utils import *

def get_cursor(database):
    db = pymysql.connect(
        host = '222.186.190.213',
        user = 'root',
        passwd = 'lyb1092',
        db = database,
        charset='utf8'
        )
    
    cursor = db.cursor()
    return cursor

class sample(object):
    def __init__(self, date, time, score, _):
        self._score = score
        self._value = date2Stamp(date + (time if len(time) == 2 else '0' + time))

    def __repr__(self):
        return "%s\t%f\t%s" % (self._score, self._value, stamp2Date(self._value, "%Y-%m-%d %H:%M:%S"))

class stock(object):
    def __init__(self, code):
        self._code = code
        self._lst = list()
    
    def insert_score(self, s):
        try:
            self._lst.append(sample(*s))
        except:
            print("error sample: ", s)
        return
    
    def __repr__(self):
        retStr = "code: %s\n" % (self._code)
        for s in self._lst:
            retStr += str(s) + "\n"
        return retStr

def get_data(sector):
    ret = dict()
    time = list()
    cursor = get_cursor('swing_data')
    cursor.execute('''
        SELECT
            inner_code
        FROM
            sector_stock_map
        WHERE
            sector = '%s'
        ''' % (sector))
    res = cursor.fetchall()
    if len(res) < 1:
        print("ERROR: No Sector Named %s" % (sector))
    elif len(res) > 1:
        print("WARNING: More Than One Sector Named %s" % (sector))
    else:
        res = res[0][0]
        res = res.split(",")
        codeStr = ""
        for code in res:
            ret[code] = stock(code)
            if codeStr == "":
                codeStr += "\"%s\"" % (code)
            else:
                codeStr += ",\"%s\"" % (code)
        cursor = get_cursor('config')
        cursor.execute('''
            SELECT
                date,
                time,
                rng_SV,
                code
            FROM
                stockdata_1mrng
            WHERE
                code in (%s)
            ''' % (codeStr))
        dataRes = cursor.fetchall()
        for s in dataRes:
            ret[s[3]].insert_score(s)
        
        for k in ret:
            ret[k]._lst.sort(key = lambda s: s._value)
            for t in ret[k]._lst:
                if t._value not in time:
                    time.append(t._value)
        time.sort()
    return ret, time

def distinctDate(stampList):
    retSet = set()
    for s in stampList:
        retSet.add(stamp2Date(s, "%Y%m%d"))
    
    retList = list(retSet)
    retList.sort()
    return retList

if __name__ == "__main__":
    data, times = get_data('电气设备')
    print(data, times)
    print(data.keys())
    print(distinctDate(times))
