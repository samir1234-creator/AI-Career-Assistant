import axios from 'axios';
import { CONFIG, ERROR_MESSAGES } from '../constants/config';

export const uploadResume = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`${CONFIG.API_URL}/resume/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted);
        }
      }
    });
    
    // According to our new BaseResponse
    if (!response.data.success) {
      throw new Error(response.data.message || ERROR_MESSAGES.UPLOAD_FAILED);
    }
    
    return response.data.data;
  } catch (error) {
    if (error.response && error.response.data && error.response.data.message) {
      throw new Error(error.response.data.message);
    }
    throw new Error(ERROR_MESSAGES.NETWORK_ERROR);
  }
};
