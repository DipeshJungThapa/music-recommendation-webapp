import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def tf_idf(input_file_path):
    filtered_df = pd.read_csv(input_file_path)
    #to make sure ttrack genres_all column is present and convert to a space-separated string for TF-IDF processing
    filtered_df['track genres_all_str'] = filtered_df['track genres_all'].apply(lambda x: ' '.join(eval(x)))
    tfidf = TfidfVectorizer()
    #Fit and transform the 'track genres_all_str' column
    tfidf_matrix = tfidf.fit_transform(filtered_df['track genres_all_str'])
    #create df from matrix
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=[f"tfidf_{feature}" for feature in tfidf.get_feature_names_out()]
    )
    #merge two df that we have
    filtered_df = pd.concat([filtered_df, tfidf_df], axis=1)
    #drop original columns
    filtered_df = filtered_df.drop(columns=['track genres_all_str', 'track genres_all','track genres'], axis=1)
    return filtered_df

def main():
    try:
        df = tf_idf("./fma_metadata/output/merged_cleaned_encoded.csv").to_csv("./fma_metadata/output/merged_cleaned_encoded_tfidf.csv",index=False)
        print("TF-IDF encoding completed and saved to 'merged_cleaned_encoded_tfidf.csv'.")
    except Exception as e:
        print(e)
        print("Error encountered while performing TF-IDF encoding")

if __name__ == "__main__":
    main()
