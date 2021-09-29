from iqoptionapi.stable_api import IQ_Option
# import Internet_protocols
import time
import json
connector =IQ_Option("ww.bingonemo@gmail.com","JF*#3C5va&_NDqy")
connector.connect()


# ACTIVES="EURUSD"
# duration=1#minute 1 or 5
# amount=1
# action="call"#put
# check =False
# while check == False:
#     check,id=connector.buy_digital_spot(ACTIVES,amount,action,duration) 
# print(id)
# sst = time.time()
# while time.time() - sst < 120:
#     check, win = connector.check_win_digital_v2(id)
#     if check == True:
#         break
# print(win)
data = connector.get_digital_position_by_position_id(14175290216)
with open('Json/posiiton_id_example.json', 'w') as jsonfile:
    json.dump(data, jsonfile)

