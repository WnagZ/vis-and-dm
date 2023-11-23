import pandas as pd
import re

path = 'all_data.csv'
df = pd.read_csv(path, sep=';', lineterminator='\r')
df.drop(columns=['ID', 'Name'])


def KeepAlphabets(text):
    return re.sub(r'[^a-zA-Z]', '', text)


def KeepAlphabetsUnderscore(text):
    return re.sub(r'[^a-zA-Z\_]', '', text)


for i in ['Occupation', 'Credit_Mix', 'Credit_History_Age',
          'Payment_of_Min_Amount', 'Payment_Behaviour', 'Credit_Score']:
    df[i] = df[i].fillna('')                            # Fill NaN with empty string

for i in ['Occupation', 'Credit_Mix', 'Credit_Score']:
    for x in range(len(i)):
        df[i][x] = KeepAlphabets(df[i][x])              # Remove everything except for A-Z

for i in ['Payment_Behaviour']:
    for x in range(len(i)):
        df[i][x] = KeepAlphabetsUnderscore(df[i][x])    # Remove everything except for A-Z and Underscore

