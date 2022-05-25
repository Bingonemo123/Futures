
import pandas as pd

filename = 'Json/tensordata.csv'
new_filename = 'Json/tensordataclean.csv'


df = pd.read_csv(new_filename, chunksize=10000)

for chunk in df:
    print(chunk)