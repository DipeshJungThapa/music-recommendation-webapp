import pandas as pd

merged = pd.read_csv("./fma_metadata/output/merged_data.csv")
#fill empty cells with 'Unknown'
merged['track genre_top'] = merged['track genre_top'].fillna('Unknown')
merged['track language_code'] = merged['track language_code'].fillna('Unknown')

missing_values = merged.isnull().sum()
#print(missing_values)
#track duration is 35 % empty so drop it
merged_new = merged.drop(columns=['track duration'],axis=1)



merged_new.to_csv("./fma_metadata/output/merged_and_cleaned.csv", index=False)
print("Data has been successfully cleaned and saved as 'merged_and_cleaned.csv'.")

merged_cleaned = pd.read_csv("./fma_metadata/output/merged_and_cleaned.csv")
# missing_values = merged_cleaned.isnull().sum()
# print(missing_values)