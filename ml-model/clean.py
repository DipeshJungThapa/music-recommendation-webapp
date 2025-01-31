import pandas as pd
import os
from dotenv import load_dotenv
import ast

def load_and_prepare_data(merged_path):
    
    merged = pd.read_csv(merged_path, low_memory=False)

    
    merged['track genres'] = merged['track genres'].apply(lambda x: safe_literal_eval(x))
    merged['track genres_all'] = merged['track genres_all'].apply(lambda x: safe_literal_eval(x))

    
    filtered_df = merged[
        (merged['track genres'].apply(len) > 0) & 
        (merged['track genres_all'].apply(len) > 0)
    ]
    return filtered_df

def safe_literal_eval(value):
    try:
        if isinstance(value, str):
            return ast.literal_eval(value)
        else:
            return []  
    except (ValueError, SyntaxError):
        return []  

def load_genre_mapping(genres_path):
    genre_mapping = pd.read_csv(genres_path)
    return genre_mapping.set_index('genre_id')['title'].to_dict()

def map_genres(genre_list, genre_dict):
    return [genre_dict.get(genre_id, 'Unknown') for genre_id in genre_list]

def apply_genre_mapping(df, genre_dict):
    df['track genres'] = df['track genres'].apply(lambda x: map_genres(x, genre_dict))
    df['track genres_all'] = df['track genres_all'].apply(lambda x: map_genres(x, genre_dict))
    return df

def replace_empty_genre(row):
    genres = row['track genres']  
    if pd.isna(row['track genre_top']) or row['track genre_top'] == '':
        if genres:
            return genres[0]  
        else:
            return 'Unknown' 
    return row['track genre_top'] 
def main():
    load_dotenv()
    merged_path = os.getenv("MERGED_PATH")
    genres_path = os.getenv("GENRES_PATH")
    merged_cleaned_path = os.getenv("MERGED_CLEANED_PATH")

    if not all([merged_path, genres_path, merged_cleaned_path]):
        print("One or more environment variables are missing. Exiting...")
        return

    filtered_df = load_and_prepare_data(merged_path)
    genre_dict = load_genre_mapping(genres_path)

    filtered_df = apply_genre_mapping(filtered_df, genre_dict)
    filtered_df['track genre_top'] = filtered_df.apply(replace_empty_genre, axis=1)
    filtered_df.drop(columns=['track genres'], inplace=True)
    
    filtered_df.to_csv(merged_cleaned_path, index=False)
    print("Mapping completed! The updated dataset has been saved as 'merged_cleaned.csv'.")

if __name__ == "__main__":
    main()
