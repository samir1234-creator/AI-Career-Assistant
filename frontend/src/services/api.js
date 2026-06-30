import axios from 'axios';
import { auth } from './firebase';
import { CONFIG, ERROR_MESSAGES } from '../constants/config';

// Set default timeout to 120 seconds to prevent indefinite hangs
axios.defaults.timeout = 120000;

// Request interceptor to inject Bearer Token
axios.interceptors.request.use(async (config) => {
  const simToken = localStorage.getItem('sim_token');
  if (simToken) {
    config.headers.Authorization = `Bearer ${simToken}`;
    return config;
  }
  
  try {
    const firebaseUser = auth.currentUser;
    if (firebaseUser) {
      const token = await firebaseUser.getIdToken();
      config.headers.Authorization = `Bearer ${token}`;
    }
  } catch (e) {
    console.error("Failed to inject Firebase auth token:", e);
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});



// ─── Helper ───────────────────────────────────────────────────────────────────
const handleAxiosError = (error) => {
  if (error.response?.data?.message) {
    throw new Error(error.response.data.message);
  }
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail;
    if (typeof detail === 'string') {
      throw new Error(detail);
    } else if (Array.isArray(detail)) {
      throw new Error(detail.map(d => `${d.loc?.join('.')} ${d.msg}`).join(', '));
    }
  }
  throw new Error(ERROR_MESSAGES.NETWORK_ERROR || 'Network error. Please try again.');
};

// ─── Resume ───────────────────────────────────────────────────────────────────
export const uploadResume = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const response = await axios.post(`${CONFIG.API_URL}/resume/upload`, formData, {
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
      try { const parsed = JSON.parse(text); throw new Error(parsed.message || 'PDF export failed', { cause: error }); }
      catch { throw new Error('PDF export failed', { cause: error }); }
    }
    handleAxiosError(error);
  }
};

// Cache state
let dashboardSummaryCache = null;
let dashboardSummaryTime = 0;

export const getDashboardSummary = async (forceRefresh = false) => {
  const now = Date.now();
  
  // Cache Hit - staleTime (15s), cacheTime (30s)
  if (!forceRefresh && dashboardSummaryCache && (now - dashboardSummaryTime) < 30000) {
    return dashboardSummaryCache;
  }
  
  try {
    const response = await axios.get(`${CONFIG.API_URL}/user/dashboard/summary`);
    if (!response.data.success) throw new Error(response.data.message || 'Failed to fetch dashboard summary');
    
    dashboardSummaryCache = response.data.data;
    dashboardSummaryTime = now;
    return response.data.data;
  } catch (error) { 
    handleAxiosError(error); 
  }
};

export const prefetchDashboardSummary = () => {
  const now = Date.now();
  // Fetch in background if cache is empty or older than staleTime (15s)
  if (!dashboardSummaryCache || (now - dashboardSummaryTime) > 15000) {
    axios.get(`${CONFIG.API_URL}/user/dashboard/summary`).then(response => {
      if (response.data?.success) {
        dashboardSummaryCache = response.data.data;
        dashboardSummaryTime = Date.now();
      }
    }).catch(() => {});
  }
};

export const clearDashboardCache = () => {
  dashboardSummaryCache = null;
  dashboardSummaryTime = 0;
};

// ─── SaaS User & Progress APIs (Wrappers around cached summary) ──────────────
export const getUserDashboard = async () => {
  const summary = await getDashboardSummary();
  return {
    has_active_roadmap: summary.has_active_roadmap,
    current_readiness: summary.readiness.current_readiness,
    projected_readiness: summary.readiness.projected_readiness,
    roadmap_progress: summary.progress.roadmap_progress,
    completed_tasks: summary.progress.completed_tasks,
    remaining_tasks: summary.progress.remaining_tasks,
    completed_skills: summary.progress.completed_skills,
    remaining_skills: summary.progress.remaining_skills,
    achievements: summary.achievements,
    badges: summary.badges,
    estimated_job_ready_date: summary.readiness.estimated_job_ready_date,
    recent_activity: summary.recent_activity,
    success_probability: summary.readiness.success_probability,
    career_goal: summary.profile.current_career_goal
  };
};

export const getUserHistory = async () => {
  const summary = await getDashboardSummary();
  return summary.history;
};

export const getResumeAnalysisDetails = async (resumeId) => {
  try {
    const response = await axios.get(`${CONFIG.API_URL}/user/history/${resumeId}`);
    if (!response.data.success) throw new Error(response.data.message || 'Failed to fetch analysis details');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const getActiveRoadmap = async () => {
  try {
    const response = await axios.get(`${CONFIG.API_URL}/user/roadmap/active`);
    if (!response.data.success) throw new Error(response.data.message || 'Failed to fetch active roadmap');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const updateTaskStatus = async (taskId, status) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/user/roadmap/task/update`, {
      task_id: taskId,
      status: status
    });
    if (!response.data.success) throw new Error(response.data.message || 'Failed to update task status');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};


// ─── Interview APIs (Phase 8) ─────────────────────────────────────────────────

export const startInterviewSession = async (payload) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/interview/start`, payload);
    if (!response.data.success) throw new Error(response.data.message || 'Failed to start session');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const evaluateAnswer = async (payload) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/interview/answer/evaluate`, payload);
    if (!response.data.success) throw new Error(response.data.message || 'Evaluation failed');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const submitCodingSolution = async (payload) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/interview/coding/submit`, payload);
    if (!response.data.success) throw new Error(response.data.message || 'Submission failed');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const completeInterviewSession = async (sessionId, durationSeconds = 0) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/interview/session/complete`, {
      session_id: sessionId,
      duration_seconds: durationSeconds
    });
    if (!response.data.success) throw new Error(response.data.message || 'Failed to complete session');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const getInterviewSessions = async (limit = 20) => {
  try {
    const response = await axios.get(`${CONFIG.API_URL}/interview/sessions?limit=${limit}`);
    if (!response.data.success) throw new Error(response.data.message || 'Failed to fetch sessions');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const getInterviewSessionDetail = async (sessionId) => {
  try {
    const response = await axios.get(`${CONFIG.API_URL}/interview/sessions/${sessionId}`);
    if (!response.data.success) throw new Error(response.data.message || 'Failed to fetch session');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const getInterviewStats = async () => {
  try {
    const response = await axios.get(`${CONFIG.API_URL}/interview/stats`);
    if (!response.data.success) throw new Error(response.data.message || 'Failed to fetch stats');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const getInterviewBadges = async () => {
  try {
    const response = await axios.get(`${CONFIG.API_URL}/interview/badges`);
    if (!response.data.success) throw new Error(response.data.message || 'Failed to fetch badges');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const askCareerCoach = async (message) => {
  try {
    const response = await axios.post(`${CONFIG.API_URL}/interview/career-coach/ask`, { message });
    if (!response.data.success) throw new Error(response.data.message || 'Coach request failed');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};

export const getCareerCoachHistory = async () => {
  try {
    const response = await axios.get(`${CONFIG.API_URL}/interview/career-coach/history`);
    if (!response.data.success) throw new Error(response.data.message || 'Failed to fetch history');
    return response.data.data;
  } catch (error) { handleAxiosError(error); }
};
