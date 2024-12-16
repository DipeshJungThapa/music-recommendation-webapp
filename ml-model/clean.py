import pandas as pd

def load_and_prepare_data():
    # Load merged data
    merged = pd.read_csv("./fma_metadata/output/merged_data.csv")

    # Fill empty cells with 'Unknown'
    merged['track genre_top'] = merged['track genre_top'].fillna('Unknown')
    merged['track language_code'] = merged['track language_code'].fillna('Unknown')

    # Drop 'track duration' since it has 35% empty values
    merged = merged.drop(columns=['track duration'], axis=1)

    # Ensure 'track genres' and 'track genres_all' columns are lists
    merged['track genres'] = merged['track genres'].apply(eval)
    merged['track genres_all'] = merged['track genres_all'].apply(eval)

    # Filter rows where these columns are not empty
    filtered_df = merged[
        (merged['track genres'].apply(len) > 0) & 
        (merged['track genres_all'].apply(len) > 0)
    ]

    return filtered_df

def load_genre_mapping():
    # Load genre mapping
    genre_mapping = pd.read_csv("./fma_metadata/genres.csv")  
    # Create a dictionary for mapping genre IDs to genre names
    return genre_mapping.set_index('genre_id')['title'].to_dict()

def map_genres(genre_list, genre_dict):
    try:
        return [genre_dict[genre_id] for genre_id in genre_list if genre_id in genre_dict]
    except Exception as e:
        print(f"Error processing genres: {genre_list}, Error: {e}")
        return []

def apply_genre_mapping(df, genre_dict):
    df['track genres'] = df['track genres'].apply(lambda x: map_genres(x, genre_dict))
    df['track genres_all'] = df['track genres_all'].apply(lambda x: map_genres(x, genre_dict))
    return df

def main():
    filtered_df = load_and_prepare_data()
    genre_dict = load_genre_mapping()
    filtered_df = apply_genre_mapping(filtered_df, genre_dict)
    filtered_df.to_csv("./fma_metadata/output/merged_cleaned.csv", index=False)
    print("Mapping completed! The updated dataset has been saved as 'merged_cleaned.csv'.")

if __name__ == "__main__":
    main()
