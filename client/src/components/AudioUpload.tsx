import React, { useRef, useState, useEffect, ChangeEvent } from 'react';
import './AudioUpload.css';
import Button from './UI/Button';

type AudioUploadProps = {
  id: string;
  onInput: (id: string, file: File | null, isValid: boolean) => void;
  errorText: string;
};

const AudioUpload: React.FC<AudioUploadProps> = ({
  id,
  onInput,
  errorText,
}) => {
  const filePickerRef = useRef<HTMLInputElement | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [fileInfo, setFileInfo] = useState<{ name: string; size: string }>({
    name: '',
    size: '',
  });
  const [isValid, setIsValid] = useState<boolean>(false);

  useEffect(() => {
    if (!file) return;

    const isMP3 = file.type === 'audio/mpeg';
    const isUnderLimit = file.size <= 10 * 1024 * 1024;

    const valid = isMP3 && isUnderLimit;
    setIsValid(valid);
    setFileInfo({
      name: file.name,
      size: (file.size / 1024).toFixed(2) + ' KB',
    });
  }, [file]);

  const pickedHandler = (event: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;

    if (!selectedFile) {
      setFile(null);
      setIsValid(false);
      onInput(id, null, false);
      return;
    }

    const isMP3 = selectedFile.type === 'audio/mpeg';
    const isUnderLimit = selectedFile.size <= 10 * 1024 * 1024;
    const valid = isMP3 && isUnderLimit;

    setFile(selectedFile);
    setIsValid(valid);
    setFileInfo({
      name: selectedFile.name,
      size: (selectedFile.size / 1024).toFixed(2) + ' KB',
    });
    onInput(id, selectedFile, valid);
  };

  return (
    <div className="form-control">
      <input
        id={id}
        style={{ display: 'none' }}
        ref={filePickerRef}
        type="file"
        accept=".mp3"
        onChange={pickedHandler}
      />
      <div className="audio-upload">
        <div className="audio-upload__preview">
          {file ? (
            <>
              <p>
                <strong>File Name:</strong> {fileInfo.name}
              </p>
              <p>
                <strong>File Size:</strong> {fileInfo.size}
              </p>
            </>
          ) : (
            <p>Please pick an audio file.</p>
          )}
        </div>
        <br />
        <Button type="button" onClick={() => filePickerRef.current?.click()}>
          Pick Audio
        </Button>
      </div>
      {!isValid && file && file.size > 10 * 1024 * 1024 && (
        <p className="error-text">Audio file must be under 10MB.</p>
      )}
      {!isValid && file && file.type !== 'audio/mpeg' && (
        <p className="error-text">Only MP3 files are allowed.</p>
      )}
      {!isValid && !file && <p className="error-text">{errorText}</p>}
    </div>
  );
};

export default AudioUpload;
