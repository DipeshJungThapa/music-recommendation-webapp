import pandas as pd

merged = pd.read_csv("./merged_data.csv")
#fill empty cells with 'Unknown'
merged['track genre_top'] = merged['track genre_top'].fillna('Unknown')
merged.to_csv("merged_and_cleaned.csv", index=False)
print("Data has been successfully cleaned and saved as 'merged_and_cleaned.csv'.")
#fill empty numerical cells with mean or median 