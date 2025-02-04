import pandas as pd
import os
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def normalize(input_df, col_to_normalize):
    df = input_df.copy()
    scaler = MinMaxScaler()
    df[col_to_normalize] = scaler.fit_transform(df[col_to_normalize])
    return df

def preprocess(extracted_path):
    df = pd.read_csv(extracted_path)
    df['track_id'] = range(1, len(df) + 1)

    initial_row_count = len(df)
    df = df[df['genre'] != 'Unknown']
    removed_rows = initial_row_count - len(df)
    
    print(f"Removed {removed_rows} rows with 'Unknown' genre.")

    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.any():
        print('Missing values in the following columns:')
        print(missing_values[missing_values > 0])
    else:
        print('No missing values found.')
    
    return df

def perform_tfidf_on_genre(df, genre_column, tfidf_model_path):
    tfidf_vectorizer = joblib.load(tfidf_model_path)
    tfidf_matrix = tfidf_vectorizer.transform(df[genre_column])

    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())    
    tfidf_df.columns = ['tfidf_' + col for col in tfidf_df.columns]

    expected_tfidf_columns = ['tfidf_' + col for col in tfidf_vectorizer.get_feature_names_out()]
    for col in expected_tfidf_columns:
        if col not in tfidf_df:
            tfidf_df[col] = 0
    
    tfidf_df = tfidf_df[expected_tfidf_columns]
    
    df_with_tfidf = pd.concat([df, tfidf_df], axis=1)

    return df_with_tfidf

def main():
    load_dotenv()  
    extracted_path = os.getenv("EXTRACTED_PATH")
    output_file = os.getenv("NORMALIZED_EXTRACTED_PATH")
    tfidf_model_path = './model/tfidf_model.pkl'  

    col_to_normalize = [
        'chroma_cens mean 01', 'chroma_cens mean 02', 'chroma_cens mean 03',
        'chroma_cens mean 04', 'chroma_cens mean 05', 'chroma_cens mean 06',
        'chroma_cens mean 07', 'chroma_cens mean 08', 'chroma_cens mean 09',
        'chroma_cens mean 10', 'chroma_cens mean 11', 'chroma_cens mean 12',
        'mfcc mean 01', 'mfcc mean 02', 'mfcc mean 03', 'mfcc mean 04',
        'mfcc mean 05', 'mfcc mean 06', 'mfcc mean 07', 'mfcc mean 08',
        'mfcc mean 09', 'mfcc mean 10', 'mfcc mean 11', 'mfcc mean 12',
        'mfcc mean 13', 'tonnetz mean 01', 'tonnetz mean 02', 'tonnetz mean 03',
        'tonnetz mean 04', 'tonnetz mean 05', 'tonnetz mean 06',
        'spectral_contrast mean 01', 'spectral_contrast mean 02',
        'spectral_contrast mean 03', 'spectral_contrast mean 04',
        'spectral_contrast mean 05', 'spectral_contrast mean 06',
        'spectral_centroid mean 01', 'spectral_rolloff mean 01','audio_features tempo'
    ]
    
    try:
        df = preprocess(extracted_path)
        df_normalized = normalize(df, col_to_normalize)
        genre_column = 'genre'  
        df_with_tfidf = perform_tfidf_on_genre(df_normalized, genre_column, tfidf_model_path)

        # Reorder columns to keep track_id first
        cols = ['track_id'] + [col for col in df_with_tfidf.columns if col != 'track_id']
        df_with_tfidf = df_with_tfidf[cols]

        df_with_tfidf.to_csv(output_file, index=False)
        print("Data normalization and TF-IDF transformation completed and saved.")
    
    except Exception as e:
        print("Error encountered while processing the data:", e)

if __name__ == "__main__":
    main()
