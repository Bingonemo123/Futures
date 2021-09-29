import pickle 
import json
data = pickle.load(open("data.pkl", 'rb'))
sandwitch = []

for d in data:
    refernece = ['Outcome', 'Sum_close', 'Sum_max', 'Buying_time',
                'Closing_time', 'Buying_price', 'Name', 'Outcome_prediction']
    cdict = {}
    for i in range(len(d)):
        cdict[refernece[i]] = d[i]

    sandwitch.append(cdict)





with open('Json/data.json', 'w') as json_file:
    json.dump(sandwitch, json_file)
