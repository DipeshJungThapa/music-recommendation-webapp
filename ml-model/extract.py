import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON
import librosa
import numpy as np
import pandas as pd
from dotenv import load_dotenv


def extract_metadata(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)
        tags = audio.tags
        
        metadata = {
            "track title": tags.get("TIT2").text[0] if tags and "TIT2" in tags else "Unknown",
            "artist name": tags.get("TPE1").text[0] if tags and "TPE1" in tags else "Unknown",
            "album": tags.get("TALB").text[0] if tags and "TALB" in tags else "Unknown",
            "genre": tags.get("TCON").text[0] if tags and "TCON" in tags else "Unknown",
            "duration": int(audio.info.length) if audio.info else 0
        }
    except Exception as e:
        metadata = {
            "track title": "Unknown",
            "artist name": "Unknown",
            "album": "Unknown",
            "genre": "Unknown",
            "duration": 0
        }
        print(f"Error extracting metadata for {file_path}: {e}")
    return metadata


def extract_audio_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=22050, mono=True)
        features = {
            "audio_features tempo": librosa.beat.tempo(y=y, sr=sr)[0],
        }
        
        
        chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
        for i in range(chroma_cens.shape[0]):
            features[f'chroma_cens mean {i+1:02d}'] = np.mean(chroma_cens[i])

        
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        for i in range(mfcc.shape[0]):
            features[f'mfcc mean {i+1:02d}'] = np.mean(mfcc[i])

        
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
        for i in range(tonnetz.shape[0]):
            features[f'tonnetz mean {i+1:02d}'] = np.mean(tonnetz[i])

        
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        for i in range(spectral_contrast.shape[0]):
            features[f'spectral_contrast mean {i+1:02d}'] = np.mean(spectral_contrast[i])

        
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        features['spectral_centroid mean 01'] = np.mean(spectral_centroid)
        features['spectral_rolloff mean 01'] = np.mean(spectral_rolloff)
    except Exception as e:
        features = {}
        print(f"Error extracting audio features for {file_path}: {e}")
    return features


def process_audio_directory(directory_path, output_file="audio_features.csv"):
    audio_data = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(('.mp3', '.wav', '.flac', '.ogg')):
            file_path = os.path.join(directory_path, file_name)
            print(f"Processing: {file_name}")
            try:
                metadata = extract_metadata(file_path)
                audio_features = extract_audio_features(file_path)
                if audio_features:  
                    combined_data = {**metadata, **audio_features}
                    combined_data["file_name"] = file_name
                    audio_data.append(combined_data)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    
    if audio_data:
        df = pd.DataFrame(audio_data)
        df.to_csv(output_file, index=False)
        print(f"Audio data saved to {output_file}")
    else:
        print("No audio files were processed successfully.")


def main():
    load_dotenv()

    extracted_path = os.getenv("EXTRACTED_PATH")
    audio_directory = os.getenv("AUDIO_DIRECTORY")

    process_audio_directory(audio_directory, output_file=extracted_path)

if __name__ == "__main__":
    main()