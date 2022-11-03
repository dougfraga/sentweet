# Import the libraries
import tweepy
import pandas as pd
import numpy as np
import re
import datetime


keywords = 'frouxonaro'


# Import DataFrame
df = pd.read_csv(f'tweets_{keywords}_en.txt', sep='\t', encoding='utf-8')


for index, row in df.iterrows():
    print(row['Tweet'],'\n', row['Analysis'],'\n\n\n')

