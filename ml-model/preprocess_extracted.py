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

