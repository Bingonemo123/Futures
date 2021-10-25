import json
import collections
from typing import Collection
import tqdm
from pushover import init, Client

init("aq7rx1r3o55k6rtobcq8xwv66u8jgw")

with open('data.json', 'r') as f:
    data = json.load(f)


tdata = []
division = 1
while True:
    interval = (data[-1].get('Closing_time') - data[0].get('Closing_time'))/division


    bar = tqdm.tqdm(range(division), leave=False)
    for s in bar:
        bar.set_description("Processing %s" % division)
        groups = {x: [] for x in range(s+1)} # s + 1 
        for p in data:
            groups[((p.get('Closing_time') - data[0].get('Closing_time')) // interval )%(s+1)].append(p.get('Outcome'))

        C = {y:collections.Counter(groups[y])[True] for y in groups}
        for z in C:
            try:
                if C[z]/len(groups[z]) > 0.6:
                    bar.write(str([division,s,  z, C[z]/len(groups[z]), interval, C[z], len(groups[z])]))
                    tdata.append([division,s,  z, C[z]/len(groups[z]), interval, C[z], len(groups[z])])
                    with open('Json/timeperioddata.json', 'w+') as f:
                        json.dump(tdata,f)
                    Client("ud1pmkki74te12d3bicw24r99kb38z").send_message(str([division,s,  z, C[z]/len(groups[z]), interval, C[z], len(groups[z])]), title="Interval calculator")
            except ZeroDivisionError:
                pass
    division += 1

##|##|##|##|##