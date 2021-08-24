from iqoptionapi.stable_api import IQ_Option
# import Internet_protocols
import logging.handlers
import datetime
import pathlib
import logging
import time
import sys
import os
import pickle
connector =IQ_Option("ww.bingonemo@gmail.com","JF*#3C5va&_NDqy")
connector.connect()
'''----------------------------------------------------------------------------------------------'''
if os.name == 'posix':
    path = pathlib.PurePosixPath(os.path.abspath(__file__)).parent 
    if 'Forex_experiments' in path.parts:
        path = path.parent / str(datetime.date.today())
    else:
        path = path / 'Forex_experiments'  / str(datetime.date.today())
    # After this, path is equals to current date folder
    file_path = pathlib.PurePosixPath(os.path.abspath(__file__))
else:
    path = pathlib.PureWindowsPath(os.path.abspath(__file__)).parent 
    if 'Forex_experiments' in path.parts:
        path = path.parent / str(datetime.date.today())
    else:
        path = path / 'Forex_experiments'  / str(datetime.date.today())
    # After this, path is equals to current date folder
    file_path = pathlib.PureWindowsPath(os.path.abspath(__file__))
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
rotatingfile_handler = logging.handlers.RotatingFileHandler(path.parent/'main.log', backupCount=5, maxBytes=1073741824)
rotatingfile_handler.setLevel(logging.DEBUG)
rotatingfile_handler.setFormatter(formatter)
logger.addHandler(rotatingfile_handler)
#----------------------------------------------------------------------------#
connector.change_balance("PRACTICE")
instrument_type="digital"
side="buy"
type="market"
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
            number = pickle.load(open('number.pkl', 'rb'))
        except:
            number = (0,0)
            pickle.dump(number, open('number.pkl', 'bw'))
        logger.info('while #1')
        while True:
            if connector.check_connect() == False:
                check,reason=connector.connect()
            else:
                break
        logger.info('unwhile #1')
        balance = connector.get_balance()
        logger.info(str(balance)+'$')
        ALL_Asset=connector.get_all_open_time()

        open_digits = [x for x in ALL_Asset[instrument_type] if ALL_Asset[instrument_type][x].get('open')]

        for i in range(5):
        
            checklist = []
            for f in open_digits:
                check, id = connector.buy_digital_spot(f, 1, 'call', 1)
                if check == True:
                    checklist.append(id)

            for chl in checklist:
                while True:
                    check, win = connector.check_win_digital_v2(chl)
                    if check == True:
                        number = (number[0] + (win > 0), number[1] + 1)
                        break

        pickle.dump(number, open('number.pkl', 'bw'))
        logger.info(number)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.exception(str(e))
        logger.exception([exc_type, fname, exc_tb.tb_lineno])
        raise Exception(str(e))
        time.sleep(60*3)
