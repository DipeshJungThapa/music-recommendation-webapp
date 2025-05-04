import { FormEvent, useState } from 'react';
import AudioUpload from './components/AudioUpload';
import TrackList from './components/TrackList';
import Button from './components/UI/Button';
import { type TrackProps as Track } from './components/TrackItem';
import LoadingSpinner from './components/UI/LoadingSpinner';
import './App.css';
import ErrorModal from './components/UI/ErrorModal';

const App = () => {
  const [fetchedTracks, setFetchedTracks] = useState<Track[] | null>(null);
  const [isFileValid, setIsFileValid] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const inputHandler = (
    _: string,
    selectedFile: File | null,
    isValid: boolean
  ) => {
    setFile(selectedFile);
    setIsFileValid(isValid);
  };
  const clearError = () => {
    setError(null);
  };
  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!file || !isFileValid) return;

    try {
      const formData = new FormData();
      formData.append('audioFile', file);
      setIsLoading(true);

      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to upload the audio.');

      const data = await response.json();
      setFetchedTracks(data.recommended_tracks);
    } catch (error) {
      console.error('Upload error:', error);
      setError((error as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      {error && <ErrorModal error={error} onClear={clearError} />}
      {isLoading && <LoadingSpinner asOverlay />}
      <h1>Upload an Audio File</h1>
      <form onSubmit={handleSubmit}>
        <AudioUpload
          onInput={inputHandler}
          id="audio"
          errorText="Please provide a valid audio file"
        />
        <Button type="submit" disabled={!isFileValid}>
          Find Similar Tracks
        </Button>
        {fetchedTracks && (
          <>
            <h2>Recommended Tracks</h2>
            <TrackList tracks={fetchedTracks} />
          </>
        )}
      </form>
    </div>
  );
};

export default App;
