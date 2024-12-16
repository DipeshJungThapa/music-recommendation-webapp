import pandas as pd

def merge_df(tracks_path, features_path,selected_tracks_col,selected_features_col, output_path):
    tracks = pd.read_csv(tracks_path, header=None,low_memory=False)
    features = pd.read_csv(features_path, header=None,low_memory=False)
    
    # extract the header 
    track_header = tracks.iloc[0:3].fillna('').apply(lambda x: ' '.join(x.astype(str).str.strip()), axis=0)
    feature_header = features.iloc[1:4].fillna('').apply(lambda x: ' '.join(x.astype(str).str.strip()), axis=0)
    
    # Update the DataFrame to use the new header
    tracks.columns = track_header.str.strip()
    tracks = tracks[3:]  # Drop the rows used for headers
    tracks.reset_index(drop=True, inplace=True)
    tracks = tracks[selected_tracks_col]

    # same as above for features
    features.columns = feature_header.str.strip()
    features = features[4:] # Drop the rows used for headers
    features.reset_index(drop=True, inplace=True)
    features = features[selected_features_col]

    merged_df = pd.merge(tracks, features, left_index=True, right_index=True)
    return merged_df

def main():
    tracks_path = "./fma_metadata/tracks.csv"
    features_path = "./fma_metadata/echonest.csv"
    output_path = "./fma_metadata/output/merged_data.csv"
    selected_tracks_columns = [
        "track_id","track title", "album id", "artist id","artist name", "track duration", 
        "track genre_top", "track genres", "track genres_all", "track language_code"
    ]
    selected_echonest_columns = [
        "audio_features acousticness", "audio_features danceability", "audio_features energy", "audio_features instrumentalness",
        "audio_features liveness", "audio_features speechiness", "audio_features tempo","social_features artist_hotttnesss", "social_features song_hotttnesss"
    ]

    try:
        merge_df(tracks_path, features_path,selected_tracks_columns,selected_echonest_columns, output_path).to_csv(output_path, index=False)
        print("Merging completed successfully")
    except Exception as e:
        print(f"errors during merging: {e}")
    
if __name__ == "__main__":
    main()
