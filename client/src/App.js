import './App.css';
import React from 'react';
import { useState } from 'react';
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
      console.log(responseData);
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
          Find
        </Button>
      </form>
    </div>
  );
};

export default App;
