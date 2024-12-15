from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Load the filtered dataset
filtered_df = pd.read_csv("./fma_metadata/output/merged_cleaned_encoded.csv") 
# Convert list of genres in `track genres_all` to a space-separated string
filtered_df['track genres_all_str'] = filtered_df['track genres_all'].apply(lambda x: ' '.join(eval(x)))

# Initialize TF-IDF Vectorizer
tfidf = TfidfVectorizer()

# Fit and transform the `track genres_all_str` column
tfidf_matrix = tfidf.fit_transform(filtered_df['track genres_all_str'])

# Convert the TF-IDF matrix to a DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())

# Conca
# tenate the TF-IDF DataFrame with the original dataset
filtered_df = pd.concat([filtered_df, tfidf_df], axis=1)

# Drop the original `track genres_all`, `track genres`, and `track genres_all_str` columns
filtered_df.drop(columns=['track genres_all', 'track genres', 'track genres_all_str'], inplace=True)

# Save the resulting dataset
filtered_df.to_csv("./fma_metadata/output/final_with_tfidf_cleaned.csv", index=False)

print(f"TF-IDF features added, redundant columns dropped, and saved as 'final_with_tfidf_cleaned.csv'.")
