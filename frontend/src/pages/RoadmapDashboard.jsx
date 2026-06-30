import { useState, useEffect, useCallback } from 'react';
import { shareRoadmap, exportRoadmapPDF, getActiveRoadmap, updateTaskStatus } from '../services/api';
import { useLocation } from 'react-router-dom';

// ─── Badge definitions ───────────────────────────────────────────────────────
const BADGE_CATALOG = [
  { id: 'foundations',  name: 'Foundations Master',        emoji: '🏗️', color: '#60a5fa', desc: 'Completed the foundational milestone',        milestoneKeywords: ['foundation', 'python', 'sql', 'programming', 'web foundation'], unlockCondition: 'Complete Foundations milestone' },
  { id: 'ml_explorer',  name: 'Machine Learning Explorer', emoji: '🤖', color: '#a78bfa', desc: 'Mastered core Machine Learning concepts',      milestoneKeywords: ['machine learning', 'ml core', 'scikit'], unlockCondition: 'Complete Machine Learning milestone' },
  { id: 'dl_specialist',name: 'Deep Learning Specialist',  emoji: '🧠', color: '#f472b6', desc: 'Conquered Deep Learning and neural networks',  milestoneKeywords: ['deep learning', 'pytorch', 'tensorflow', 'framework'], unlockCondition: 'Complete Deep Learning milestone' },
  { id: 'nlp_expert',   name: 'NLP Practitioner',          emoji: '📝', color: '#34d399', desc: 'Achieved NLP and language model proficiency',  milestoneKeywords: ['nlp', 'natural language', 'bert', 'transformers'], unlockCondition: 'Complete NLP milestone' },
  { id: 'llm_builder',  name: 'LLM Builder',               emoji: '💡', color: '#fbbf24', desc: 'Built production-ready LLM applications',     milestoneKeywords: ['llm', 'large language', 'gpt', 'generative'], unlockCondition: 'Complete LLM milestone' },
  { id: 'cloud_guru',   name: 'Cloud Practitioner',        emoji: '☁️', color: '#38bdf8', desc: 'Deployed and managed cloud infrastructure',   milestoneKeywords: ['cloud', 'aws', 'azure', 'gcp', 'devops', 'deployment'], unlockCondition: 'Complete AWS/Cloud milestone' },
  { id: 'security_ace', name: 'Security Specialist',       emoji: '🔐', color: '#ef4444', desc: 'Mastered cybersecurity and ethical hacking',   milestoneKeywords: ['security', 'penetration', 'owasp', 'siem', 'cryptography'], unlockCondition: 'Complete Security milestone' },
  { id: 'career_ready', name: 'Career Ready',              emoji: '🚀', color: '#10b981', desc: 'Completed the full career roadmap!',           milestoneKeywords: ['ready', 'career ready'], unlockCondition: 'Complete 100% of the roadmap' },
];

// ─── Utility helpers ──────────────────────────────────────────────────────────
const BADGE_TIMESTAMPS_KEY = (career) => `rdp_badge_timestamps_v2_${career?.toLowerCase().replace(/\s+/g, '_')}`;





const STATUS = { NOT_STARTED: 'not_started', IN_PROGRESS: 'in_progress', COMPLETED: 'completed' };

const statusLabel = { not_started: 'Not Started', in_progress: 'In Progress', completed: 'Completed' };
const statusColor = { not_started: '#64748b', in_progress: '#fbbf24', completed: '#10b981' };
const statusBg   = { not_started: 'rgba(100,116,139,0.08)', in_progress: 'rgba(251,191,36,0.08)', completed: 'rgba(16,185,129,0.08)' };
const statusBorder = { not_started: 'rgba(100,116,139,0.2)', in_progress: 'rgba(251,191,36,0.2)', completed: 'rgba(16,185,129,0.2)' };

const nextStatus = { not_started: STATUS.IN_PROGRESS, in_progress: STATUS.COMPLETED, completed: STATUS.NOT_STARTED };

const getDifficultyColor = (d) =>
  d === 'Advanced' ? '#f87171' : d === 'Intermediate' ? '#fbbf24' : '#34d399';

const getDemandColor = (d) =>
  d?.toLowerCase().includes('very high') || d?.toLowerCase().includes('critical') ? '#10b981' :
  d?.toLowerCase().includes('high') ? '#60a5fa' : '#94a3b8';

const formatNumber = (n) => n >= 1000 ? `${(n / 1000).toFixed(0)}K+` : String(n);


// ─── KPI Stat Card ────────────────────────────────────────────────────────────
const StatCard = ({ emoji, label, value, color = '#6366f1', sub }) => (
  <div style={{
    backgroundColor: 'rgba(255,255,255,0.01)', border: `1px solid ${color}25`,
    borderRadius: '10px', padding: '1rem 1.25rem',
    display: 'flex', flexDirection: 'column', gap: '0.3rem',
    transition: 'border-color 0.2s ease',
  }}
    onMouseEnter={e => e.currentTarget.style.borderColor = `${color}50`}
    onMouseLeave={e => e.currentTarget.style.borderColor = `${color}25`}
  >
    <div style={{ fontSize: '1.5rem' }}>{emoji}</div>
    <div style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', fontWeight: '700', letterSpacing: '0.05em' }}>{label}</div>
    <div style={{ fontSize: '1.4rem', fontWeight: '800', color, fontFamily: "'Outfit',sans-serif" }}>{value}</div>
    {sub && <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{sub}</div>}
  </div>
);


// ─── Resource list item ───────────────────────────────────────────────────────
const ResourceItem = ({ res }) => {
  const typeColors = { Course: '#a78bfa', Documentation: '#38bdf8', Video: '#f472b6', Practice: '#34d399', Book: '#fbbf24' };
  const c = typeColors[res.type] || '#94a3b8';
  return (
    <a href={res.url} target="_blank" rel="noopener noreferrer" style={{
      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      backgroundColor: 'rgba(255,255,255,0.02)', border: '1px solid var(--border-color)',
      padding: '0.45rem 0.75rem', borderRadius: '6px', textDecoration: 'none', gap: '0.5rem',
      fontSize: '0.78rem', color: '#818cf8', transition: 'all 0.2s ease'
    }}
      onMouseEnter={e => { e.currentTarget.style.backgroundColor = 'rgba(99,102,241,0.08)'; e.currentTarget.style.borderColor = '#6366f140'; }}
      onMouseLeave={e => { e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.02)'; e.currentTarget.style.borderColor = 'var(--border-color)'; }}
    >
      <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>📘 {res.name}</span>
      <span style={{ fontSize: '0.6rem', fontWeight: '700', backgroundColor: c + '15', color: c, padding: '0.1rem 0.4rem', borderRadius: '3px', flexShrink: 0, textTransform: 'uppercase' }}>
        {res.type}
      </span>
    </a>
  );
};

// ─── Project card ─────────────────────────────────────────────────────────────
const ProjectCard = ({ proj }) => {
  const dc = proj.difficulty === 'Advanced' ? '#f87171' : proj.difficulty === 'Beginner' ? '#34d399' : '#fbbf24';
  return (
    <div style={{
      backgroundColor: 'rgba(255,255,255,0.015)', border: '1px solid var(--border-color)',
      borderRadius: '8px', padding: '0.85rem', transition: 'border-color 0.2s ease'
    }}
      onMouseEnter={e => e.currentTarget.style.borderColor = `${dc}40`}
      onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border-color)'}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.3rem', gap: '0.5rem' }}>
        <span style={{ fontWeight: '700', fontSize: '0.85rem', color: 'var(--text-light)' }}>{proj.title}</span>
        <span style={{ fontSize: '0.62rem', fontWeight: '700', backgroundColor: dc + '12', color: dc, border: `1px solid ${dc}25`, padding: '0.1rem 0.4rem', borderRadius: '3px', flexShrink: 0, textTransform: 'uppercase' }}>
          {proj.difficulty}
        </span>
      </div>
      <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', margin: 0, lineHeight: '1.5' }}>{proj.description}</p>
      {proj.tech && proj.tech.length > 0 && (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem', marginTop: '0.5rem' }}>
          {proj.tech.slice(0, 5).map((t, i) => (
            <span key={i} style={{ fontSize: '0.62rem', backgroundColor: 'rgba(99,102,241,0.08)', color: '#a5b4fc', border: '1px solid rgba(99,102,241,0.15)', padding: '0.1rem 0.35rem', borderRadius: '3px' }}>{t}</span>
          ))}
        </div>
      )}
      {proj.estimated_hours && (
        <div style={{ fontSize: '0.65rem', color: '#475569', marginTop: '0.4rem' }}>⏱ ~{proj.estimated_hours}h</div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN COMPONENT
// ═══════════════════════════════════════════════════════════════════════════════
export const RoadmapDashboard = ({ roadmapData, onClose, candidateName }) => {
  const location = useLocation();
  const stateRoadmapData = location.state?.roadmapData;
  const initialRoadmapData = roadmapData || stateRoadmapData;

  const [activeSubTab, setActiveSubTab] = useState('timeline');
  const [selectedMonth, setSelectedMonth] = useState(1);
  const [expandedWeeks, setExpandedWeeks] = useState({});
  const [expandedMilestones, setExpandedMilestones] = useState({});
  const [milestoneProgress, setMilestoneProgress] = useState({});
  const [badgeTimestamps, setBadgeTimestamps] = useState({});
  const [shareLoading, setShareLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [shareMsg, setShareMsg] = useState('');
  
  // SaaS live state
  const [loading, setLoading] = useState(!initialRoadmapData);
  const [liveRoadmap, setLiveRoadmap] = useState(initialRoadmapData);
  const [apiTasks, setApiTasks] = useState([]);
  const [apiProgress, setApiProgress] = useState(null);
  const [apiAnalytics, setApiAnalytics] = useState(null);

  useEffect(() => {
    const fetchActiveRoadmap = async () => {
      try {
        if (!initialRoadmapData) {
          setLoading(true);
        }
        const res = await getActiveRoadmap();
        if (res?.success && res.data?.roadmap) {
          const combined = {
            ...res.data.roadmap,
            milestones: res.data.milestones || [],
            progress: res.data.progress,
            analytics: res.data.analytics
          };
          setLiveRoadmap(combined);
          setApiTasks(res.data.tasks || []);
          setApiProgress(res.data.progress);
          setApiAnalytics(res.data.analytics);
        }
      } catch (err) {
        console.error("Failed to fetch active roadmap:", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchActiveRoadmap();
  }, [initialRoadmapData]);

  // Helper for index/milestone_index mapping
  const getMsIndex = (ms) => ms.milestone_index !== undefined ? ms.milestone_index : ms.index;

  // ── Load progress from localStorage ────────────────────────────────────────
  useEffect(() => {
    if (liveRoadmap?.milestones) {
      const init = {};
      const completedIndices = apiProgress?.completed_milestones || [];
      (liveRoadmap?.milestones || []).forEach(m => {
        const index = getMsIndex(m);
        const isComplete = completedIndices.includes(index) || m.complete;
        init[index] = isComplete ? STATUS.COMPLETED : STATUS.NOT_STARTED;
      });
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setMilestoneProgress(init);
    }
  }, [liveRoadmap, apiProgress]);



  const career = liveRoadmap?.career;
  const jm = liveRoadmap?.job_market;
  const cf = liveRoadmap?.career_forecast;

  // ── Skill status mapping ───────────────────────────────────────────────────
  const skillStatus = {};
  ((liveRoadmap?.matched_skills || []) || []).forEach(s => {
    skillStatus[s.toLowerCase().trim()] = STATUS.COMPLETED;
  });
  (liveRoadmap?.milestones || []).forEach(m => {
    const idx = getMsIndex(m);
    const status = milestoneProgress[idx] || STATUS.NOT_STARTED;
    m.skills.forEach(s => {
      const s_key = s.toLowerCase().trim();
      if (status === STATUS.COMPLETED || m.complete) {
        skillStatus[s_key] = STATUS.COMPLETED;
      } else if (status === STATUS.IN_PROGRESS && skillStatus[s_key] !== STATUS.COMPLETED) {
        skillStatus[s_key] = STATUS.IN_PROGRESS;
      }
    });
  });

  const masteredSkillsSet = new Set((liveRoadmap?.matched_skills || []) || []);
  (liveRoadmap?.milestones || []).forEach(m => {
    const idx = getMsIndex(m);
    if (milestoneProgress[idx] === STATUS.COMPLETED || m.complete) {
      m.skills.forEach(s => masteredSkillsSet.add(s));
    }
  });
  const liveSkillsMastered = masteredSkillsSet.size;

  const allSkillsSet = new Set([
    ...((liveRoadmap?.matched_skills || []) || []),
    ...((liveRoadmap?.missing_skills || []) || [])
  ]);
  const liveSkillsRemaining = Math.max(0, allSkillsSet.size - liveSkillsMastered);

  // ── Computed metrics ────────────────────────────────────────────────────────
  const totalMilestones = (liveRoadmap?.milestones || []).filter(m => !m.title.toLowerCase().includes('ready')).length;
  const completedCount = Object.values(milestoneProgress).filter(s => s === STATUS.COMPLETED).length;
  const inProgressCount = Object.values(milestoneProgress).filter(s => s === STATUS.IN_PROGRESS).length;
  
  // Use DB-recalculated completion percentages if available
  const completionPct = apiProgress 
    ? Math.round(apiProgress.current_roadmap_completion) 
    : (totalMilestones > 0 ? Math.round((completedCount / totalMilestones) * 100) : 0);
  
  const baseReadiness = (liveRoadmap?.progress?.completion_percentage || 0) || 0;
  const liveReadiness = apiProgress
    ? apiProgress.current_readiness
    : (completionPct >= 100 ? (liveRoadmap?.expected_readiness || 0) : Math.min(99, Math.round(baseReadiness + (completionPct / 100) * ((liveRoadmap?.expected_readiness || 0) - baseReadiness))));
  
  const skillAcqPct = Math.min(100, completionPct + Math.round(inProgressCount * (50 / Math.max(totalMilestones, 1))));

  // Success Probability live calculation
  const demandLevel = jm?.demand_level || 'High';
  const demandLower = demandLevel.toLowerCase();
  let demandContrib;
  if (demandLower.includes("very high") || demandLower.includes("critical")) {
    demandContrib = 15;
  } else if (demandLower.includes("high")) {
    demandContrib = 10;
  } else if (demandLower.includes("medium") || demandLower.includes("steady")) {
    demandContrib = 5;
  } else {
    demandContrib = 2;
  }

  const projectsList = (liveRoadmap?.projects || []) || [];
  const projectCount = projectsList.length;
  let portfolioContrib;
  if (projectCount >= 2) {
    portfolioContrib = 15;
  } else if (projectCount === 1) {
    portfolioContrib = 8;
  } else {
    portfolioContrib = 0;
  }
  
  const liveSuccessProbability = apiAnalytics 
    ? apiAnalytics.success_probability 
    : Math.min(98, Math.round(liveReadiness + demandContrib + portfolioContrib));

  // Dynamic Durations
  const getWeekStatus = (weekNumber) => {
    const weekTasks = apiTasks.filter(t => t.week_number === weekNumber);
    if (weekTasks.length === 0) return STATUS.NOT_STARTED;
    if (weekTasks.every(t => t.status === 'Completed')) return STATUS.COMPLETED;
    if (weekTasks.some(t => t.status === 'Completed' || t.status === 'In Progress')) return STATUS.IN_PROGRESS;
    return STATUS.NOT_STARTED;
  };

  let completedWeeksCount = 0;
  (liveRoadmap?.monthly_roadmap || []).forEach(month => {
    month.weeks.forEach(week => {
      if (getWeekStatus(week.week_number) === STATUS.COMPLETED) {
        completedWeeksCount++;
      }
    });
  });

  const remainingWeeks = Math.max(0, (liveRoadmap?.total_weeks || 0) - completedWeeksCount);
  const remainingMonths = Math.max(0, Math.ceil(remainingWeeks / 4));
  const remainingStudyHours = remainingWeeks * 8;

  const getEstCompletionDate = (weeksLeft) => {
    const d = new Date();
    d.setDate(d.getDate() + (weeksLeft * 7));
    return d.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' });
  };
  const liveEstCompletionDate = getEstCompletionDate(remainingWeeks);

  // ── Badge earned functions ──────────────────────────────────────────────────
  const checkIsEarned = (badge) => {
    if (badge.id === 'career_ready') return completionPct >= 100;
    const matches = (liveRoadmap?.milestones || []).filter(m => 
      badge.milestoneKeywords.some(kw => m.title.toLowerCase().includes(kw))
    );
    if (matches.length === 0) return false;
    return matches.every(m => milestoneProgress[getMsIndex(m)] === STATUS.COMPLETED);
  };


  const unlockedBadges = BADGE_CATALOG.filter(badge => checkIsEarned(badge));

  // ── Badge timestamps effect ──────────────────────────────────────────────────
  useEffect(() => {
    let changed = false;
    const updated = { ...badgeTimestamps };
    BADGE_CATALOG.forEach(badge => {
      const isEarned = checkIsEarned(badge);
      if (isEarned && !updated[badge.id]) {
        updated[badge.id] = new Date().toLocaleString();
        changed = true;
      } else if (!isEarned && updated[badge.id]) {
        delete updated[badge.id];
        changed = true;
      }
    });
    if (changed) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setBadgeTimestamps(updated);
      localStorage.setItem(BADGE_TIMESTAMPS_KEY(career), JSON.stringify(updated));
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [milestoneProgress, completionPct, career]);

  // ── Milestone status toggle ─────────────────────────────────────────────────
  const toggleMilestoneStatus = useCallback(async (milestoneIndex) => {
    const current = milestoneProgress[milestoneIndex] || STATUS.NOT_STARTED;
    const next = nextStatus[current];
    const nextBackendStatus = next === STATUS.COMPLETED ? 'Completed' : 'Not Started';
    
    // Find all tasks associated with this milestone
    const milestone = (liveRoadmap?.milestones || []).find(m => getMsIndex(m) === milestoneIndex);
    if (!milestone) return;
    
    const milestoneSkills = (milestone.skills || []).map(s => s.toLowerCase().trim());
    const matchedTasks = apiTasks.filter(t => {
      const titleLower = t.title.toLowerCase();
      const descLower = (t.description || "").toLowerCase();
      return milestoneSkills.some(skill => titleLower.includes(skill) || descLower.includes(skill));
    });
    
    // If no tasks match by skills, fall back to week mapping
    let tasksToUpdate = matchedTasks;
    if (tasksToUpdate.length === 0) {
      const weeksPerMilestone = Math.max(1, (liveRoadmap?.total_weeks || 0) / Math.max(1, (liveRoadmap?.milestones || []).length));
      const startWeek = milestoneIndex * weeksPerMilestone + 1;
      const endWeek = (milestoneIndex + 1) * weeksPerMilestone;
      tasksToUpdate = apiTasks.filter(t => startWeek <= t.week_number && t.week_number <= endWeek);
    }
    
    if (tasksToUpdate.length === 0) return;
    
    try {
      // Update all these tasks to the next state in sequence
      let lastRes = null;
      for (const task of tasksToUpdate) {
        lastRes = await updateTaskStatus(task.task_id, nextBackendStatus);
      }
      
      if (lastRes?.success && lastRes.data) {
        setApiTasks(lastRes.data.tasks || []);
        setApiProgress(lastRes.data.progress);
        setApiAnalytics(lastRes.data.analytics);
        if (lastRes.data.milestones) {
          const combined = {
            ...liveRoadmap,
            milestones: lastRes.data.milestones,
            progress: lastRes.data.progress,
            analytics: lastRes.data.analytics
          };
          setLiveRoadmap(combined);
        }
      }
    } catch (err) {
      console.error("Failed to toggle milestone tasks:", err);
    }
  }, [liveRoadmap, apiTasks, milestoneProgress]);

  const toggleWeek = (wn) => setExpandedWeeks(prev => ({ ...prev, [wn]: !prev[wn] }));
  const toggleMilestone = (idx) => setExpandedMilestones(prev => ({ ...prev, [idx]: !prev[idx] }));

  const getWeekTasks = (weekNumber) => {
    return apiTasks.filter(t => t.week_number === weekNumber);
  };

  const renderTaskItem = (task) => {
    const statusIcons = { not_started: '⏳', in_progress: '🔄', completed: '✅', skipped: '🛑' };
    const statusLabels = { not_started: 'Not Started', in_progress: 'In Progress', completed: 'Completed', skipped: 'Skipped' };
    const statusBgColors = { not_started: 'rgba(255,255,255,0.02)', in_progress: 'rgba(245,158,11,0.08)', completed: 'rgba(16,185,129,0.08)', skipped: 'rgba(239,68,68,0.08)' };
    const statusBorders = { not_started: 'var(--border-color)', in_progress: 'rgba(245,158,11,0.3)', completed: 'rgba(16,185,129,0.3)', skipped: 'rgba(239,68,68,0.3)' };
    const statusTextColors = { not_started: 'var(--text-muted)', in_progress: '#f59e0b', completed: 'var(--success)', skipped: '#f87171' };
    
    const normStatus = (task.status || 'Not Started').toLowerCase().replace(' ', '_');
    
    const cycleStatus = async () => {
      const statusCycle = ['not_started', 'in_progress', 'completed', 'skipped'];
      const nextIdx = (statusCycle.indexOf(normStatus) + 1) % statusCycle.length;
      const nextNorm = statusCycle[nextIdx];
      const nextBackendStatus = nextNorm.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
      
      try {
        const res = await updateTaskStatus(task.task_id, nextBackendStatus);
        if (res.success && res.data) {
          setApiTasks(res.data.tasks || []);
          setApiProgress(res.data.progress);
          setApiAnalytics(res.data.analytics);
          if (res.data.milestones) {
            const combined = {
              ...liveRoadmap,
              milestones: res.data.milestones,
              progress: res.data.progress,
              analytics: res.data.analytics
            };
            setLiveRoadmap(combined);
          }
        }
      } catch (err) {
        console.error("Failed to update task status:", err);
      }
    };
    
    return (
      <div key={task.id} style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0.6rem 0.85rem',
        backgroundColor: statusBgColors[normStatus],
        border: `1px solid ${statusBorders[normStatus]}`,
        borderRadius: '6px',
        fontSize: '0.82rem',
        gap: '0.75rem',
        transition: 'all 0.2s ease'
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.15rem', flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
            <span style={{ 
              fontSize: '0.62rem', 
              fontWeight: '700', 
              backgroundColor: 'rgba(255,255,255,0.05)', 
              color: '#a5b4fc', 
              padding: '0.1rem 0.35rem', 
              borderRadius: '3px',
              textTransform: 'uppercase'
            }}>
              {task.type}
            </span>
            <span style={{ fontWeight: '600', color: '#fff', textAlign: 'left' }}>{task.title}</span>
          </div>
          {task.description && (
            <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textAlign: 'left' }}>{task.description}</span>
          )}
        </div>
        
        <button 
          onClick={cycleStatus} 
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.3rem',
            fontSize: '0.72rem',
            fontWeight: '700',
            backgroundColor: 'transparent',
            border: `1px solid ${statusBorders[normStatus]}`,
            color: statusTextColors[normStatus],
            padding: '0.25rem 0.6rem',
            borderRadius: '20px',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            whiteSpace: 'nowrap'
          }}
          onMouseEnter={(e) => { e.target.style.backgroundColor = statusTextColors[normStatus] + '15'; }}
          onMouseLeave={(e) => { e.target.style.backgroundColor = 'transparent'; }}
        >
          <span>{statusIcons[normStatus]}</span>
          <span>{statusLabels[normStatus]}</span>
        </button>
      </div>
    );
  };

  const currentMonthPlan = (liveRoadmap?.monthly_roadmap || []).find(m => m.month_number === selectedMonth) || (liveRoadmap?.monthly_roadmap || [])[0];

  // ── Share roadmap ───────────────────────────────────────────────────────────
  const handleShare = async () => {
    setShareLoading(true);
    setShareMsg('');
    try {
      const result = await shareRoadmap(liveRoadmap, candidateName || 'Candidate');
      const fullUrl = `${window.location.origin}${window.location.pathname}#shared/${result.share_id}`;
      await navigator.clipboard.writeText(fullUrl);
      setShareMsg('✓ Link copied to clipboard!');
    } catch {
      setShareMsg('⚠ Failed to generate share link.');
    } finally {
      setShareLoading(false);
      setTimeout(() => setShareMsg(''), 4000);
    }
  };

  // ── Export PDF ──────────────────────────────────────────────────────────────
  const handleExportPDF = async () => {
    setPdfLoading(true);
    try {
      await exportRoadmapPDF(liveRoadmap, candidateName || 'Candidate');
    } catch (err) {
      alert(`PDF export failed: ${err.message}`);
    } finally {
      setPdfLoading(false);
    }
  };

  // ─────────────────────────────────────────────────────────────────────────
  // RENDER
  // ─────────────────────────────────────────────────────────────────────────
  // If liveRoadmap is not loaded yet
  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '6rem 2rem' }}>
        <div className="spinner"></div>
        <p style={{ color: 'var(--text-muted)', fontWeight: '500' }}>Loading live study progress...</p>
      </div>
    );
  }

  if (!liveRoadmap) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        No active career roadmap found.
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', animation: 'fadeIn 0.3s ease' }}>
      <style>{`
        @keyframes badgeUnlock {
          0% { transform: scale(0.5); opacity: 0; }
          60% { transform: scale(1.15); }
          100% { transform: scale(1); opacity: 1; }
        }
        @keyframes pulse-glow {
          0%, 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0); }
          50% { box-shadow: 0 0 0 6px rgba(99,102,241,0.2); }
        }
        .roadmap-syllabus-grid {
          display: grid;
          grid-template-columns: 1.5fr 1fr;
          gap: 2rem;
          align-items: flex-start;
        }
        .roadmap-week-detail-grid {
          display: grid;
          grid-template-columns: 1fr 1.2fr;
          gap: 1.5rem;
          align-items: flex-start;
        }
        .roadmap-salary-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1rem;
          margin-bottom: 1rem;
        }
        .roadmap-header-actions {
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 0.75rem;
        }
        @media (max-width: 850px) {
          .roadmap-syllabus-grid {
            grid-template-columns: 1fr !important;
            gap: 1.5rem !important;
          }
          .roadmap-week-detail-grid {
            grid-template-columns: 1fr !important;
            gap: 1.25rem !important;
          }
          .roadmap-salary-grid {
            grid-template-columns: 1fr !important;
          }
          .roadmap-header-actions {
            align-items: flex-start !important;
            width: 100% !important;
          }
        }
      `}</style>

      {/* ─── Header Card ──────────────────────────────────────────────────── */}
      <div style={{
        backgroundColor: 'var(--bg-card)', padding: '1.75rem 2rem',
        borderRadius: '12px', border: '1px solid var(--border-color)',
        background: 'linear-gradient(135deg, rgba(99,102,241,0.04) 0%, var(--bg-card) 60%)'
      }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1.5rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
            <span style={{ fontSize: '0.75rem', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: '700' }}>
              Career Intelligence Roadmap
            </span>
            <h2 style={{ fontSize: '1.9rem', fontWeight: '800', color: 'var(--text-light)', fontFamily: "'Outfit',sans-serif", margin: 0 }}>
              {career} Roadmap
            </h2>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.25rem' }}>
              <span style={{ fontSize: '0.72rem', fontWeight: '600', backgroundColor: 'rgba(255,255,255,0.03)', color: 'var(--text-muted)', border: '1px solid var(--border-color)', padding: '0.22rem 0.6rem', borderRadius: '4px' }}>
                ⏱️ {(liveRoadmap?.total_weeks || 0)}w / {(liveRoadmap?.total_months || 0)}mo
              </span>
              <span style={{ fontSize: '0.72rem', fontWeight: '700', backgroundColor: `${getDifficultyColor((liveRoadmap?.difficulty || 'Beginner'))}15`, color: getDifficultyColor((liveRoadmap?.difficulty || 'Beginner')), border: `1px solid ${getDifficultyColor((liveRoadmap?.difficulty || 'Beginner'))}30`, padding: '0.22rem 0.6rem', borderRadius: '4px', textTransform: 'uppercase' }}>
                ⚡ {(liveRoadmap?.difficulty || 'Beginner')}
              </span>
              {jm?.demand_level && (
                <span style={{ fontSize: '0.72rem', fontWeight: '700', backgroundColor: `${getDemandColor(jm.demand_level)}15`, color: getDemandColor(jm.demand_level), border: `1px solid ${getDemandColor(jm.demand_level)}30`, padding: '0.22rem 0.6rem', borderRadius: '4px' }}>
                  🔥 {jm.demand_level} Demand
                </span>
              )}
            </div>
          </div>

          <div className="roadmap-header-actions">
            {/* Live readiness meter */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Readiness</div>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.3rem', justifyContent: 'flex-end' }}>
                  <span style={{ fontSize: '0.95rem', color: 'var(--text-muted)', textDecoration: 'line-through' }}>{baseReadiness}%</span>
                  <span style={{ fontSize: '1.6rem', fontWeight: '800', color: 'var(--success)' }}>→ {liveReadiness}%</span>
                </div>
              </div>
              <div style={{
                width: '56px', height: '56px', borderRadius: '50%',
                background: `conic-gradient(var(--success) ${liveReadiness * 3.6}deg, rgba(255,255,255,0.06) 0deg)`,
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                <div style={{ width: '44px', height: '44px', borderRadius: '50%', backgroundColor: 'var(--bg-card)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem' }}>🚀</div>
              </div>
            </div>

            {/* Action buttons */}
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', justifyContent: 'flex-end' }}>
              <button onClick={handleExportPDF} disabled={pdfLoading} style={{
                fontSize: '0.78rem', fontWeight: '600', padding: '0.4rem 0.85rem',
                backgroundColor: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.25)',
                color: '#a7f3d0', borderRadius: '6px', cursor: 'pointer', transition: 'all 0.2s ease'
              }}
                onMouseEnter={e => { e.target.style.backgroundColor = 'var(--success)'; e.target.style.color = '#fff'; }}
                onMouseLeave={e => { e.target.style.backgroundColor = 'rgba(16,185,129,0.1)'; e.target.style.color = '#a7f3d0'; }}
              >
                {pdfLoading ? '⏳ Generating...' : '📄 Export PDF'}
              </button>
              <button onClick={onClose} style={{
                fontSize: '0.78rem', fontWeight: '600', padding: '0.4rem 0.85rem',
                backgroundColor: 'transparent', border: '1px solid var(--border-color)',
                color: 'var(--text-muted)', borderRadius: '6px', cursor: 'pointer', transition: 'all 0.2s ease'
              }}
                onMouseEnter={e => { e.target.style.color = 'var(--text-light)'; e.target.style.borderColor = 'var(--text-light)'; }}
                onMouseLeave={e => { e.target.style.color = 'var(--text-muted)'; e.target.style.borderColor = 'var(--border-color)'; }}
              >
                ← Back
              </button>
            </div>
            {shareMsg && <div style={{ fontSize: '0.75rem', color: '#a7f3d0', fontWeight: '600' }}>{shareMsg}</div>}
          </div>
        </div>
      </div>


      {/* ─── Tab Navigation ───────────────────────────────────────────────── */}
      <div style={{ display: 'flex', borderBottom: '1px solid var(--border-color)', gap: '0.25rem', overflowX: 'auto' }}>
        {[
          { id: 'timeline',     label: '🗺️ Timeline' },
          { id: 'monthly',      label: '📅 Syllabus' },
          { id: 'milestones',   label: '🏆 Milestones' },
          { id: 'intelligence', label: '📡 Career Intel' },
          { id: 'analytics',    label: '📊 Analytics' },
        ].map(tab => (
          <button key={tab.id} onClick={() => setActiveSubTab(tab.id)} style={{
            backgroundColor: 'transparent', border: 'none', whiteSpace: 'nowrap',
            borderBottom: activeSubTab === tab.id ? '2px solid var(--primary)' : '2px solid transparent',
            color: activeSubTab === tab.id ? 'var(--text-light)' : 'var(--text-muted)',
            padding: '0.7rem 0.85rem', cursor: 'pointer', fontSize: '0.88rem', fontWeight: '600',
            transition: 'all 0.2s ease', outline: 'none'
          }}>{tab.label}</button>
        ))}
      </div>

      {/* ═══════════════════════════════════════════════════════════════════ */}
      {/* TAB: TIMELINE VIEW                                                  */}
      {/* ═══════════════════════════════════════════════════════════════════ */}
      {activeSubTab === 'timeline' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', paddingLeft: '1.25rem', borderLeft: '2px solid rgba(99,102,241,0.3)', position: 'relative' }}>
          {(liveRoadmap?.monthly_roadmap || []).map((month, idx) => {
            const isCapstone = month.title.toLowerCase().includes('capstone') || month.title.toLowerCase().includes('portfolio');
            const dotColor = isCapstone ? '#10b981' : '#6366f1';
            return (
              <div key={idx} style={{ position: 'relative', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                <div style={{ position: 'absolute', left: '-1.5rem', top: '0.3rem', width: '10px', height: '10px', borderRadius: '50%', backgroundColor: dotColor, border: '3px solid var(--bg-dark)', boxShadow: `0 0 8px ${dotColor}60` }} />
                <div style={{ fontWeight: '700', fontSize: '0.75rem', color: isCapstone ? '#10b981' : '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Month {month.month_number} {isCapstone ? '🎓' : ''}
                </div>
                <div style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-light)' }}>{month.title}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Skills: {month.skills.join(' → ')}</div>
                {month.goals?.length > 0 && (
                  <div style={{ fontSize: '0.75rem', color: '#475569' }}>Goals: {month.goals.slice(0, 2).join(' • ')}</div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* ═══════════════════════════════════════════════════════════════════ */}
      {/* TAB: MONTHLY SYLLABUS                                               */}
      {/* ═══════════════════════════════════════════════════════════════════ */}
      {activeSubTab === 'monthly' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2rem' }}>
          {/* Month selector pills */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', borderBottom: '1px dashed var(--border-color)', paddingBottom: '1rem' }}>
            {(liveRoadmap?.monthly_roadmap || []).map(month => (
              <button key={month.month_number} onClick={() => setSelectedMonth(month.month_number)} style={{
                backgroundColor: selectedMonth === month.month_number ? 'var(--primary)' : 'rgba(255,255,255,0.03)',
                border: '1px solid var(--border-color)',
                color: selectedMonth === month.month_number ? '#fff' : 'var(--text-muted)',
                padding: '0.4rem 0.9rem', borderRadius: '20px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '600', transition: 'all 0.2s ease'
              }}>M{month.month_number}</button>
            ))}
          </div>

          <div className="roadmap-syllabus-grid">
            {/* Left: weekly syllabus */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: '#a5b4fc', textTransform: 'uppercase', fontWeight: '700' }}>Month {currentMonthPlan?.month_number} · Active Syllabus</span>
                <h3 style={{ fontSize: '1.35rem', fontWeight: '700', color: 'var(--text-light)', margin: '0.25rem 0 0', fontFamily: "'Outfit',sans-serif" }}>
                  {currentMonthPlan?.title}
                </h3>
              </div>

              {currentMonthPlan?.weeks?.map(week => (
                <div key={week.week_number} style={{ backgroundColor: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '8px', overflow: 'hidden' }}>
                  <button onClick={() => toggleWeek(week.week_number)} style={{
                    width: '100%', backgroundColor: 'transparent', border: 'none',
                    padding: '0.9rem 1.1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                    cursor: 'pointer', color: 'var(--text-light)', outline: 'none'
                  }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.1rem', textAlign: 'left' }}>
                      <span style={{ fontSize: '0.68rem', color: '#a5b4fc', fontWeight: '700', textTransform: 'uppercase' }}>Week {week.week_number}</span>
                      <span style={{ fontWeight: '600', fontSize: '0.9rem' }}>{week.title}</span>
                    </div>
                    <span style={{ transform: expandedWeeks[week.week_number] ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s ease', color: 'var(--text-muted)', fontSize: '0.8rem' }}>▼</span>
                  </button>

                  {expandedWeeks[week.week_number] && (
                    <div style={{ 
                      padding: '1.1rem', 
                      borderTop: '1px solid var(--border-color)', 
                      display: 'flex', 
                      flexDirection: 'column', 
                      gap: '1rem', 
                      backgroundColor: 'rgba(255,255,255,0.005)',
                      animation: 'fadeIn 0.2s ease' 
                    }}>
                      <div className="roadmap-week-detail-grid">
                        {/* Left Column: Topics & Resources */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                          <div>
                            <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: '#a5b4fc', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                              📝 Syllabus Topics
                            </h5>
                            <ul style={{ paddingLeft: '1.1rem', margin: 0, display: 'flex', flexDirection: 'column', gap: '0.3rem', fontSize: '0.8rem', color: '#cbd5e1' }}>
                              {week.topics?.map((t, i) => <li key={i}>{t}</li>)}
                            </ul>
                          </div>

                          {week.expected_outcome && (
                            <div style={{ 
                              backgroundColor: 'rgba(16,185,129,0.04)', 
                              border: '1px solid rgba(16,185,129,0.15)', 
                              borderRadius: '6px', 
                              padding: '0.65rem 0.8rem' 
                            }}>
                              <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: '#34d399', marginBottom: '0.2rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                🎯 Target Learning Outcome
                              </h5>
                              <p style={{ fontSize: '0.78rem', color: '#e2e8f0', margin: 0, lineHeight: '1.4' }}>
                                {week.expected_outcome}
                              </p>
                            </div>
                          )}

                          {week.resources?.length > 0 && (
                            <div>
                              <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: '#38bdf8', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                📚 Recommended Resources
                              </h5>
                              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                                {week.resources.map((res, i) => <ResourceItem key={i} res={res} />)}
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Right Column: Interactive Checklist Tasks */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                          <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: 'var(--primary)', marginBottom: '0.2rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                            📋 Weekly Progress Checklist
                          </h5>
                          {getWeekTasks(week.week_number).length > 0 ? (
                            getWeekTasks(week.week_number).map(task => renderTaskItem(task))
                          ) : (
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                              No tasks generated for this week.
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Right: goals + projects */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              <div className="section-card" style={{ padding: '1.25rem', margin: 0 }}>
                <h4 style={{ fontSize: '0.9rem', fontWeight: '700', color: 'var(--text-light)', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.4rem', marginBottom: '0.65rem' }}>🎯 Monthly Targets</h4>
                <ul style={{ listStyleType: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {currentMonthPlan?.goals?.map((g, i) => (
                    <li key={i} style={{ display: 'flex', gap: '0.4rem', fontSize: '0.8rem', color: '#cbd5e1', alignItems: 'flex-start' }}>
                      <span style={{ color: 'var(--primary)', fontWeight: '700' }}>⚡</span><span>{g}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="section-card" style={{ padding: '1.25rem', margin: 0 }}>
                <h4 style={{ fontSize: '0.9rem', fontWeight: '700', color: 'var(--text-light)', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.4rem', marginBottom: '0.85rem' }}>🛠️ Portfolio Projects</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {currentMonthPlan?.projects?.map((proj, i) => <ProjectCard key={i} proj={proj} />)}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ═══════════════════════════════════════════════════════════════════ */}
      {/* TAB: MILESTONE CHECKLIST (Smart Progress Tracking)                  */}
      {/* ═══════════════════════════════════════════════════════════════════ */}
      {activeSubTab === 'milestones' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
          {(liveRoadmap?.milestones || []).map(ms => {
            const idx = getMsIndex(ms);
            const status = milestoneProgress[idx] || STATUS.NOT_STARTED;
            const isExpanded = expandedMilestones[idx];
            const isFinal = ms.title.toLowerCase().includes('ready');

            return (
              <div key={idx} style={{
                backgroundColor: statusBg[status], border: `1px solid ${statusBorder[status]}`,
                borderRadius: '10px', overflow: 'hidden', transition: 'all 0.3s ease'
              }}>
                {/* Milestone header */}
                <div style={{ padding: '1rem 1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  {/* Status badge (clickable) */}
                  <button
                    onClick={() => !isFinal && toggleMilestoneStatus(idx)}
                    disabled={isFinal}
                    style={{
                      fontSize: '0.65rem', fontWeight: '700',
                      backgroundColor: statusBg[status], color: statusColor[status],
                      border: `1.5px solid ${statusBorder[status]}`,
                      padding: '0.3rem 0.65rem', borderRadius: '20px',
                      cursor: isFinal ? 'default' : 'pointer',
                      transition: 'all 0.2s ease', whiteSpace: 'nowrap', flexShrink: 0,
                      textTransform: 'uppercase', letterSpacing: '0.04em'
                    }}
                  >
                    {status === STATUS.COMPLETED ? '✅' : status === STATUS.IN_PROGRESS ? '🔄' : '⏳'} {statusLabel[status]}
                  </button>

                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: '700', fontSize: '0.88rem', color: 'var(--text-light)', fontFamily: "'Outfit',sans-serif" }}>{ms.title}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.15rem' }}>
                      Skills: {ms.skills.slice(0, 4).join(' · ')}{ms.skills.length > 4 ? ` +${ms.skills.length - 4} more` : ''}
                    </div>
                  </div>

                  {/* Expand toggle */}
                  {!isFinal && (ms.resources?.length > 0 || ms.projects?.length > 0) && (
                    <button onClick={() => toggleMilestone(idx)} style={{
                      backgroundColor: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-muted)',
                      padding: '0.3rem 0.6rem', borderRadius: '6px', cursor: 'pointer', fontSize: '0.75rem', flexShrink: 0,
                      transition: 'all 0.2s ease'
                    }}
                      onMouseEnter={e => { e.target.style.borderColor = '#6366f1'; e.target.style.color = '#a5b4fc'; }}
                      onMouseLeave={e => { e.target.style.borderColor = 'var(--border-color)'; e.target.style.color = 'var(--text-muted)'; }}
                    >
                      {isExpanded ? 'Hide ▲' : 'Resources & Projects ▼'}
                    </button>
                  )}
                </div>

                {/* Expandable: resources + projects */}
                {isExpanded && !isFinal && (
                  <div style={{ borderTop: '1px solid var(--border-color)', padding: '1rem 1.25rem', display: 'flex', flexDirection: 'column', gap: '1.25rem', animation: 'fadeIn 0.2s ease' }}>
                    {ms.resources?.length > 0 && (
                      <div>
                        <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: 'var(--text-light)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>📚 Learning Resources</h5>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '0.35rem' }}>
                          {ms.resources.map((res, i) => <ResourceItem key={i} res={res} />)}
                        </div>
                      </div>
                    )}

                    {ms.projects?.length > 0 && (
                      <div>
                        <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: 'var(--text-light)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>🛠️ Portfolio Projects</h5>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '0.6rem' }}>
                          {ms.projects.map((proj, i) => <ProjectCard key={i} proj={proj} />)}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* ═══════════════════════════════════════════════════════════════════ */}
      {/* TAB: CAREER INTELLIGENCE (Job Market + Forecast)                    */}
      {/* ═══════════════════════════════════════════════════════════════════ */}
      {activeSubTab === 'intelligence' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
          {/* Career Forecast Section */}
          {cf && (
            <div>
              <h3 style={{ fontSize: '1.05rem', fontWeight: '700', color: 'var(--text-light)', marginBottom: '1rem', fontFamily: "'Outfit',sans-serif" }}>
                🔭 Career Outcome Forecast
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '0.85rem' }}>
                <StatCard emoji="🎯" label="Current Readiness" value={`${liveReadiness}%`} color="#6366f1" />
                <StatCard emoji="🚀" label="Projected Readiness" value={`${(liveRoadmap?.expected_readiness || 0)}%`} color="#10b981" sub="After completing roadmap" />
                <StatCard emoji="📈" label="Success Probability" value={`${liveSuccessProbability}%`} color="#f59e0b" sub="Job landing estimate" />
                <StatCard emoji="⏱️" label="Time to Job Ready" value={remainingWeeks > 0 ? `${remainingWeeks}w (~${remainingMonths}mo)` : 'Job Ready!'} color="#60a5fa" />
                <StatCard emoji="✅" label="Skills Mastered" value={liveSkillsMastered} color="#34d399" />
                <StatCard emoji="📚" label="Skills Remaining" value={liveSkillsRemaining} color="#f472b6" />
                <StatCard emoji="⏱️" label="Total Study Hours" value={`${remainingStudyHours} hrs`} color="#e0f2fe" sub="Remaining time" />
                <StatCard emoji="📅" label="Est. Completion Date" value={liveEstCompletionDate} color="#c084fc" sub="Based on workload" />
              </div>

              {cf.eligible_roles?.length > 0 && (
                <div style={{ marginTop: '1.25rem', backgroundColor: 'rgba(99,102,241,0.05)', border: '1px solid rgba(99,102,241,0.15)', borderRadius: '10px', padding: '1.1rem' }}>
                  <h4 style={{ fontSize: '0.8rem', fontWeight: '700', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>
                    🎓 Eligible Roles After Completion
                  </h4>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {cf.eligible_roles.map((role, i) => (
                      <span key={i} style={{ fontSize: '0.8rem', fontWeight: '600', backgroundColor: 'rgba(99,102,241,0.1)', color: '#a5b4fc', border: '1px solid rgba(99,102,241,0.25)', padding: '0.3rem 0.77rem', borderRadius: '20px' }}>
                        {i === 0 ? '⭐ ' : ''}{role}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Job Market Intelligence */}
          {jm ? (
            <div>
              <h3 style={{ fontSize: '1.05rem', fontWeight: '700', color: 'var(--text-light)', marginBottom: '1rem', fontFamily: "'Outfit',sans-serif" }}>
                💼 Job Market Intelligence
              </h3>

              {/* Salary Grid */}
              <div className="roadmap-salary-grid">
                {[
                  { flag: '🇮🇳', region: 'India Salary Tiers', data: jm.india_salary, color: '#f97316' },
                  { flag: '🌍', region: 'Global Salary Tiers', data: jm.global_salary, color: '#38bdf8' },
                ].map(({ flag, region, data, color }) => (
                  <div key={region} style={{ 
                    backgroundColor: `${color}05`, 
                    border: `1px solid ${color}20`, 
                    borderRadius: '12px', 
                    padding: '1.25rem',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.75rem'
                  }}>
                    <div style={{ fontSize: '0.72rem', fontWeight: '700', color, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      {flag} {region}
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      {[
                        { label: 'Entry Level', value: data?.entry },
                        { label: 'Mid Level', value: data?.mid },
                        { label: 'Senior Level', value: data?.senior },
                      ].map(tier => {
                        const isObject = tier.value && typeof tier.value === 'object';
                        const salaryText = isObject ? tier.value.salary_range : tier.value;
                        const expText = isObject ? tier.value.experience : null;
                        const demandText = isObject ? tier.value.demand_level : null;

                        return (
                          <div key={tier.label} style={{ 
                            display: 'flex', 
                            flexDirection: 'column',
                            gap: '0.25rem',
                            padding: '0.5rem 0.6rem',
                            backgroundColor: 'rgba(255,255,255,0.02)',
                            border: '1px solid var(--border-color)',
                            borderRadius: '6px'
                          }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: '600' }}>{tier.label}</span>
                              <span style={{ fontSize: '0.85rem', color: '#fff', fontWeight: '700', fontFamily: "'Outfit',sans-serif" }}>{salaryText || '—'}</span>
                            </div>
                            {isObject && (expText || demandText) && (
                              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.68rem', color: 'var(--text-muted)' }}>
                                <span>Exp: {expText || '—'}</span>
                                <span style={{ color: demandText === 'Critical' || demandText === 'Very High' ? '#fb7185' : 'var(--text-muted)' }}>
                                  Demand: {demandText || '—'}
                                </span>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                    <div style={{ fontSize: '0.65rem', color: '#64748b', textAlign: 'center', marginTop: '0.2rem' }}>
                      Overall Average: <strong style={{ color: '#fff' }}>{data?.formatted || '—'}</strong>
                    </div>
                  </div>
                ))}
              </div>

              {/* Market Stats */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: '0.75rem', marginBottom: '1rem' }}>
                <StatCard emoji="🔥" label="Demand Level" value={jm.demand_level} color={getDemandColor(jm.demand_level)} />
                <StatCard emoji="📊" label="Hiring Trend" value={jm.hiring_trend} color="#a78bfa" />
                <StatCard emoji="📈" label="YoY Growth" value={jm.yoy_growth} color="#34d399" />
                <StatCard emoji="💼" label="Job Openings" value={formatNumber(jm.estimated_job_openings)} color="#f59e0b" sub="Estimated annually" />
                <StatCard emoji="🏠" label="Remote Friendly" value={jm.remote_friendly ? 'Yes' : 'No'} color={jm.remote_friendly ? '#34d399' : '#f87171'} />
              </div>

              {/* Top Employers */}
              {jm.top_employers?.length > 0 && (
                <div style={{ backgroundColor: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '10px', padding: '1.1rem', marginBottom: '1rem' }}>
                  <h4 style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.65rem' }}>🏢 Top Hiring Companies</h4>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {jm.top_employers.map((co, i) => (
                      <span key={i} style={{ fontSize: '0.78rem', fontWeight: '600', backgroundColor: 'rgba(255,255,255,0.04)', color: '#e2e8f0', border: '1px solid rgba(255,255,255,0.1)', padding: '0.3rem 0.7rem', borderRadius: '6px' }}>
                        {co}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Certifications */}
              {jm.certification_boost?.length > 0 && (
                <div style={{ backgroundColor: 'rgba(16,185,129,0.04)', border: '1px solid rgba(16,185,129,0.15)', borderRadius: '10px', padding: '1.1rem' }}>
                  <h4 style={{ fontSize: '0.78rem', fontWeight: '700', color: '#10b981', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.65rem' }}>🎓 Recommended Certifications</h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                    {jm.certification_boost.map((cert, i) => (
                      <div key={i} style={{ display: 'flex', gap: '0.5rem', fontSize: '0.82rem', color: '#cbd5e1', alignItems: 'flex-start' }}>
                        <span style={{ color: '#10b981', flexShrink: 0 }}>✓</span>
                        <span>{cert}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
              No job market data available for this career path.
            </div>
          )}
        </div>
      )}

      {/* ═══════════════════════════════════════════════════════════════════ */}
      {/* TAB: ANALYTICS DASHBOARD                                            */}
      {/* ═══════════════════════════════════════════════════════════════════ */}
      {activeSubTab === 'analytics' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

          {/* KPI cards grid */}
          <div>
            <h4 style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.85rem' }}>Key Performance Indicators</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(170px, 1fr))', gap: '0.75rem' }}>
              <StatCard emoji="🎯" label="Current Readiness" value={`${liveReadiness}%`} color="#6366f1" />
              <StatCard emoji="🚀" label="Projected Readiness" value={`${(liveRoadmap?.expected_readiness || 0)}%`} color="#10b981" />
              <StatCard emoji="✅" label="Skills Mastered" value={liveSkillsMastered} color="#34d399" />
              <StatCard emoji="📚" label="Skills Remaining" value={liveSkillsRemaining} color="#f472b6" />
              <StatCard emoji="⏱️" label="Est. Job Ready" value={remainingWeeks > 0 ? `${remainingWeeks} weeks` : 'Ready!'} color="#60a5fa" />
              <StatCard emoji="📈" label="Success Probability" value={`${liveSuccessProbability}%`} color="#f59e0b" />
              <StatCard emoji="🏆" label="Milestones Done" value={`${completedCount}/${totalMilestones}`} color="#a78bfa" />
              <StatCard emoji="🛠️" label="Projects Available" value={(liveRoadmap?.milestones || []).reduce((acc, m) => acc + (m.projects?.length || 0), 0)} color="#38bdf8" sub="Portfolio projects" />
              {jm && <StatCard emoji="💰" label="India Salary" value={jm.india_salary?.formatted || '—'} color="#f97316" />}
              {jm && <StatCard emoji="🌍" label="Global Salary" value={jm.global_salary?.formatted || '—'} color="#38bdf8" />}
              {jm && <StatCard emoji="💼" label="Job Openings" value={formatNumber(jm.estimated_job_openings)} color="#fbbf24" />}
              <strong style={{ display: 'none' }} />
              <StatCard emoji="⏱️" label="Total Study Hours" value={`${remainingStudyHours} hrs`} color="#e0f2fe" sub="Remaining time" />
              <StatCard emoji="📅" label="Target Date" value={liveEstCompletionDate} color="#c084fc" sub="Based on workload" />
              <StatCard emoji="⏱️" label="Weekly Workload" value="8 hours" color="#60a5fa" sub="Suggested pace" />
              <StatCard emoji="🗓️" label="Monthly Workload" value="32 hours" color="#34d399" sub="Suggested pace" />
            </div>
          </div>

          {/* Milestone status breakdown */}
          <div style={{ backgroundColor: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '10px', padding: '1.25rem' }}>
            <h4 style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '1rem' }}>Milestone Breakdown</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {[
                { label: 'Completed', count: completedCount, color: '#10b981', icon: '✅' },
                { label: 'Uncompleted', count: totalMilestones - completedCount, color: '#ef4444', icon: '❌' },
              ].map(row => (
                <div key={row.label} style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <span style={{ fontSize: '0.8rem', color: row.color, width: '110px', flexShrink: 0, fontWeight: '600' }}>{row.icon} {row.label}</span>
                  <div style={{ flex: 1 }} />
                  <span style={{ fontSize: '0.8rem', color: row.color, fontWeight: '700', width: '30px', textAlign: 'right' }}>{row.count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RoadmapDashboard;

