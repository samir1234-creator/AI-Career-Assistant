import React, { useState } from 'react';
import { ResumeUpload } from '../components/ResumeUpload/ResumeUpload';
import { formatFileSize } from '../utils/formatters';

export const AnalyzerPage = () => {
  const [parsedData, setParsedData] = useState(null);

  const handleUploadSuccess = (data) => {
    setParsedData(data);
  };

  return (
    <div className="container">
      <div className="text-center mb-8">
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#fff' }}>
          Resume Analyzer
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>
          Upload your resume (PDF) to extract its contents securely.
        </p>
      </div>

      {!parsedData ? (
        <ResumeUpload onUploadSuccess={handleUploadSuccess} />
      ) : (
        <div style={{ backgroundColor: 'var(--bg-card)', padding: '2rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Parsing Results</h2>
            <button 
              onClick={() => setParsedData(null)}
              style={{
                backgroundColor: 'transparent',
                color: 'var(--text-muted)',
                border: '1px solid var(--border-color)',
                padding: '0.5rem 1rem',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
            >
              Upload Another
            </button>
          </div>
          
          <div style={{ marginBottom: '2rem' }}>
            <p><strong>Filename:</strong> {parsedData.filename}</p>
            <p><strong>Size:</strong> {formatFileSize(parsedData.file_size_bytes)}</p>
            <p><strong>Pages:</strong> {parsedData.page_count}</p>
          </div>
          
          <div>
            <h3 style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>Extracted Text:</h3>
            <div style={{ 
              backgroundColor: 'var(--bg-dark)', 
              padding: '1.5rem', 
              borderRadius: '8px', 
              maxHeight: '400px', 
              overflowY: 'auto',
              whiteSpace: 'pre-wrap',
              fontFamily: 'monospace',
              fontSize: '0.9rem',
              color: '#cbd5e1',
              border: '1px solid var(--border-color)'
            }}>
              {parsedData.text_content}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
