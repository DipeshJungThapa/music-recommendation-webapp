import pandas as pd

merged = pd.read_csv("./fma_metadata/output/merged_data.csv")
#fill empty cells with 'Unknown'
merged['track genre_top'] = merged['track genre_top'].fillna('Unknown')
merged['track language_code'] = merged['track language_code'].fillna('Unknown')

#track duration is 35 % empty so drop it
merged_new = merged.drop(columns=['track duration'],axis=1)

merged_new['track genres'] = merged_new['track genres'].apply(eval)
merged_new['track genres_all'] = merged_new['track genres_all'].apply(eval)

filtered_df = merged_new[
    (merged_new['track genres'].apply(len) > 0) & 
    (merged_new['track genres_all'].apply(len) > 0)
]



filtered_df.to_csv("./fma_metadata/output/merged_and_cleaned.csv", index=False)
print("Data has been successfully cleaned and saved as 'merged_and_cleaned.csv'.")

