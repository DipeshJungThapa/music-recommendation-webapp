import pandas as pd
from dotenv import load_dotenv
import os

def merge_df(tracks_path,echonest_path, features_path,selected_tracks_col,selected_echonest_col):
    tracks = pd.read_csv(tracks_path, header=None,low_memory=False)
    echonest = pd.read_csv(echonest_path, header=None,low_memory=False)
    features = pd.read_csv(features_path, header=None,low_memory=False)
    
    # extract the header 
    track_header = tracks.iloc[0:3].fillna('').apply(lambda x: ' '.join(x.astype(str).str.strip()), axis=0)
    echonest_header = echonest.iloc[1:4].fillna('').apply(lambda x: ' '.join(x.astype(str).str.strip()), axis=0)
    features_header = features.iloc[0:4].fillna('').apply(lambda x: ' '.join(x.astype(str).str.strip()), axis=0)

    # Update the DataFrame to use the new header
    tracks.columns = track_header.str.strip()
    tracks = tracks[3:]  # Drop the rows used for headers
    tracks.reset_index(drop=True, inplace=True)
    tracks = tracks[selected_tracks_col]

    # same as above for features
    echonest.columns = echonest_header.str.strip()
    echonest = echonest[4:] # Drop the rows used for headers
    echonest.reset_index(drop=True, inplace=True)
    echonest = echonest[selected_echonest_col]

    # same as above for features
    features.columns = features_header.str.strip()
    features = features[4:] # Drop the rows used for headers
    features.columns = [features.columns[0].replace('feature statistics number', '')] + list(features.columns[1:])

    features.reset_index(drop=True, inplace=True)
    chroma = features.loc[:, 'chroma_cens mean 01':'chroma_cens mean 12']
    mfcc = features.loc[:, 'mfcc mean 01':'mfcc mean 13']
    tonnetz = features.loc[:, 'tonnetz mean 01':'tonnetz mean 06']
    spectral_contrast = features.loc[:, 'spectral_contrast mean 01':'spectral_contrast mean 06']
    other_spetral = ['spectral_centroid mean 01', 'spectral_rolloff mean 01']
    final_features = pd.concat([chroma, mfcc, tonnetz, spectral_contrast, features[other_spetral]], axis=1)



    merged_tracks_echonest = pd.merge(tracks, echonest, left_index=True, right_index=True)
    merged_df = pd.merge(merged_tracks_echonest, final_features, left_index=True, right_index=True)

    return merged_df

def main():
    load_dotenv()
    
    tracks_path = os.getenv("TRACKS_PATH")
    echonest_path = os.getenv("ECHONEST_PATH")
    features_path = os.getenv("FEATURES_PATH")
    output_path =   os.getenv("MERGED_PATH")
    selected_tracks_columns = [
        "track_id","track title", "album id", "artist id","artist name", 
        "track genre_top", "track genres_all", "track language_code"
    ]
    selected_echonest_columns = [
        "audio_features acousticness", "audio_features danceability", "audio_features energy", "audio_features instrumentalness",
        "audio_features liveness", "audio_features speechiness", "audio_features tempo","social_features artist_hotttnesss", "social_features song_hotttnesss"
    ]

    try:
        merge_df(tracks_path,echonest_path,features_path,selected_tracks_columns,selected_echonest_columns).to_csv(output_path, index=False)
        print("Merging completed successfully")
    except Exception as e:
        print(f"errors during merging: {e}")
    
if __name__ == "__main__":
    main()
