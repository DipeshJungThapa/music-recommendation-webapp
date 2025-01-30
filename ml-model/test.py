import os
import pandas as pd
import ast

# Ensure the output directory exists
os.makedirs('ml-model/fma_metadata/output', exist_ok=True)

# Load the dataset
try:
    df = pd.read_csv('./fma_metadata/output/merged.csv')
    df['track genre_top'] = df['track genre_top'].fillna('Unknown')
   
except FileNotFoundError:
    print("Error: The file 'merged_cleaned.csv' was not found.")
    exit()

# Check if required columns exist
required_columns = ['track genre_top', 'track genres']
if not all(col in df.columns for col in required_columns):
    print(f"Error: Required columns {required_columns} are missing from the dataset.")
    print("Available columns:", df.columns)
    exit()

# Replace "Unknown" in 'track genre_top' with the first genre from 'track genres'
def replace_unknown_genre(row):
    try:
        genres = ast.literal_eval(row['track genres']) if isinstance(row['track genres'], str) else []
        if row['track genre_top'] == '' and genres:
            return genres[0]
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing row {row.name}: {e}")
    return row['track genre_top']

# Apply the function row-wise
df['track genre_top'] = df.apply(replace_unknown_genre, axis=1)

# Save the updated dataset
output_file = './merged_cleaned.csv'
df.to_csv(output_file, index=False)

print(f"Dataset updated and saved successfully to {output_file}!")