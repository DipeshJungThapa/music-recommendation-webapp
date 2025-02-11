import React, { useRef, useState, useEffect } from 'react';
import './AudioUpload.css';
import Button from './Button';

const AudioUpload = (props) => {
  const filePickerRef = useRef();
  const [file, setFile] = useState();
  const [fileInfo, setFileInfo] = useState({ name: '', size: '' });
  const [isValid, setIsValid] = useState(false);

  useEffect(() => {
    if (!file) {
      return;
    }
    if (
      file.type !== 'audio/mpeg' &&
      file.type !== 'audio/wav' &&
      file.type !== 'audio/ogg' &&
      file.type !== 'audio/flac'
    ) {
      setIsValid(false);
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setIsValid(false);
      return;
    }
    setFileInfo({
      name: file.name,
      size: (file.size / 1024).toFixed(2) + ' KB',
    });
  }, [file]);

  const pickedHandler = (event) => {
    let pickedFile;
    let fileIsValid = isValid;
    if (event.target.files && event.target.files.length === 1) {
      pickedFile = event.target.files[0];
      setFile(pickedFile);
      setIsValid(true);
      fileIsValid = true;
    } else {
      setIsValid(false);
      fileIsValid = false;
    }
    props.onInput(props.id, pickedFile, fileIsValid);
  };

  const AudioHandler = () => {
    filePickerRef.current.click();
  };

  return (
    <div className="form-control">
      <input
        id={props.id}
        style={{ display: 'none' }}
        ref={filePickerRef}
        type="file"
        accept=".mp3,.wav,.ogg,.flac"
        onChange={pickedHandler}
      />
      <div className={`audio-upload ${props.center && 'center'}`}>
        <div className="audio-upload__preview">
          {file && (
            <div>
              <p>
                <strong>File Name:</strong> {fileInfo.name}
              </p>
              <p>
                <strong>File Size:</strong> {fileInfo.size}
              </p>
            </div>
          )}
          {!file && <p>Please pick an audio file.</p>}
        </div>
        <Button type="button" onClick={AudioHandler}>
          Pick Audio
        </Button>
      </div>
      {!isValid && file && file.size > 10 * 1024 * 1024 && (
        <p>Audio file must be under 10MB.</p>
      )}
      {!isValid && !file && <p>{props.errorText}</p>}
    </div>
  );
};

export default AudioUpload;
