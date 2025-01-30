import pandas as pd
import os
from dotenv import load_dotenv
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
    filtered_df = filtered_df.drop(columns=['track genres_all_str', 'track genres_all'], axis=1)
    return filtered_df

def main():
    load_dotenv()
    merged_cleaned_encoded_path = os.getenv("MERGED_CLEANED_ENCODED_PATH")
    merged_cleaned_encoded_tfidf_path = os.getenv("MERGED_CLEANED_ENCODED_TFIDF_PATH")
    
    if not all([merged_cleaned_encoded_path, merged_cleaned_encoded_tfidf_path]):
        print("One or more environment variables are missing")
        return
    
    
    try:
        df = tf_idf(merged_cleaned_encoded_path).to_csv(merged_cleaned_encoded_tfidf_path,index=False)
        print("TF-IDF encoding completed and saved to 'merged_cleaned_encoded_tfidf.csv'.")
    except Exception as e:
        print(e)
        print("Error encountered while performing TF-IDF encoding")

if __name__ == "__main__":
    main()
