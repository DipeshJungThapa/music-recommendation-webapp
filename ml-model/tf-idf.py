import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the cleaned dataset
filtered_df = pd.read_csv("./fma_metadata/output/merged_cleaned.csv")

# Ensure 'track genres_all' column is present and convert to a space-separated string for TF-IDF processing
filtered_df['track genres_all_str'] = filtered_df['track genres_all'].apply(lambda x: ' '.join(eval(x)))

# Initialize TF-IDF Vectorizer
tfidf = TfidfVectorizer()

# Fit and transform the 'track genres_all_str' column
tfidf_matrix = tfidf.fit_transform(filtered_df['track genres_all_str'])

# Create a DataFrame from the TF-IDF matrix
tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray(), 
    columns=[f"tfidf_{feature}" for feature in tfidf.get_feature_names_out()]
)

# Add the TF-IDF DataFrame to the original DataFrame
filtered_df = pd.concat([filtered_df, tfidf_df], axis=1)

# Drop the intermediate 'track genres_all_str' column and original 'track genres_all' column
filtered_df = filtered_df.drop(columns=['track genres_all_str', 'track genres_all'], axis=1)

# Save the updated DataFrame with the new TF-IDF columns
filtered_df.to_csv("./fma_metadata/output/merged_with_tfidf.csv", index=False)

print("TF-IDF encoding completed and saved to 'merged_with_tfidf.csv'.")
