import pandas as pd
import numpy as np
import re

path = 'all_data.csv'
path1 = 'clean_data.csv'
path2 = 'filled_data.csv'
df = pd.read_csv(path, sep=';', lineterminator='\r')
# df = pd.read_csv(path2)
df.drop(columns=['ID', 'Name'], inplace = True)
df.drop(columns=['Unnamed: 0'], inplace = True)


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

df['Annual_Income'] = df['Annual_Income'].replace('[^\d.,]', '', regex=True).str.replace(',', '.', regex=False).astype(
    float)
df['Monthly_Inhand_Salary'] = df['Monthly_Inhand_Salary'].replace('[^\d.,]', '', regex=True).str.replace(',', '.',
                                                                                                         regex=False).astype(
    float)
df['Outstanding_Debt'] = df['Outstanding_Debt'].replace('[^\d.,]', '', regex=True).str.replace(',', '.',
                                                                                               regex=False).astype(
    float)
df['Total_EMI_per_month'] = df['Total_EMI_per_month'].replace('[^\d.,]', '', regex=True).str.replace(',', '.',
                                                                                                     regex=False).astype(
    float)
df['Amount_invested_monthly'] = df['Amount_invested_monthly'].replace('[^\d.,]', '', regex=True).str.replace(',', '.',
                                                                                                             regex=False).astype(
    float)
df['Monthly_Balance'] = df['Monthly_Balance'].replace('[^\d,]', '', regex=True).str.replace(',', '.',
                                                                                            regex=False).astype(float)
df['Monthly_Balance'] = pd.to_numeric(df['Monthly_Balance'], errors='coerce')
df['Num_Credit_Card'] = df['Num_Credit_Card'].replace('[^\d,]', '', regex=True)
df['Num_Credit_Card'] = pd.to_numeric(df['Num_Credit_Card'], errors='coerce',
                                      downcast='integer')  # this one still has issues
df['Interest_Rate'] = df['Interest_Rate'].replace('[^\d,]', '', regex=True)
df['Interest_Rate'] = pd.to_numeric(df['Interest_Rate'], errors='coerce', downcast='integer')
df['Num_of_Loan'] = df['Num_of_Loan'].replace('[^\d,]', '', regex=True)
df['Num_of_Loan'] = pd.to_numeric(df['Num_of_Loan'], errors='coerce', downcast='integer')
df['Num_of_Delayed_Payment'] = df['Num_of_Delayed_Payment'].replace('[^\d,]', '', regex=True)
df['Num_of_Delayed_Payment'] = pd.to_numeric(df['Num_of_Delayed_Payment'], errors='coerce', downcast='integer')
df['Num_Credit_Inquiries'] = df['Num_Credit_Inquiries'].replace('[^\d,]', '', regex=True)
df['Num_Credit_Inquiries'] = pd.to_numeric(df['Num_Credit_Inquiries'], errors='coerce', downcast='integer')
df['Credit_Utilization_Ratio'] = df['Credit_Utilization_Ratio'].replace('[^\d.,]', '', regex=True).str.replace(',', '.',
                                                                                                               regex=False).astype(
    float)
df["Age"] = df["Age"].replace("_", "")
df['Age'] = pd.to_numeric(df['Age'], errors='coerce', downcast='integer')
del df["SSN"]

# deal with Changed_Credit_Limit
# deal with Credit_History_Age
# map Payment_of_Min_Amount
# map Total_EMI_per_month
# one hot encode Payment_Behaviour
# map Credit_Score

df = pd.read_csv('clean_data.csv')
df['Age'] = df['Age'].astype('Int64')
df = df.replace('', np.nan)
df = df.dropna(subset=['Annual_Income'])

def fill_group(group, col_name):
    mode = group[col_name].mode()
    group[col_name] = group[col_name].fillna(mode[0])

    return group

def fill_missing_values(df, col_name):
    grouped = df.groupby('Customer_ID')
    filled_df = grouped.apply(fill_group, col_name=col_name)
    return filled_df

columns = ['Age', 'Occupation', 'Monthly_Inhand_Salary']
for i in columns:
    print(i)
    df = fill_missing_values(df, col_name= i)

# Step 1: Extract unique types of loans from the "Type_of_Loan" column
unique_loan_types = set()

for col_str in [i for i in df["Type_of_Loan"].unique()]:
    types = re.split(', |and ', str(col_str))
    #types = str(col_str).split(', | and ')
    unique_loan_types.update(set(types))

unique_loan_types.remove('')
unique_loan_types.remove('nan')
# Step 2: Convert the set to a list
loan_types = list(unique_loan_types)

# Step 1: Create new columns for each type of loan
for loan_type in loan_types:
    df[loan_type] = 0

# Step 2: Update the new columns based on the "Type_of_Loan" column
for index, row in df.iterrows():
    type_of_loans = re.split(', |and ', str(row['Type_of_Loan']))
    for loan_type in loan_types:
        if loan_type in type_of_loans:
            df.at[index, loan_type] = 1

# Step 3: Drop the original "Type_of_Loan" column
df = df.drop('Type_of_Loan', axis=1)

df.rename(columns = {'Not Specified':'Loan Not Specified'}, inplace = True)

df.to_csv("filled_data.csv")
