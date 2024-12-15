import pandas as pd

# Load merged data
merged = pd.read_csv("./fma_metadata/output/merged_data.csv")

# Fill empty cells with 'Unknown'
merged['track genre_top'] = merged['track genre_top'].fillna('Unknown')
merged['track language_code'] = merged['track language_code'].fillna('Unknown')

# Drop 'track duration' since it has 35% empty values
merged_new = merged.drop(columns=['track duration'], axis=1)

# Ensure 'track genres' and 'track genres_all' columns are lists
merged_new['track genres'] = merged_new['track genres'].apply(eval)
merged_new['track genres_all'] = merged_new['track genres_all'].apply(eval)

# Filter rows where these columns are not empty
filtered_df = merged_new[
    (merged_new['track genres'].apply(len) > 0) & 
    (merged_new['track genres_all'].apply(len) > 0)
]

# Load genre mapping
genre_mapping = pd.read_csv("./fma_metadata/genres.csv")  
# Create a dictionary for mapping genre IDs to genre names
genre_dict = genre_mapping.set_index('genre_id')['title'].to_dict()

# Define mapping function
def map_genres(genre_list):
    try:
        return [genre_dict[genre_id] for genre_id in genre_list if genre_id in genre_dict]
    except Exception as e:
        print(f"Error processing genres: {genre_list}, Error: {e}")
        return []

# Apply mapping to the columns using .loc to avoid SettingWithCopyWarning
filtered_df.loc[:, 'track genres'] = filtered_df['track genres'].apply(map_genres)
filtered_df.loc[:, 'track genres_all'] = filtered_df['track genres_all'].apply(map_genres)

# Save the updated DataFrame
filtered_df.to_csv("./fma_metadata/output/merged_cleaned.csv", index=False)

print("Mapping completed! The updated dataset has been saved as 'merged_cleaned.csv'.")
