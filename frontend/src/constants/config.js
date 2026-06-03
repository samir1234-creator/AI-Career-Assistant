export const CONFIG = {
  API_URL: 'http://localhost:8000/api/v1',
  MAX_FILE_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_FILE_TYPES: ['application/pdf'],
};

export const ERROR_MESSAGES = {
  INVALID_FILE_TYPE: 'Please upload a valid PDF file.',
  FILE_TOO_LARGE: 'File size exceeds the 5MB limit.',
  UPLOAD_FAILED: 'An error occurred during upload. Please try again.',
  NETWORK_ERROR: 'Network error or server is unreachable.',
};
