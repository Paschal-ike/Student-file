import React, { useState } from 'react';
import useFileUpload from '../hooks/useFileUpload';
import './FileUpload.css';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const { uploadFile, uploading } = useFileUpload();

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (!file) {
      alert('Please select a file.');
      return;
    }
    uploadFile(file);
  };

  return (
    <div className="upload-container">
      <h2>Upload Student Data</h2>
      <input
        type="file"
        accept=".csv, .xlsx"
        className="file-input"
        onChange={handleFileChange}
      />
      <button
        onClick={handleFileUpload}
        className="upload-button"
        disabled={uploading}
      >
        {uploading ? 'Uploading...' : 'Upload File'}
      </button>
    </div>
  );
};

export default FileUpload;
