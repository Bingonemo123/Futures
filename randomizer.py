from multiprocessing import Process, Value
import log_protocols
logger = log_protocols.Archlog
path = log_protocols.Archpath

    
def that():

    from iqoptionapi.stable_api import IQ_Option
    import datetime
    import time
    import sys
    import os
    import json
    import log_protocols
    from threading import Thread
    import functools

    connector =IQ_Option("levanmikeladze123@gmail.com","591449588")
    connector.connect()

    '''----------------------------------------------------------------------------------------------'''
    logger = log_protocols.Archlog
    path = log_protocols.Archpath    
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

    #----------------------------------------------------------------------------#
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
    def custom_candles (f):
        connector.start_candles_stream(f[:6], 5, 600)
        candles = list(connector.get_realtime_candles(f[:6], 5).values())
        return candles
    #----------------------------------------------------------------------------#



    logger.debug('Start')
    # while True:
    for one in [True]:
        try:
            if datetime.datetime.now().minute == 0:
                logger.info('Hour remainder ' + str(datetime.datetime.now().hour))
             
            # if datetime.datetime.now().hour > 6 and datetime.datetime.now().hour < 23:
            #     if get_custom_balance() < 10000:
            #         connector.reset_practice_balance()
            #         logger.info('Balance reset')
            #     time.sleep(10* 60)
            #     continue

            try:
                data = json.load(open(path/'r_data.json', 'r'))
            except:
                data = []
                json.dump(data, open(path/'r_data.json', 'w'))

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
                    # if f[-3:] != 'OTC':
                    #     continue
                    balance = get_custom_balance()
                    if balance == None:
                        continue
                    try:
                        candles = custom_candles(f)
                    except:
                        continue
                    s = sum([1 for c in candles if c.get('close') > candles[-1].get('close')])
                    if s not in found_s:
                        found_s.append(s)
                    recept = {98: "put",129: "put",156: "call",206: "call",213: "put",220: "put",227: "put",99: "call",238: "put",266: "put",316: "put",330: "call",345: "put",370: "put",409: "put",250: "put",427: "put",482: "call",483: "put", 401: "put" }
                    if s in recept:
                    
                        if balance < 1:
                            connector.reset_practice_balance()
                            logger.info('Balance reset')

                        if balance < 10000:
                            bit = balance
                        else:
                            bit = 10000 + (balance % 10000)

                        partition = 5
                        if bit/partition < 1:
                            bit = 1
                        elif bit/partition > 20000:
                            bit = 20000
                        else:
                            bit = bit/partition

                        side = recept[s]
                        duration=1#minute 1 or 5
                        connector.subscribe_strike_list(f,duration)
                        #get strike_list
                        strikedata=connector.get_realtime_strike_list(f, duration)
                        mprice = None
                        mid = None
                        if side == 'call':
                            for price in strikedata:
                                if strikedata[price][side]['profit'] != None:
                                    if strikedata[price][side]['profit'] > 100:
                                        if mprice != None:
                                            if float(price) < mprice:
                                                mprice = float(price)
                                                mid = strikedata[price][side]['id']
                                        else:
                                            mprice = float(price)
                                            mid = strikedata[price][side]['id']
                        else:
                            for price in strikedata:
                                if strikedata[price][side]['profit'] != None:
                                    if strikedata[price][side]['profit'] > 100:
                                        if mprice != None:
                                            if float(price) > mprice:
                                                mprice = float(price)
                                                mid = strikedata[price][side]['id']
                                        else:
                                            mprice = float(price)
                                            mid = strikedata[price][side]['id']
                        check, id = connector.buy_digital(bit, mid)
                        if check == True and type(id) is not dict:
                            balance = get_custom_balance()
                            if balance == None:
                                continue
                            checklist.append((id,s, balance))
                            logger.info(recept[s] + ' on ' + f + ' ' + str(id) + ' ' + str(s) + ' ' + str(balance)+'$' )
                for chl in checklist:
                    sst = time.time()
                    while time.time() - sst < 120:
                        check, win = connector.check_win_digital_v2(chl[0])
                        if check == True:
                            position_id = connector.get_digital_position(chl[0]).get('msg').get('position').get('id')
                            data.append({'Outcome' : (win > 0),
                                     'Id' : chl[0],
                                     'Sum': chl[1],
                                     'Balance': chl[2],
                                     'Closing_time': time.time(),
                                     'Position_Id': position_id
                                    }) # add exam)
                            break
                if len(checklist) > 0:
                    logger.info(checklist)
            json.dump(data, open(path/'r_data.json', 'w'))
            logger.debug(len(data))
            logger.debug(found_s)

            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.exception(str(e))
            logger.exception([exc_type, fname, exc_tb.tb_lineno])
            time.sleep(60*3)


if __name__ == '__main__':
    logger.info('High level entry')
    while True:
        p = Process(target=that)
        p.start()
        p.join(timeout= 15 * 60)