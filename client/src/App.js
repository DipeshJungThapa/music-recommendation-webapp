import './App.css';
import React from 'react';
import AudioUpload from './components/AudioUpload';
import { useForm } from './components/form-hook';
import Button from './components/Button';

const App = () => {
  const [formState, inputHandler] = useForm({
    audio: {
      value: null,
      isValid: false,
    },
  });
  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const formData = new FormData();
      formData.append('audioFile', formState.inputs.audio.value);
      console.log(formState.inputs.audio.value);
      await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
    } catch (err) {
      console.log(err);
    }
  };
  return (
    <div className="app">
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
