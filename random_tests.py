'''Sandbox for sporadic tests'''

from iqoptionapi.stable_api import IQ_Option
import time
import random
Iq=IQ_Option("levanmikeladze123@gmail.com","591449588")
Iq.connect()#connect to iqoption
ACTIVES="AUDCAD"
duration=1#minute 1 or 5
amount=1
Iq.subscribe_strike_list(ACTIVES,duration)
#get strike_list
data=Iq.get_realtime_strike_list(ACTIVES, duration)
print("get strike data")
print(data)
"""data
{'1.127100':
    {  'call':
            {   'profit': None,
                'id': 'doEURUSD201811120649PT1MC11271'
            },
        'put':
            {   'profit': 566.6666666666666,
                'id': 'doEURUSD201811120649PT1MP11271'
            }
    }............
}
"""
#get price list
# price_list=list(data.keys())
# #random choose Strategy
# choose_price=price_list[random.randint(0,len(price_list)-1)]
# #get instrument_id
# instrument_id=data[choose_price]["call"]["id"]
# #get profit
# profit=data[choose_price]["call"]["profit"]
side = 'call'
mprice = None
mid = None
for price in data:
    if data[price][side]['profit'] != None:
        if data[price][side]['profit'] > 100:
            if mprice != None:
                if float(price) < mprice:
                    mprice = float(price)
                    mid = data[price][side]['id']
            else:
                mprice = float(price)
                mid = data[price][side]['id']

print(mprice, mid, data[str(mprice)])

