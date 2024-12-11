import pandas as pd


merged_cleaned = pd.read_csv("./fma_metadata/output/merged_and_cleaned.csv")
print(merged_cleaned.info())
#working on this file
#track title:label encoding, artist name:label, track genre_top: one-hot
import pandas as pd


# Load the genre mapping file
genre_mapping = pd.read_csv("./fma_metadata/genres.csv")  # Update with your actual file path

# Create a dictionary for mapping genre IDs to genre names
genre_dict = genre_mapping.set_index('genre_id')['title'].to_dict()

# Function to map numeric genre IDs to genre names
def map_genres(genre_list):
    try:
        # Convert stringified list to actual list and map each ID to its name
        return [genre_dict[int(genre_id)] for genre_id in genre_list.strip('[]').split(',') if genre_id.strip().isdigit()]
    except Exception as e:
        print(f"Error processing genres: {genre_list}, Error: {e}")
        return []

# Apply the mapping function to `track genres` and `track genres_all`
merged_cleaned['track genres'] = merged_cleaned['track genres'].apply(map_genres)
merged_cleaned['track genres_all'] = merged_cleaned['track genres_all'].apply(map_genres)

# Save the updated DataFrame
merged_cleaned.to_csv("./fma_metadata/output/mapped_genres_dataset.csv", index=False)

print("Mapping completed! The updated dataset has been saved as 'mapped_genres_dataset.csv'.")
