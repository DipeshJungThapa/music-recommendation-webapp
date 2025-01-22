import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("./fma_metadata/output/merged_cleaned_encoded_tfidf.csv")



tfidf_columns = [col for col in df.columns if col.startswith("tfidf_")]
audio_feature_columns = [
    "audio_features acousticness", "audio_features danceability", "audio_features energy",
    "audio_features instrumentalness", "audio_features liveness", "audio_features speechiness",
    "audio_features tempo"
]


feature_columns = tfidf_columns + audio_feature_columns 


feature_matrix = df[feature_columns]


cosine_sim_matrix = cosine_similarity(feature_matrix)


def get_recommendations(track_id, num_recommendations=5):
    """
    Generates recommendations for a given track ID based on cosine similarity.
    
    Args:
        track_id (int): The track ID for which recommendations are generated.
        num_recommendations (int): Number of recommendations to return.
    
    Returns:
        pd.DataFrame: A DataFrame containing recommended tracks.
    """
    try:
        
        track_idx = df.index[df["track_id"] == track_id].tolist()[0]

        
        sim_scores = list(enumerate(cosine_sim_matrix[track_idx]))

        
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        
        top_indices = [i[0] for i in sim_scores[1:num_recommendations + 1]]

        
        recommendations = df.iloc[top_indices][[
            "track_id", "track title", "artist name", "track genre_top"
        ]]

        return recommendations
    except IndexError:
        print(f"Track ID {track_id} not found in the dataset.")
        return pd.DataFrame()


track_id_to_search =   184
num_recommendations = 10
recommended_tracks = get_recommendations(track_id_to_search, num_recommendations)

print(f"Recommendations for Track ID {track_id_to_search}:\n")
print(recommended_tracks)
