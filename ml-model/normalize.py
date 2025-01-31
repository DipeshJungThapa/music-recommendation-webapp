import pandas as pd
import os
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler

def normalize(input_file_path,col_to_normalize):
    df = pd.read_csv(input_file_path)
    scaler = MinMaxScaler()
    df[col_to_normalize] = scaler.fit_transform(df[col_to_normalize])
    return df

def main():
    load_dotenv()
    merged_cleaned_encoded_tfidf_path = os.getenv("MERGED_CLEANED_ENCODED_TFIDF_PATH")
    output_file = os.getenv("NORMALIZED_PATH")

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
        df = normalize(merged_cleaned_encoded_tfidf_path,col_to_normalize).to_csv(output_file,index=False)
        print("Data normalization completed and saved to 'normalized.csv'.")
    except Exception as e:
        print(e)
        print("Error endocuntered while normalizing the data")

if __name__ == "__main__":
    main()