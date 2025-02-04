import joblib
import pandas as pd
import os
from dotenv import load_dotenv


def filter_columns(df):
    selected_features = [
    col for col in df.columns
    if (col.startswith('chroma_cens mean') or col.startswith('mfcc mean') or
        col.startswith('tonnetz mean') or col.startswith('spectral_contrast mean') or
        col.startswith('spectral_centroid mean') or col.startswith('spectral_rolloff mean') or
        col.startswith('tfidf_')) and col != 'spectral_contrast mean 07'
]
    selected_features.append('audio_features tempo')
    return selected_features


def transform_features(input_features, pca):
    return pca.transform(input_features)


def get_recommendations(knn_model, input_features_pca, n_neighbors=5):
    return knn_model.kneighbors(input_features_pca, n_neighbors=n_neighbors)


def main():
    load_dotenv()
    knn_path = os.getenv('MODEL_PATH')
    pca_path = os.getenv('PCA_PATH')
    df_path = os.getenv('NORMALIZED_EXTRACTED_PATH')
    fma_path = os.getenv('MERGED_CLEANED_PATH')

    knn_model = joblib.load(knn_path)
    #print the number of rows in the training data
    print("KNN Model Training Data Shape:", knn_model._fit_X.shape)

    pca = joblib.load(pca_path)

    df = pd.read_csv(df_path)
    fma_df = pd.read_csv(fma_path)

    track_id = int(input('Enter track ID: '))

    selected_features = filter_columns(df)
    input_song_features = df[selected_features].iloc[track_id].values.reshape(1, -1)
    input_song_features_pca = transform_features(input_song_features, pca)

    
    distances, indices = get_recommendations(knn_model, input_song_features_pca)

    print('Input Song:')
    track_title = df.iloc[track_id]['track title']
    artist_name = df.iloc[track_id]['artist name']
    genre_top = df.iloc[track_id]['genre']
    print(f'Track ID: {track_id}, Title: {track_title}, Artist: {artist_name}, Genre: {genre_top}')

    print('\nRecommendations:')
    for i, idx in enumerate(indices[0]):
        if idx < len(fma_df):
            track_id = fma_df.iloc[idx]['track_id']
            track_title = fma_df.iloc[idx]['track title']
            genre_top = fma_df.iloc[idx]['track genre_top']
            print(f'{i+1}. Track ID: {track_id}, Title: {track_title}, Genre: {genre_top}')
if __name__ == "__main__":
    main()
