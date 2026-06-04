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
      throw new Error(error.response.data.message, { cause: error });
    }
    throw new Error(ERROR_MESSAGES.NETWORK_ERROR, { cause: error });
  }
};

export const extractResumeInfo = async (textContent) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/resume/extract`, {
      text_content: textContent,
    });
    
    if (!response.data.success) {
      throw new Error(response.data.message || 'Extraction failed');
    }
    
    return response.data.data;
  } catch (error) {
    if (error.response && error.response.data && error.response.data.message) {
      throw new Error(error.response.data.message, { cause: error });
    }
    throw new Error(ERROR_MESSAGES.NETWORK_ERROR, { cause: error });
  }
};

export const classifySkills = async (skills) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/skills/classify`, {
      skills: skills,
    });
    
    if (!response.data.success) {
      throw new Error(response.data.message || 'Skills classification failed');
    }
    
    return response.data.data;
  } catch (error) {
    if (error.response && error.response.data && error.response.data.message) {
      throw new Error(error.response.data.message, { cause: error });
    }
    throw new Error(ERROR_MESSAGES.NETWORK_ERROR, { cause: error });
  }
};

export const getATSScore = async (resumeData) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/ats/score`, resumeData);
    
    if (!response.data.success) {
      throw new Error(response.data.message || 'ATS scoring failed');
    }
    
    return response.data.data;
  } catch (error) {
    if (error.response && error.response.data && error.response.data.message) {
      throw new Error(error.response.data.message, { cause: error });
    }
    throw new Error(ERROR_MESSAGES.NETWORK_ERROR, { cause: error });
  }
};
