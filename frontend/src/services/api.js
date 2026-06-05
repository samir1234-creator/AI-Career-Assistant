import axios from 'axios';
import { CONFIG, ERROR_MESSAGES } from '../constants/config';

// ─── Helper ───────────────────────────────────────────────────────────────────
const handleAxiosError = (error) => {
  if (error.response?.data?.message) {
    throw new Error(error.response.data.message);
  }
  throw new Error(ERROR_MESSAGES.NETWORK_ERROR || 'Network error. Please try again.');
};

// ─── Resume ───────────────────────────────────────────────────────────────────
export const uploadResume = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const response = await axios.post(`${CONFIG.API_URL}/resume/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const pct = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(pct);
        }
      }
    });
    if (!response.data.success) throw new Error(response.data.message || ERROR_MESSAGES.UPLOAD_FAILED);
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const extractResumeInfo = async (textContent) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/resume/extract`, { text_content: textContent });
    if (!response.data.success) throw new Error(response.data.message || 'Extraction failed');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

// ─── Skills ───────────────────────────────────────────────────────────────────
export const classifySkills = async (skills) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/skills/classify`, { skills });
    if (!response.data.success) throw new Error(response.data.message || 'Classification failed');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

// ─── ATS ──────────────────────────────────────────────────────────────────────
export const getATSScore = async (resumeData) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/ats/score`, resumeData);
    if (!response.data.success) throw new Error(response.data.message || 'ATS scoring failed');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

// ─── Career Recommendations ───────────────────────────────────────────────────
export const getRecommendations = async (resumeData) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/career/recommend`, resumeData);
    if (!response.data.success) throw new Error(response.data.message || 'Recommendations failed');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

// ─── Skill Gap Analysis ───────────────────────────────────────────────────────
export const getSkillGapAnalysis = async (gapPayload) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/skill-gap/analyze`, gapPayload);
    if (!response.data.success) throw new Error(response.data.message || 'Skill gap analysis failed');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

// ─── Roadmap ──────────────────────────────────────────────────────────────────
export const generateRoadmap = async (roadmapPayload) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/roadmap/generate`, roadmapPayload);
    if (!response.data.success) throw new Error(response.data.message || 'Roadmap generation failed');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

/**
 * Share a roadmap — returns { share_id, shareable_url, message }
 */
export const shareRoadmap = async (roadmapData, candidateName) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/roadmap/share`, {
      roadmap: roadmapData,
      candidate_name: candidateName || null,
    });
    if (!response.data.success) throw new Error(response.data.message || 'Share failed');
    return response.data.data; // { share_id, shareable_url }
  } catch (error) { handleAxiosError(error); }
};

/**
 * Retrieve a shared roadmap by its share_id
 */
export const getSharedRoadmap = async (shareId) => {
  try {
    const response = await axios.get(`${CONFIG.API_URL}/roadmap/shared/${shareId}`);
    if (!response.data.success) throw new Error(response.data.message || 'Shared roadmap not found');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

/**
 * Export roadmap as PDF — triggers browser download
 */
export const exportRoadmapPDF = async (roadmapData, candidateName) => {
  try {
    const response = await axios.post(
      `${CONFIG.API_URL}/roadmap/export-pdf`,
      { roadmap: roadmapData, candidate_name: candidateName || null },
      { responseType: 'blob' }
    );

    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const careerName = roadmapData?.career?.replace(/\s+/g, '_') || 'Roadmap';
    a.download = `${careerName}_Career_Roadmap.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (error) {
    // If blob error, try to parse the error message
    if (error.response?.data instanceof Blob) {
      const text = await error.response.data.text();
      try { const parsed = JSON.parse(text); throw new Error(parsed.message || 'PDF export failed'); }
      catch { throw new Error('PDF export failed'); }
    }
    handleAxiosError(error);
  }
};
