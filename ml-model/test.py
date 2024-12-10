import pandas as pd

tracks = pd.read_csv('./fma_metadata/raw_tracks.csv')
features = pd.read_csv('./fma_metadata/echonest.csv')
genres = pd.read_csv('./fma_metadata/genres.csv')

print(features.head())
