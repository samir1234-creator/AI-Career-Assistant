let apiUrl = import.meta.env.VITE_API_URL || '';

if (typeof window !== 'undefined') {
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  if (isLocal) {
    apiUrl = 'http://localhost:8000/api/v1';
  } else {
    if (!apiUrl || apiUrl.includes('localhost') || apiUrl.includes('127.0.0.1')) {
      apiUrl = '/api/v1';
    }
  }
} else {
  if (!apiUrl) {
    apiUrl = '/api/v1';
  }
}

export const CONFIG = {
  API_URL: apiUrl,
  MAX_FILE_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_FILE_TYPES: ['application/pdf'],
};

export const ERROR_MESSAGES = {
  INVALID_FILE_TYPE: 'Please upload a valid PDF file.',
  FILE_TOO_LARGE: 'File size exceeds the 5MB limit.',
  UPLOAD_FAILED: 'An error occurred during upload. Please try again.',
  NETWORK_ERROR: 'Network error or server is unreachable.',
};
