import pandas as pd

df = pd.read_csv("clean_data.csv")

columns = ['Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan', 'Num_Bank_Accounts']
for col in columns:
    print(col)
    # df[col] = df[col].astype(int)
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.loc[df['Num_Credit_Card'] >= 12, 'Num_Credit_Card'] = pd.NA  #the maximum value of correct credit cards is 11,
                                                                # all other higher ones are outliers

df.loc[df['Interest_Rate'] >= 35, 'Interest_Rate'] = pd.NA  #the maximum value of correct interest rate is 34,
                                                                # all other higher ones are outliers

df.loc[df['Num_of_Loan'] >= 10, 'Num_of_Loan'] = pd.NA  #the maximum value of correct loans is 9,
                                                                # all other higher ones are outliers

df.loc[(df["Num_Bank_Accounts"] < 0) | (df["Num_Bank_Accounts"] > 10), 'Num_Bank_Accounts'] = pd.NA


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
    df = fill_missing_values(df, col_name= i)

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


def convert_to_years_months(duration):
    if isinstance(duration, float):
        return duration
    years = 0
    months = 0
    if 'Years' in duration:
        years = int(duration.split('Years')[0])
    if 'Months' in duration:
        months = int(duration.split('Months')[0].split('Yearsand')[-1])
    return years + months / 12

df['Credit_History_Age_float'] = df['Credit_History_Age'].apply(convert_to_years_months)


def replace_outliers(df, col_name):
    def replace_group_outliers(group):
        mean = group[col_name].mean()
        std = group[col_name].std()
        mode = group[col_name].mode()
        threshold = 2 * std  # Define your threshold here, based on standard deviation

        group.loc[group[col_name] != mode[0], col_name] = pd.NA
        return group

    return df.groupby('Customer_ID').apply(replace_group_outliers)



df = replace_outliers(df, 'Total_EMI_per_month')
print(df['Total_EMI_per_month'])


def fill_group(group, col_name):
    mode = group[col_name].mode()

    # Replace outliers with mode
    group[col_name] = group[col_name].fillna(mode[0])

    return group

# Function to fill missing values and handle outliers
def fill_missing_values(df, col_name):
    grouped = df.groupby('Customer_ID')
    filled_df = grouped.apply(fill_group, col_name=col_name)
    return filled_df


df = fill_missing_values(df, 'Total_EMI_per_month')

# Clean age
customer_IDs = df[(df['Age'].isna()) | (df['Age'] > 100) | (df['Age'] < 0)]['Customer_ID'].values

# get real age by customer id
for id in customer_IDs:
    realAge = 0
    try:
        realAge = df.loc[(df['Customer_ID'] == id) & (df['Age'].notna()) & (df['Age'] < 100) & (df['Age'] > 0)]['Age'].values[-1]
    except IndexError:
        continue
    # fill missing value
    df.loc[(df['Customer_ID'] == id) & ((df['Age'].isna()) | (df['Age'] > 100) | (df['Age'] < 0)), ['Age']] = realAge

# Clean Monthly_Inhand_Salary
customer_IDs = df[df['Monthly_Inhand_Salary'].isna()]['Customer_ID'].values

# get real age by customer id
for id in customer_IDs:
    realIncome = 0
    try:
        realIncome = df.loc[(df['Customer_ID'] == id) & (df['Monthly_Inhand_Salary'].notna())]['Monthly_Inhand_Salary'].values[-1]
    except IndexError:
        continue
    # fill missing value
    df.loc[(df['Customer_ID'] == id) & (df['Monthly_Inhand_Salary'].isna()), 'Monthly_Inhand_Salary'] = realIncome


df.to_csv("filled_data.csv")