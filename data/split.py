#! /usr/bin/env python3

import pandas as pd

src_file = 'noc_2017.csv'
dest_dir = 'noc_2017'
chunksize = 500000

i = 1
for chunk in pd.read_csv(src_file, chunksize=chunksize):
    chunk.to_csv(f'{dest_dir}/{i}.csv')
    print(i)
    i += 1