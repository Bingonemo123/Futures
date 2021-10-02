from iqoptionapi.stable_api import IQ_Option
import datetime
import logging.handlers
import logging
import time
import sys
import os
import pathlib
import pickle
connector =IQ_Option("levanmikeladze123@gmail.com","591449588")
connector.connect()

'''----------------------------------------------------------------------------------------------'''
if os.name == 'posix':
    path = pathlib.PurePosixPath(os.path.abspath(__file__)).parent
else:
    path = pathlib.PureWindowsPath(os.path.abspath(__file__)).parent

'''----------------------------------------------------------------------------------------------'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
"""StreamHandler"""
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG) 
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
"""FileHandler"""
rotatingfile_handler = logging.handlers.RotatingFileHandler(path/'demomain.log', backupCount=5, maxBytes=1073741824)
rotatingfile_handler.setLevel(logging.INFO)
rotatingfile_handler.setFormatter(formatter)
logger.addHandler(rotatingfile_handler)
#----------------------------------------------------------------------------#
connector.change_balance("PRACTICE")
instrument_type="digital"
side="buy"
type_market="market"
limit_price=None 
stop_price=None 
stop_lose_kind=None 
stop_lose_value=None 
take_profit_kind='percent' 
take_profit_value=6
use_trail_stop=False 
auto_margin_call=True 
use_token_for_commission=False 
#----------------------------------------------------------------------------#
def get_custom_balance(timeout = 60):
    connector.api.balances_raw = None
    connector.api.get_balances()
    stt = time.time()
    while connector.api.balances_raw == None and time.time() - stt < timeout:
        pass
    if connector.api.balances_raw == None:
        return None
    for balance in connector.api.balances_raw["msg"]:
            if balance["id"] == connector.get_balance_id():
                return balance["amount"]

logger.info('Start')
while True:
    try:
        try:
            data = pickle.load(open('demo_data.pkl', 'rb'))
        except:
            data = []
            pickle.dump(data, open('demo_data.pkl', 'bw'))

        logger.debug('w1')
        while True:
            if connector.check_connect() == False:
                check,reason=connector.connect()
            else:
                break
        logger.debug('uw1')

        balance = get_custom_balance()
        if balance == None:
            continue
        logger.debug(str(balance)+'$')
        
        ALL_Asset=connector.get_all_open_time()

        open_digits = [x for x in ALL_Asset[instrument_type] if ALL_Asset[instrument_type][x].get('open')]
        found_s = []
        for i in range(5):
        
            checklist = []
            for f in open_digits:
                balance = get_custom_balance()
                if balance == None:
                    continue
                connector.start_candles_stream(f[:6], 5, 600)
                candles = list(connector.get_realtime_candles(f[:6], 5).values())
                s = sum([1 for c in candles if c.get('close') > candles[-1].get('close')])
                if s not in found_s:
                    found_s.append(s)
                recept = {
                            "98": "put",
                            "99": "call",
                            "129": "put",
                            "156": "call",
                            "206": "call",
                            "213": "put",
                            "220": "put",
                            "227": "put",
                            "238": "put",
                            "250": "put",
                            "266": "put",
                            "316": "put",
                            "330": "call",
                            "345": "put",
                            "370": "put",
                            "401": "put",
                            "409": "put",
                            "427": "put",
                            "482": "call",
                            "483": "put"
                            }
                if str(s) in recept:
                    var_1 = 10000
                    if balance < 1 or datetime.datetime.now().hour == 0:
                        connector.reset_practice_balance()
                    if balance % var_1 >= var_1/2 or balance < var_1:
                        bit = balance % var_1
                    else:
                        bit = var_1
                    partition = 5
                    if bit/partition < 1:
                        bit = 1
                    elif bit/partition > 20000:
                        bit = 20000
                    else:
                        bit = bit/partition
                    check, id = connector.buy_digital_spot(f, bit, recept[str(s)], 1)
                    if check == True:
                        checklist.append((id,s))
                        balance = get_custom_balance()
                        if balance == None:
                            continue
                        logger.info(recept[str(s)] + ' on ' + f + ' ' + str(id) + ' ' + str(s) + ' ' + str(balance)+'$')
            for chl in checklist:
                sst = time.time()
                while time.time() - sst < 120:
                    check, win = connector.check_win_digital_v2(chl[0])
                    if check == True:
                        data.append(((win > 0), chl[1]))
                        break
            if len(checklist) > 0:
                logger.info(checklist)
        pickle.dump(data, open('demo_data.pkl', 'bw'))
        logger.debug(len(data))
        logger.debug(found_s)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.exception(str(e))
        logger.exception([exc_type, fname, exc_tb.tb_lineno])
        time.sleep(60*3)
