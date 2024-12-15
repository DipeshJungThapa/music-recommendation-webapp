import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

# Load the CSV file
input_file = './fma_metadata/output/merged_cleaned.csv'
df = pd.read_csv(input_file)

# === Label Encoding for 'track genre_top' column ===
# Identify the data type of the 'track genre_top' column
genre_top_dtype = df['track genre_top'].dtype

# Print unique values before encoding
print("Unique values in 'track genre_top' before encoding:")
print(df['track genre_top'].unique())

# Check if the column contains unordered categories
if genre_top_dtype == 'object':
    # Apply Label Encoding
    label_encoder = LabelEncoder()
    df['track genre_top'] = label_encoder.fit_transform(df['track genre_top'])
    print("Label Encoding applied to 'track genre_top' column.")
else:
    print("The 'track genre_top' column is not of type object and may not need encoding.")

# Print unique values after encoding
print("Unique values in 'track genre_top' after encoding:")
print(df['track genre_top'].unique())

# === Label Encoding for 'artist name' column ===
# Identify the data type of the 'artist name' column
artist_name_dtype = df['artist name'].dtype

# Print unique values before encoding
print("Unique values in 'artist name' before encoding:")
print(df['artist name'].unique())

# Check if the column contains unordered categories
if artist_name_dtype == 'object':
    # Apply Label Encoding
    artist_label_encoder = LabelEncoder()
    df['artist name'] = artist_label_encoder.fit_transform(df['artist name'])
    print("Label Encoding applied to 'artist name' column.")
else:
    print("The 'artist name' column is not of type object and may not need encoding.")

# Print unique values after encoding
print("Unique values in 'artist name' after encoding:")
print(df['artist name'].unique())

# Save the resulting DataFrame with both encodings to a single CSV file
output_file = './fma_metadata/output/merged_cleaned_encoded.csv'
df.to_csv(output_file, index=False)
print(f"Encoded data with both Label Encoding and One-Hot Encoding has been saved to '{output_file}'.")

# === Setting the output file to read-only mode ===
os.chmod(output_file, 0o444)
print(f"The file '{output_file}' has been set to read-only mode.")
