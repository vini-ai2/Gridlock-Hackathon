import numpy as np
import pandas as pd


df = pd.read_csv('dataset.csv')
df.head()
df.describe()
df.info()

subset_counts = df['violation_type'].value_counts()
print(subset_counts)
wrong_parking_df = df[df['violation_type'].str.contains("WRONG PARKING", na=False)]

# 2. Filter rows that contain "NO PARKING" anywhere in the list
no_parking_df = df[df['violation_type'].str.contains("NO PARKING", na=False)]

print(f"Wrong Parking: {len(wrong_parking_df)}")
print(f"No Parking: {len(no_parking_df)}")