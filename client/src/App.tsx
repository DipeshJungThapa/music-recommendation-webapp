import { FormEvent, useState, ReactNode } from 'react';
import AudioUpload from './components/AudioUpload';
import TrackList from './components/TrackList';
import Button from './components/UI/Button';
import { type TrackProps as Track } from './components/TrackItem';
import LoadingSpinner from './components/UI/LoadingSpinner';
import './App.css';
const App = () => {
  const [fetchedTracks, setFetchedTracks] = useState<Track[] | null>(null);
  const [isFileValid, setIsFileValid] = useState<boolean>(false);
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const inputHandler = (id: string, file: File | null, isValid: boolean) => {
    setFile(file);
    setIsFileValid(isValid);
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    if (!file || !isFileValid) {
      console.log('No valid file selected.');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('audioFile', file);
      setIsLoading(true);
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload the audio.');
      }

      const data = await response.json();
      setIsLoading(false);
      setFetchedTracks(data.recommended_tracks);
    } catch (error) {
      console.error('Error uploading file:', error);
      setIsLoading(false);
    }
  };

  let content: ReactNode = <></>;
  if (fetchedTracks) {
    content = <TrackList tracks={fetchedTracks} isLoading={isLoading} />;
  }

  return (
    <div className="app">
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
          <div>
            <h2>Recommended Tracks</h2>
            {content}
          </div>
        )}
      </form>
    </div>
  );
};

export default App;
