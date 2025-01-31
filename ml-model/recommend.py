import joblib
import pandas as pd
import os
from dotenv import load_dotenv

def load_model(path):
    return joblib.load(path)

def load_data(file_path):
    return pd.read_csv(file_path)

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


def get_recommendations(knn_model, input_features_pca, n_neighbors=3):
    return knn_model.kneighbors(input_features_pca, n_neighbors=n_neighbors)


def main():
    load_dotenv()
    knn_path = os.getenv('MODEL_PATH')
    pca_path = os.getenv('PCA_PATH')
    df_path = os.getenv('NORMALIZED_EXTRACTED_PATH')
    knn_model = load_model(knn_path)
    pca = load_model(pca_path)
    df = load_data(df_path)

    selected_features = filter_columns(df)
    input_song_features = df[selected_features].iloc[0].values.reshape(1, -1)

    
    input_song_features_pca = transform_features(input_song_features, pca)

    
    distances, indices = get_recommendations(knn_model, input_song_features_pca)

    
    print("Recommended Track Indices:", indices[0])
    print("Distances:", distances[0])

if __name__ == "__main__":
    main()
