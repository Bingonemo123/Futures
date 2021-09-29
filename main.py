from iqoptionapi.stable_api import IQ_Option
# import Internet_protocols
import logging.handlers
import logging
import time
import sys
import os
import json
connector =IQ_Option("ww.bingonemo@gmail.com","JF*#3C5va&_NDqy")
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
rotatingfile_handler = logging.handlers.RotatingFileHandler('main.log', backupCount=5, maxBytes=1073741824)
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
            data = json.load(open('data.json', 'r'))
        except:
            data = []
            json.dump(data, open('data.json', 'w'))
        logger.info('w1')
        while True:
            if connector.check_connect() == False:
                check,reason=connector.connect()
            else:
                break
        logger.info('uw1')
        
        ALL_Asset=connector.get_all_open_time() # loop warning

        open_digits = [x for x in ALL_Asset[instrument_type] if ALL_Asset[instrument_type][x].get('open')]

        for i in range(5):
        
            checklist = []
            for f in open_digits:
                # connector.start_candles_stream(f[:6], 5, 600) # loop warning
                # candles = list(connector.get_realtime_candles(f[:6], 5).values())

                # Exams
                buying_time = time.time()
                # Exams

                check, id = connector.buy_digital_spot(f, 1, 'call', 1)
                if check == True:
                    checklist.append((id, buying_time)) # add exam

            for chl in checklist:
                sst = time.time()
                while time.time() - sst < 120:
                    check, win = connector.check_win_digital_v2(chl[0])
                    if check == True:
                        position_id = connector.get_digital_position(chl[0]).get('msg').get('position').get('id')
                        data.append({'Outcome' : (win > 0),
                                     'Id' : chl[0],
                                     'Buying_time': chl[1],
                                     'Closing_time': time.time(),
                                     'Position_Id': position_id
                                    }) # add exam
                        break
            logger.info(checklist)
        json.dump(data, open('data.json', 'w'))
        logger.info(len(data))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.exception(str(e))
        logger.exception([exc_type, fname, exc_tb.tb_lineno])
        time.sleep(60*3)
