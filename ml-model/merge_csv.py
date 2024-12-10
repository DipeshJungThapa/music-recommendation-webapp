import pandas as pd

# Load the file without using any header
tracks = pd.read_csv("./fma_metadata/tracks.csv", header=None)

new_header = tracks.iloc[0:3].fillna('').apply(lambda x: ' '.join(x.astype(str).str.strip()), axis=0)

# Update the DataFrame to use the new header
tracks.columns = new_header.str.strip()
tracks = tracks[3:]  # Drop the rows used for headers

# Reset the index (optional)
tracks.reset_index(drop=True, inplace=True)

#same for features
features = pd.read_csv("./fma_metadata/echonest.csv",header=None)

header = features.iloc[1:4].fillna('').apply(lambda x: ' '.join(x.astype(str).str.strip()), axis=0)

features.columns = header.str.strip()
features = features[4:]

features.reset_index(drop=True, inplace=True)

selected_tracks_columns = [
    "track_id","track title", "album id", "artist id","artist name", "track duration", 
    "track genre_top", "track genres", "track genres_all", "track language_code"
]
tracks = tracks[selected_tracks_columns]

# Select important columns from the echonest DataFrame
selected_echonest_columns = [
    "audio_features acousticness", "audio_features danceability", "audio_features energy", "audio_features instrumentalness",
    "audio_features liveness", "audio_features speechiness", "audio_features tempo","social_features artist_hotttnesss", "social_features song_hotttnesss"
]
features = features[selected_echonest_columns]

# Merge the two DataFrames on `track_id`
merged_df = pd.merge(tracks, features, left_index=True, right_index=True)

# Save the merged data for further processing
merged_df.to_csv("merged_data.csv", index=False)

print("Data has been successfully merged and saved as 'merged_data.csv'.")

