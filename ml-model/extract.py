import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TRCK, TDRC
import librosa
import numpy as np
import pandas as pd

# Function to extract metadata
def extract_metadata(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)
        tags = audio.tags
        
        metadata = {
            "title": tags.get("TIT2").text[0] if tags and "TIT2" in tags else "Unknown",
            "artist": tags.get("TPE1").text[0] if tags and "TPE1" in tags else "Unknown",
            "album": tags.get("TALB").text[0] if tags and "TALB" in tags else "Unknown",
            "genre": tags.get("TCON").text[0] if tags and "TCON" in tags else "Unknown",
            "track_number": tags.get("TRCK").text[0] if tags and "TRCK" in tags else "Unknown",
            "release_date": tags.get("TDRC").text[0] if tags and "TDRC" in tags else "Unknown",
            "duration": int(audio.info.length) if audio.info else 0
        }
    except Exception as e:
        metadata = {
            "title": "Unknown",
            "artist": "Unknown",
            "album": "Unknown",
            "genre": "Unknown",
            "track_number": "Unknown",
            "release_date": "Unknown",
            "duration": 0
        }
        print(f"Error extracting metadata for {file_path}: {e}")
    return metadata

# Function to extract audio features
def extract_audio_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=22050, mono=True)
        features = {
            "tempo": librosa.beat.tempo(y=y, sr=sr)[0],
            "spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
            "spectral_bandwidth": np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
            "rolloff": np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)),
            "zero_crossing_rate": np.mean(librosa.feature.zero_crossing_rate(y)),
            **{f"mfcc_{i+1}": v for i, v in enumerate(np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20), axis=1))}
        }
    except Exception as e:
        features = {
            "tempo": 0,
            "spectral_centroid": 0,
            "spectral_bandwidth": 0,
            "rolloff": 0,
            "zero_crossing_rate": 0,
            **{f"mfcc_{i+1}": 0 for i in range(20)}
        }
        print(f"Error extracting audio features for {file_path}: {e}")
    return features

# Main function to process a directory of audio files
def process_audio_directory(directory_path, output_file="audio_features.csv"):
    audio_data = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(('.mp3', '.wav', '.flac', '.ogg')):
            file_path = os.path.join(directory_path, file_name)
            print(f"Processing: {file_name}")
            try:
                metadata = extract_metadata(file_path)
                audio_features = extract_audio_features(file_path)
                combined_data = {**metadata, **audio_features}
                combined_data["file_name"] = file_name
                audio_data.append(combined_data)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    # Convert the data to a DataFrame and save it to CSV
    df = pd.DataFrame(audio_data)
    df.to_csv(output_file, index=False)
    print(f"Audio data saved to {output_file}")

# Specify the directory path
audio_directory = './test-files/'  # Replace with your directory path
process_audio_directory(audio_directory, output_file="audio_features.csv")
