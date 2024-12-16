import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize(input_file_path,col_to_normalize):
    input_file_path = "./fma_metadata/output/final_with_tfidf_cleaned.csv"
    df = pd.read_csv(input_file_path)
    scaler = MinMaxScaler()
    df[col_to_normalize] = scaler.fit_transform(df[col_to_normalize])
    return df

def main():
    col_to_normalize = [
        'audio_features acousticness',
        'audio_features danceability',
        'audio_features energy',
        'audio_features instrumentalness',
        'audio_features liveness',
        'audio_features speechiness',
        'audio_features tempo',
        'social_features artist_hotttnesss',
        'social_features song_hotttnesss'
        ]

    try:
        df = normalize("./fma_metadata/output/merged_cleaned_encoded_tfidf.csv",col_to_normalize).to_csv("./fma_metadata/output/normalized.csv",index=False)
    except Exception as e:
        print(e)
        print("Error endocuntered while normalizing the data")

if __name__ == "__main__":
    main