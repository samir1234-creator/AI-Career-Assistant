import { useState } from 'react';
import { uploadResume } from '../services/api';
import { CONFIG, ERROR_MESSAGES } from '../constants/config';

export const useFileUpload = () => {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);

  const handleFileSelection = (selectedFile) => {
    setError(null);
    if (!selectedFile) return false;

    if (!CONFIG.ALLOWED_FILE_TYPES.includes(selectedFile.type)) {
      setError(ERROR_MESSAGES.INVALID_FILE_TYPE);
      return false;
    }

    if (selectedFile.size > CONFIG.MAX_FILE_SIZE) {
      setError(ERROR_MESSAGES.FILE_TOO_LARGE);
      return false;
    }

    setFile(selectedFile);
    return true;
  };

  const uploadFile = async () => {
    if (!file) return null;

    setIsLoading(true);
    setError(null);
    setProgress(0);

    try {
      const data = await uploadResume(file, (percentCompleted) => {
        setProgress(percentCompleted);
      });
      return data;
    } catch (err) {
      setError(err.message || ERROR_MESSAGES.UPLOAD_FAILED);
      return null;
    } finally {
      setIsLoading(false);
      setProgress(0);
    }
  };

  const reset = () => {
    setFile(null);
    setError(null);
    setProgress(0);
  };

  return {
    file,
    isLoading,
    error,
    progress,
    handleFileSelection,
    uploadFile,
    reset,
  };
};
