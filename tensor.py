import json
import tqdm
import functools
from threading import Thread
import os 
import pandas as pd

from iqoptionapi.stable_api import IQ_Option
connector =IQ_Option("ww.bingonemo@gmail.com","JF*#3C5va&_NDqy")
connector.connect()

real_data = json.load(open("data.json", 'r'))

def timeout(timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception as je:
                print ('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco

@timeout(120)
def custom_candles (a, b, c, d):
    return list(connector.get_candles(a, b, c, d))

last_position_id = 14246305191
skip=False

for r in tqdm.tqdm(real_data):
    if r.get('Position_Id') != None:
        if r.get('Position_Id') == last_position_id:
            skip = True
            continue

        if skip:
            while True:
                if connector.check_connect() == False:
                    check,reason=connector.connect()
                else:
                    break
            h = connector.get_digital_position_by_position_id(r.get('Position_Id'))

            opening_time = h.get('msg').get('position').get('open_quote_time_ms')
            candles = list(connector.get_candles(h.get('msg').get('position').get('instrument_underlying')[:6], 5, 600, opening_time/1000))
            r['Candles'] = candles
            df = pd.DataFrame.from_dict(r, orient='index', columns=['Data'])

            # if file does not exist write header 
            if not os.path.isfile('Json/tensordata.csv'):
                df.to_csv('Json/tensordata.csv', header='column_names')
            else: # else it exists so append without writing the header
                df.to_csv('Json/tensordata.csv', mode='a', header=False, chunksize=10000)


