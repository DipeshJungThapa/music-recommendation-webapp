import os
import joblib
import pandas as pd
from preprocess_extracted import normalize, perform_tfidf_on_genre
from extract import extract_metadata, extract_audio_features


def save_uploaded_file(file, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file.filename)
    file.save(file_path)
    return file_path


def process_uploaded_file(file_path):
    metadata = extract_metadata(file_path)
    audio_features = extract_audio_features(file_path)

    combined_data = {**metadata, **audio_features}
    combined_data["file_name"] = os.path.basename(file_path)
    return combined_data


def load_and_preprocess_data(combined_data,merged_cleaned_path,tf_idf_path):
    df_dataset = pd.read_csv(merged_cleaned_path)
    df = pd.DataFrame([combined_data])

    cols_to_normalize = [
        col for col in df.columns if col.startswith(('chroma_cens mean', 'mfcc mean', 
                                                    'tonnetz mean', 'spectral_contrast mean', 
                                                    'spectral_centroid mean', 'spectral_rolloff mean', 
                                                    'audio_features tempo'))
    ]
    df_normalized = normalize(df, cols_to_normalize)
    
    df_with_tfidf = perform_tfidf_on_genre(df_normalized, 'genre', tf_idf_path)
    return df_dataset, df_with_tfidf


def get_song_recommendations(df_with_tfidf, df_dataset,knn_path,pca_path):
    knn_model = joblib.load(knn_path)
    pca = joblib.load(pca_path)
    
    selected_features = filter_columns(df_with_tfidf)
    input_song_features = df_with_tfidf[selected_features].iloc[0].values.reshape(1, -1)
    input_song_features_pca = pca.transform(input_song_features)
    distances, indices = knn_model.kneighbors(input_song_features_pca, n_neighbors=5)

    recommended_tracks = [
        {
            "track_name": df_dataset.iloc[idx]['track title'], 
            "artist": df_dataset.iloc[idx]['artist name'], 
            "genre": df_dataset.iloc[idx]['track genre_top']
        } 
        for idx in indices[0]
    ]
    
    return recommended_tracks


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
