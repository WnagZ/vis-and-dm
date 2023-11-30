import pandas as pd

df = pd.read_csv("filled_data.csv")

columns = ['Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan']
for col in columns:
    df[col] = df[col].astype(int)
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.loc[df['Num_Credit_Card'] >= 12, 'Num_Credit_Card'] = pd.NA  #the maximum value of correct credit cards is 11,
                                                                # all other higher ones are outliers

df.loc[df['Interest_Rate'] >= 35, 'Interest_Rate'] = pd.NA  #the maximum value of correct interest rate is 34,
                                                                # all other higher ones are outliers

df.loc[df['Num_of_Loan'] >= 10, 'Num_of_Loan'] = pd.NA  #the maximum value of correct loans is 9,
                                                                # all other higher ones are outliers

#Delay from due date seems to be clean

def fill_group(group, col_name):
    mode = group[col_name].mode()
    group[col_name] = group[col_name].fillna(mode[0])

    return group

def fill_missing_values(df, col_name):
    grouped = df.groupby('Customer_ID')
    filled_df = grouped.apply(fill_group, col_name=col_name)
    return filled_df

for i in columns:
    print(i)
    df_filled = fill_missing_values(df, col_name= i)

# Clean Num_of_Delayed_Payment by Justin
upper = df['Num_of_Delayed_Payment'].mean()+(2*df['Num_of_Delayed_Payment'].std())

for x in range(len(df['Num_of_Delayed_Payment'])):
    if df['Num_of_Delayed_Payment'][x] > upper:
        df['Num_of_Delayed_Payment'][x] = int(upper)

# Clean Num_Credit_Inquiries by Justin
upper = df['Num_Credit_Inquiries'].mean()+(2*df['Num_Credit_Inquiries'].std())

for x in range(len(df['Num_Credit_Inquiries'])):
    if df['Num_Credit_Inquiries'][x] > upper:
        df['Num_Credit_Inquiries'][x] = int(upper)

df_filled.to_csv("filled_data.csv")
