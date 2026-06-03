import React, { useState, useRef } from 'react';
import './ResumeUpload.css';
import { useFileUpload } from '../../hooks/useFileUpload';

export const ResumeUpload = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);
  
  const {
    file,
    isLoading,
    error,
    progress,
    handleFileSelection,
    uploadFile,
  } = useFileUpload();

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current.click();
  };

  const handleUpload = async () => {
    const data = await uploadFile();
    if (data) {
      onUploadSuccess(data);
    }
  };

  return (
    <div className="resume-upload-container">
      <div 
        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="upload-icon">📄</div>
        <h3>Upload your Resume</h3>
        <p>Drag and drop your PDF here, or click to browse</p>
        
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={(e) => handleFileSelection(e.target.files[0])} 
          accept="application/pdf"
          style={{ display: 'none' }}
        />
        <button className="btn-browse" onClick={handleBrowseClick}>Browse File</button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {file && !error && (
        <div className="file-info-container">
          <div className="file-info">
            <span>Selected: {file.name}</span>
            <button 
              className="btn-upload" 
              onClick={handleUpload} 
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : 'Analyze Resume'}
            </button>
          </div>
          
          {isLoading && (
            <div className="progress-container">
              <div className="progress-bar" style={{ width: `${progress}%` }}></div>
              <span className="progress-text">{progress}%</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
