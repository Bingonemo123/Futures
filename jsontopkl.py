import json
import pickle

import tqdm
from iqoptionapi.stable_api import IQ_Option

connector =IQ_Option("ww.bingonemo@gmail.com","JF*#3C5va&_NDqy")
connector.connect()

real_data = json.load(open("data.json", 'r'))

get_ready = []
for r in tqdm.tqdm(real_data):
    if r.get('Position_Id') != None:
        # if r.get('OTC') != True:
        #     continue

        h = connector.get_digital_position_by_position_id(r.get('Position_Id'))
        # if h.get('msg').get('position').get('instrument_underlying')[-3:] != 'OTC':
        #     continue
        opening_time = h.get('msg').get('position').get('open_quote_time_ms')
        # closing_time = h.get('msg').get('position').get('close_quote_time_ms')
        # open_price = h.get('msg').get('position').get('open_underlying_price')
        # close_price = h.get('msg').get('position').get('close_underlying_price')
        candles = list(connector.get_candles(h.get('msg').get('position').get('instrument_underlying')[:6], 5, 600, opening_time/1000))
        s = sum([1 for c in candles if c.get('close') > candles[-1].get('close')])
        get_ready.append((r.get('Outcome'), s))

with open('getreadyfull.pkl', 'wb') as f:
    pickle.dump(get_ready, f)
