from stattools import Stat
import random
import numpy as np
import pickle
real_data = pickle.load(open("data.pkl", 'rb'))   
# real_data = [ (np.random.choice((True, False), p=[0.624, 1-0.624]), random.randint(0, 600)) for k in range(1000)]    
page = Stat(real_data)
page.strmlt(True)