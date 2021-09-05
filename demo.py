from iqoptionapi.stable_api import IQ_Option
import datetime
import logging.handlers
import logging
import time
import sys
import os
import pickle
connector =IQ_Option("levanmikeladze123@gmail.com","591449588")
connector.connect()

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
rotatingfile_handler = logging.handlers.RotatingFileHandler('demomain.log', backupCount=5, maxBytes=1073741824)
rotatingfile_handler.setLevel(logging.DEBUG)
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
while True:
    try:

        try:
            data = pickle.load(open('demo_data_{0}.pkl'.format(str(datetime.date.today())), 'rb'))
        except:
            data = []
            pickle.dump(data, open('demo_data_{0}.pkl'.format(str(datetime.date.today())), 'bw'))


        logger.info('w1')
        while True:
            if connector.check_connect() == False:
                check,reason=connector.connect()
            else:
                break
        logger.info('uw1')

        balance = connector.get_balance()
        logger.info(str(balance)+'$')
        
        ALL_Asset=connector.get_all_open_time()

        open_digits = [x for x in ALL_Asset[instrument_type] if ALL_Asset[instrument_type][x].get('open')]

        for i in range(5):
        
            checklist = []
            for f in open_digits:
                balance = connector.get_balance()
                connector.start_candles_stream(f[:6], 5, 600)
                candles = list(connector.get_realtime_candles(f[:6], 5).values())
                s = sum([1 for c in candles if c.get('close') > candles[-1].get('close')])
                recept = {99: 'call', 156: 'call', 206: 'call', 213: 'put', 238:'put', 266:'put', 316:'put', 330:'call', 482:'call'}
                if s in recept:
                    check, id = connector.buy_digital_spot(f, balance/2, recept[s], 1)
                    if check == True:
                        checklist.append((id,s))
                        balance = connector.get_balance()
                        logger.info(recept[s] + ' on ' + f + ' ' + str(id) + ' ' + str(s) + ' ' + str(balance)+'$')
            for chl in checklist:
                sst = time.time()
                while time.time() - sst < 120:
                    check, win = connector.check_win_digital_v2(chl[0])
                    if check == True:
                        data.append(((win > 0), chl[1]))
                        break
            logger.info(checklist)
        pickle.dump(data, open('demo_data_{0}.pkl'.format(str(datetime.date.today())), 'bw'))
        logger.info(len(data))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.exception(str(e))
        logger.exception([exc_type, fname, exc_tb.tb_lineno])
        time.sleep(60*3)
