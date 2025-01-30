import pandas as pd
import os
from dotenv import load_dotenv
import ast

def load_and_prepare_data(merged_path):
    # Load merged data
    merged = pd.read_csv(merged_path, low_memory=False)

    # Ensure 'track genres' and 'track genres_all' columns are lists
    merged['track genres'] = merged['track genres'].apply(lambda x: safe_literal_eval(x))
    merged['track genres_all'] = merged['track genres_all'].apply(lambda x: safe_literal_eval(x))

    # Filter rows where these columns are not empty
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
            return []  # Return empty list if it's not a string
    except (ValueError, SyntaxError):
        return []  # Return empty list if evaluation fails

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
    """Fills empty 'track genre_top' with the first genre from 'track genres'."""
    genres = row['track genres']  # Already a list after eval
    if pd.isna(row['track genre_top']) or row['track genre_top'] == '':
        if genres:
            return genres[0]  # Return first genre if available
        else:
            return 'Unknown'  # Default to 'Unknown' if no genres
    return row['track genre_top']  # If 'track genre_top' is not empty, return it

def main():
    load_dotenv()

    # Load paths from environment variables
    merged_path = os.getenv("MERGED_PATH")
    genres_path = os.getenv("GENRES_PATH")
    merged_cleaned_path = os.getenv("MERGED_CLEANED_PATH")

    if not all([merged_path, genres_path, merged_cleaned_path]):
        print("One or more environment variables are missing. Exiting...")
        return

    # Load and filter the data
    filtered_df = load_and_prepare_data(merged_path)

    # Load genre mapping
    genre_dict = load_genre_mapping(genres_path)

    # Apply genre mapping to the data
    filtered_df = apply_genre_mapping(filtered_df, genre_dict)

    # Replace empty 'track genre_top' using the first genre from 'track genres'
    filtered_df['track genre_top'] = filtered_df.apply(replace_empty_genre, axis=1)
    
    #drop column track genres
    filtered_df.drop(columns=['track genres'], inplace=True)
    # Save the cleaned dataset
    filtered_df.to_csv(merged_cleaned_path, index=False)
    print("Mapping completed! The updated dataset has been saved as 'merged_cleaned.csv'.")

if __name__ == "__main__":
    main()
