import './App.css';
import React, { useState } from 'react';
import AudioUpload from './components/AudioUpload';
import { useForm } from './components/form-hook';
import Button from './components/Button';
import LoadingSpinner from './components/LoadingSpinner';

const App = () => {
  const [formState, inputHandler] = useForm({
    audio: {
      value: null,
      isValid: false,
    },
  });
  const [isLoading, setIsLoading] = useState(false);
  const [recommendedTracks, setRecommendedTracks] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const formData = new FormData();
      formData.append('audioFile', formState.inputs.audio.value);
      setIsLoading(true);
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      const responseData = await response.json();
      setRecommendedTracks(responseData.recommended_tracks || []);
      setIsLoading(false);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="app">
      {isLoading && <LoadingSpinner asOverlay />}
      <h1>Upload an Audio File</h1>
      <form onSubmit={handleSubmit}>
        <AudioUpload
          onInput={inputHandler}
          id="audio"
          errorText="Please provide an audio file."
        />
        <Button type="submit" disabled={!formState.isValid}>
          Find Similar Tracks
        </Button>
      </form>

      {recommendedTracks.length > 0 && (
        <div className="track-list">
          <h2>Recommended Tracks</h2>
          <ul>
            {recommendedTracks.map((track, index) => (
              <li key={index} className="track-item">
                <img
                  src={track.album_cover}
                  alt={track.track_name}
                  className="album-cover"
                />
                <div className="track-info">
                  <p>
                    <strong>Track Name:</strong> {track.track_name}
                  </p>
                  <p>
                    <strong>Artist:</strong> {track.artist}
                  </p>
                  <p>
                    <strong>Genre:</strong> {track.genre}
                  </p>
                  <a
                    href={track.spotify_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="spotify-link"
                  >
                    Listen on Spotify
                  </a>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default App;
