import pandas as pd
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
    df = pd.read_csv("./fma_metadata/output/merged_cleaned.csv")
    
    encode_column(df, 'track genre_top')
    encode_column(df, 'artist name')
    
    output_file = './fma_metadata/output/merged_cleaned_encoded.csv'
    df.to_csv(output_file, index=False)
    print(f"Encoded data with both Label Encoding and One-Hot Encoding has been saved to '{output_file}'.")


if __name__ == "__main__":
    main()