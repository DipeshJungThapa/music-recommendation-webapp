import pandas as pd

# Read the CSV without specifying the header (treat all rows as data initially)
tracks = pd.read_csv('./fma_metadata/tracks.csv', header=None)

# Manually assign the column names:
# Extract the first column's header from row 3 (index 2)
first_column_header = tracks.iloc[2, 0]

# Extract the headers for the remaining columns from row 2 (index 1)
other_columns_headers = tracks.iloc[1, 1:].tolist()

# Combine the headers
headers = [first_column_header] + other_columns_headers

# Set the new headers
tracks.columns = headers

# Drop rows used for the headers
tracks = tracks.iloc[3:]  # Keep rows from row 4 onward (index 3)

# Reset the index
tracks = tracks.reset_index(drop=True)
tracks = tracks.set_index('track_id')

features = pd.read_csv('./fma_metadata/echonest.csv', header=None)

# Manually assign the column names:
# Extract the first column's header from row 4 (index 3)
first_column_header = features.iloc[3, 0]

# Extract the headers for the remaining columns from row 3 (index 2)
other_columns_headers = features.iloc[2, 1:].tolist()

# Combine the headers
headers = [first_column_header] + other_columns_headers

# Set the new headers
features.columns = headers

# Drop rows used for the headers
features = features.iloc[4:]  # Keep rows from row 5 onward (index 4)

# Reset the index
features = features.reset_index(drop=True)

# Set the first column (e.g., 'feature_id') as the index
features = features.set_index(first_column_header)

selected_tracks_columns = [
    "title", "album_id", "artist id","artist name", "track duration", 
    "track genre_top", "track genres", "track genres_all, track language_code"
]
tracks = tracks[selected_tracks_columns]

# Select important columns from the echonest DataFrame
selected_echonest_columns = [
    "acousticness", "danceability", "energy", "instrumentalness",
    "liveness", "speechiness", "tempo"
]
features = features[selected_echonest_columns]

# Merge the two DataFrames on `track_id`
merged_df = pd.merge(tracks, features, left_index=True, right_index=True)

# Save the merged data for further processing
merged_df.to_csv("merged_data.csv", index=False)

print("Data has been successfully merged and saved as 'merged_data.csv'.")
