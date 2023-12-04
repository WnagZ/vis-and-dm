import pandas as pd
df = pd.read_csv("./METABRIC_RNA_Mutation.csv")#Adapt the path
df_D = pd.concat([df["age_at_diagnosis"], df.iloc[:, 31:520]], axis=1)
D = df_D.to_numpy()
y = df["overall_survival_months"].to_numpy()

