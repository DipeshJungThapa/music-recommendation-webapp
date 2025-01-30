import pandas as pd
from dotenv import load_dotenv
from sklearn.preprocessing import LabelEncoder
import os

def encode_column(df, column_name):
    if df[column_name].dtype == 'object':
        label_encoder = LabelEncoder()
        df[column_name] = label_encoder.fit_transform(df[column_name])
        print(f"Label Encoding applied to '{column_name}' column.")
    else:
        print(f"The '{column_name}' column is not of type object and may not need encoding.")
    
    # Print unique values after encoding
    print(f"Unique values in '{column_name}' after encoding:")
    print(df[column_name].unique())

def main():
    load_dotenv()
    merged_cleaned_path = os.getenv("MERGED_CLEANED_PATH")
    merged_cleaned_encoded_path = os.getenv("MERGED_CLEANED_ENCODED_PATH")

    df = pd.read_csv(merged_cleaned_path)
    
    encode_column(df, 'track genre_top')
    encode_column(df, 'artist name')
    
    output_file = merged_cleaned_encoded_path
    df.to_csv(output_file, index=False)
    print(f"Encoded data with both Label Encoding has been saved to '{output_file}'.")


if __name__ == "__main__":
    main()