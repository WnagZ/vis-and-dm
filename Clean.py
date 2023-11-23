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



df['Annual_Income'] = df['Annual_Income'].replace('[^\d.,]', '', regex=True).str.replace(',', '.', regex=False).astype(float)
df['Monthly_Inhand_Salary'] = df['Monthly_Inhand_Salary'].replace('[^\d.,]', '', regex=True).str.replace(',', '.', regex=False).astype(float)
df['Outstanding_Debt'] = df['Outstanding_Debt'].replace('[^\d.,]', '', regex=True).str.replace(',', '.', regex=False).astype(float)
df['Total_EMI_per_month'] = df['Total_EMI_per_month'].replace('[^\d.,]', '', regex=True).str.replace(',', '.', regex=False).astype(float)
df['Amount_invested_monthly'] = df['Amount_invested_monthly'].replace('[^\d.,]', '', regex=True).str.replace(',', '.', regex=False).astype(float)
df['Monthly_Balance'] = df['Monthly_Balance'].replace('[^\d,]', '', regex=True).str.replace(',', '.', regex=False).astype(float)
df['Monthly_Balance'] = pd.to_numeric(df['Monthly_Balance'], errors='coerce')
df['Num_Credit_Card'] = df['Num_Credit_Card'].replace('[^\d,]', '', regex=True)
df['Num_Credit_Card'] = pd.to_numeric(df['Num_Credit_Card'], errors='coerce', downcast='integer') #this one still has issues
df['Interest_Rate'] = df['Interest_Rate'].replace('[^\d,]', '', regex=True)
df['Interest_Rate'] = pd.to_numeric(df['Interest_Rate'], errors='coerce', downcast='integer')
df['Num_of_Loan'] = df['Num_of_Loan'].replace('[^\d,]', '', regex=True)
df['Num_of_Loan'] = pd.to_numeric(df['Num_of_Loan'], errors='coerce', downcast='integer')
df['Num_of_Delayed_Payment'] = df['Num_of_Delayed_Payment'].replace('[^\d,]', '', regex=True)
df['Num_of_Delayed_Payment'] = pd.to_numeric(df['Num_of_Delayed_Payment'], errors='coerce', downcast='integer')
df['Num_Credit_Inquiries'] = df['Num_Credit_Inquiries'].replace('[^\d,]', '', regex=True)
df['Num_Credit_Inquiries'] = pd.to_numeric(df['Num_Credit_Inquiries'], errors='coerce', downcast='integer')
df['Credit_Utilization_Ratio'] = df['Credit_Utilization_Ratio'].replace('[^\d.,]', '', regex=True).str.replace(',', '.', regex=False).astype(float)
# deal with Changed_Credit_Limit
# deal with Credit_History_Age
# map Payment_of_Min_Amount
# map Total_EMI_per_month
# one hot encode Payment_Behaviour
# map Credit_Score
