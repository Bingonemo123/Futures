from iqoptionapi.stable_api import IQ_Option
# import Internet_protocols

import json
connector =IQ_Option("ww.bingonemo@gmail.com","JF*#3C5va&_NDqy")
connector.connect()
data = connector.get_digital_position(14824212618)
print (data)
with open('Json/digital_position_eample.json', 'w') as jsonfile: 
    json.dump(data, jsonfile)
