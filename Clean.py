import pandas as pd
import re

path = 'all_data.csv'
df = pd.read_csv(path, sep=';', lineterminator='\r')
df.drop(columns=['ID', 'Name'])


def KeepAlphabets(text):
    return re.sub(r'[^a-zA-Z]', '', text)


def KeepAlphabetsUnderscore(text):
    return re.sub(r'[^a-zA-Z\_]', '', text)


def KeepAlphabetsNumbers(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text)


for i in ['Occupation', 'Credit_Mix', 'Credit_History_Age',
          'Payment_of_Min_Amount', 'Payment_Behaviour', 'Credit_Score']:
    df[i] = df[i].fillna('')
    # Fill NaN with empty string

for i in ['Occupation', 'Payment_of_Min_Amount', 'Credit_Mix', 'Credit_Score']:
    for x in range(len(df[i])):
        df[i][x] = KeepAlphabets(df[i][x])
        # Remove everything except for A-Z

for i in range(len(df['Payment_Behaviour'])):
    df['Payment_Behaviour'][i] = KeepAlphabetsUnderscore(df['Payment_Behaviour'][i])
    # Remove everything except for A-Z and Underscore

for i in range(len(df['Credit_History_Age'])):
    df['Credit_History_Age'][i] = KeepAlphabetsNumbers(df['Credit_History_Age'][i])
    # Remove everything except for A-Z and Numbers
