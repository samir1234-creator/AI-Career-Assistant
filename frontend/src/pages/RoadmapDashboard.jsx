import React, { useState, useEffect, useCallback } from 'react';
import { shareRoadmap, exportRoadmapPDF, getSharedRoadmap } from '../services/api';

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
const STORAGE_KEY = (career) => `rdp_progress_v2_${career?.toLowerCase().replace(/\s+/g, '_')}`;
const BADGE_TIMESTAMPS_KEY = (career) => `rdp_badge_timestamps_v2_${career?.toLowerCase().replace(/\s+/g, '_')}`;

const loadProgress = (career) => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY(career));
    return raw ? JSON.parse(raw) : {};
  } catch { return {}; }
};

const saveProgress = (career, data) => {
  try { localStorage.setItem(STORAGE_KEY(career), JSON.stringify(data)); } catch {}
};

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

// ─── Progress Ring (pure CSS conic-gradient) ──────────────────────────────────
const ProgressRing = ({ pct, size = 80, color = '#6366f1', label, sublabel, emoji }) => (
  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.4rem' }}>
    <div style={{
      width: size, height: size, borderRadius: '50%',
      background: `conic-gradient(${color} ${pct * 3.6}deg, rgba(255,255,255,0.06) 0deg)`,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      boxShadow: `0 0 16px ${color}30`
    }}>
      <div style={{
        width: size - 14, height: size - 14, borderRadius: '50%',
        backgroundColor: 'var(--bg-card)',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '1px'
      }}>
        {emoji && <span style={{ fontSize: size * 0.22 }}>{emoji}</span>}
        <span style={{ fontSize: size * 0.2, fontWeight: '800', color: '#fff', lineHeight: 1 }}>{pct}%</span>
      </div>
    </div>
    {label && <div style={{ fontSize: '0.7rem', color: '#fff', fontWeight: '700', textAlign: 'center', maxWidth: size }}>{label}</div>}
    {sublabel && <div style={{ fontSize: '0.65rem', color: '#64748b', textAlign: 'center', maxWidth: size }}>{sublabel}</div>}
  </div>
);

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

// ─── Badge Card ───────────────────────────────────────────────────────────────
const BadgeCard = ({ badge, unlocked, timestamp, progress }) => (
  <div style={{
    backgroundColor: unlocked ? `${badge.color}10` : 'rgba(255,255,255,0.01)',
    border: `1px solid ${unlocked ? badge.color + '40' : 'rgba(255,255,255,0.06)'}`,
    borderRadius: '12px', padding: '1.1rem',
    display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem',
    opacity: unlocked ? 1 : 0.5,
    transition: 'all 0.3s ease',
    animation: unlocked ? 'badgeUnlock 0.5s cubic-bezier(0.34,1.56,0.64,1)' : 'none',
    filter: unlocked ? 'none' : 'grayscale(1)',
    cursor: unlocked ? 'default' : 'not-allowed',
    position: 'relative',
    overflow: 'hidden'
  }}>
    <div style={{ fontSize: '2.2rem', filter: unlocked ? `drop-shadow(0 0 8px ${badge.color})` : 'none' }}>
      {badge.emoji}
    </div>
    <div style={{ fontSize: '0.75rem', fontWeight: '800', color: unlocked ? badge.color : '#475569', textAlign: 'center' }}>
      {badge.name}
    </div>
    <div style={{ fontSize: '0.65rem', color: '#64748b', textAlign: 'center', lineHeight: '1.4' }}>
      {badge.desc}
    </div>
    
    <div style={{ 
      fontSize: '0.6rem', 
      color: unlocked ? '#cbd5e1' : '#475569', 
      textAlign: 'center', 
      marginTop: '0.2rem',
      borderTop: '1px dashed rgba(255,255,255,0.04)',
      paddingTop: '0.3rem',
      width: '100%'
    }}>
      <strong>Condition:</strong> {badge.unlockCondition}
    </div>
    
    <div style={{ fontSize: '0.6rem', color: unlocked ? badge.color : '#64748b', fontWeight: '700' }}>
      Progress: {progress}
    </div>

    {unlocked && (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.25rem', marginTop: '0.25rem' }}>
        <div style={{
          fontSize: '0.6rem', fontWeight: '700', backgroundColor: badge.color + '20',
          color: badge.color, padding: '0.15rem 0.5rem', borderRadius: '20px', textTransform: 'uppercase'
        }}>✓ Unlocked</div>
        {timestamp && (
          <div style={{ fontSize: '0.55rem', color: '#64748b' }}>Earned: {timestamp}</div>
        )}
      </div>
    )}
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
  const [activeSubTab, setActiveSubTab] = useState('timeline');
  const [selectedMonth, setSelectedMonth] = useState(1);
  const [expandedWeeks, setExpandedWeeks] = useState({});
  const [expandedMilestones, setExpandedMilestones] = useState({});
  const [milestoneProgress, setMilestoneProgress] = useState({});
  const [badgeTimestamps, setBadgeTimestamps] = useState({});
  const [shareLoading, setShareLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [shareMsg, setShareMsg] = useState('');
  const [newlyUnlocked, setNewlyUnlocked] = useState(new Set());

  if (!roadmapData) return null;

  const career = roadmapData.career;
  const jm = roadmapData.job_market;
  const cf = roadmapData.career_forecast;

  // ── Load progress from localStorage ────────────────────────────────────────
  useEffect(() => {
    const saved = loadProgress(career);
    const savedTimestamps = localStorage.getItem(BADGE_TIMESTAMPS_KEY(career));
    setBadgeTimestamps(savedTimestamps ? JSON.parse(savedTimestamps) : {});

    // Auto-populate: milestones with complete=true from backend start as completed
    const init = { ...saved };
    roadmapData.milestones.forEach(m => {
      if (m.complete && !init[m.index]) {
        init[m.index] = STATUS.COMPLETED;
      } else if (!init[m.index]) {
        init[m.index] = STATUS.NOT_STARTED;
      }
    });
    setMilestoneProgress(init);
  }, [career, roadmapData.milestones]);

  // ── Skill status mapping ───────────────────────────────────────────────────
  const skillStatus = {};
  (roadmapData.matched_skills || []).forEach(s => {
    skillStatus[s.toLowerCase().trim()] = STATUS.COMPLETED;
  });
  roadmapData.milestones.forEach(m => {
    const status = milestoneProgress[m.index] || STATUS.NOT_STARTED;
    m.skills.forEach(s => {
      const s_key = s.toLowerCase().trim();
      if (status === STATUS.COMPLETED || m.complete) {
        skillStatus[s_key] = STATUS.COMPLETED;
      } else if (status === STATUS.IN_PROGRESS && skillStatus[s_key] !== STATUS.COMPLETED) {
        skillStatus[s_key] = STATUS.IN_PROGRESS;
      }
    });
  });

  const masteredSkillsSet = new Set(roadmapData.matched_skills || []);
  roadmapData.milestones.forEach(m => {
    if (milestoneProgress[m.index] === STATUS.COMPLETED || m.complete) {
      m.skills.forEach(s => masteredSkillsSet.add(s));
    }
  });
  const liveSkillsMastered = masteredSkillsSet.size;

  const allSkillsSet = new Set([
    ...(roadmapData.matched_skills || []),
    ...(roadmapData.missing_skills || [])
  ]);
  const liveSkillsRemaining = Math.max(0, allSkillsSet.size - liveSkillsMastered);

  // ── Computed metrics ────────────────────────────────────────────────────────
  const totalMilestones = roadmapData.milestones.filter(m => !m.title.toLowerCase().includes('ready')).length;
  const completedCount = Object.values(milestoneProgress).filter(s => s === STATUS.COMPLETED).length;
  const inProgressCount = Object.values(milestoneProgress).filter(s => s === STATUS.IN_PROGRESS).length;
  const completionPct = totalMilestones > 0 ? Math.round((completedCount / totalMilestones) * 100) : 0;
  
  const baseReadiness = roadmapData.progress?.completion_percentage || 0;
  const liveReadiness = completionPct >= 100 ? roadmapData.expected_readiness : Math.min(99, Math.round(baseReadiness + (completionPct / 100) * (roadmapData.expected_readiness - baseReadiness)));
  const skillAcqPct = Math.min(100, completionPct + Math.round(inProgressCount * (50 / Math.max(totalMilestones, 1))));

  // Success Probability live calculation
  const demandLevel = jm?.demand_level || 'High';
  const demandLower = demandLevel.toLowerCase();
  let demandContrib = 10;
  if (demandLower.includes("very high") || demandLower.includes("critical")) {
    demandContrib = 15;
  } else if (demandLower.includes("high")) {
    demandContrib = 10;
  } else if (demandLower.includes("medium") || demandLower.includes("steady")) {
    demandContrib = 5;
  } else {
    demandContrib = 2;
  }

  const projectsList = roadmapData.projects || [];
  const projectCount = projectsList.length;
  let portfolioContrib = 0;
  if (projectCount >= 2) {
    portfolioContrib = 15;
  } else if (projectCount === 1) {
    portfolioContrib = 8;
  } else {
    portfolioContrib = 0;
  }
  const liveSuccessProbability = Math.min(98, Math.round(liveReadiness + demandContrib + portfolioContrib));

  // Dynamic Durations
  const getWeekStatus = (week, monthSkills) => {
    const titleLower = week.title.toLowerCase();
    const matchingSkill = monthSkills.find(s => 
      titleLower.includes(s.toLowerCase()) || 
      week.topics.some(t => t.toLowerCase().includes(s.toLowerCase()))
    ) || monthSkills[0];
    if (!matchingSkill) return STATUS.NOT_STARTED;
    return skillStatus[matchingSkill.toLowerCase().trim()] || STATUS.NOT_STARTED;
  };

  let completedWeeksCount = 0;
  roadmapData.monthly_roadmap.forEach(month => {
    month.weeks.forEach(week => {
      if (getWeekStatus(week, month.skills) === STATUS.COMPLETED) {
        completedWeeksCount++;
      }
    });
  });

  const remainingWeeks = Math.max(0, roadmapData.total_weeks - completedWeeksCount);
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
    const matches = roadmapData.milestones.filter(m => 
      badge.milestoneKeywords.some(kw => m.title.toLowerCase().includes(kw))
    );
    if (matches.length === 0) return false;
    return matches.every(m => milestoneProgress[m.index] === STATUS.COMPLETED);
  };

  const getBadgeProgress = (badge) => {
    if (badge.id === 'career_ready') return `${completionPct}%`;
    const matches = roadmapData.milestones.filter(m => 
      badge.milestoneKeywords.some(kw => m.title.toLowerCase().includes(kw))
    );
    if (matches.length === 0) return "N/A";
    const completed = matches.filter(m => milestoneProgress[m.index] === STATUS.COMPLETED).length;
    return `${completed}/${matches.length}`;
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
      setBadgeTimestamps(updated);
      localStorage.setItem(BADGE_TIMESTAMPS_KEY(career), JSON.stringify(updated));
    }
  }, [milestoneProgress, completionPct, career]);

  // ── Milestone status toggle ─────────────────────────────────────────────────
  const toggleMilestoneStatus = useCallback((milestoneIndex) => {
    setMilestoneProgress(prev => {
      const current = prev[milestoneIndex] || STATUS.NOT_STARTED;
      const next = nextStatus[current];
      const updated = { ...prev, [milestoneIndex]: next };
      saveProgress(career, updated);

      // Trigger temporary newly unlocked badges state for visual highlight
      if (next === STATUS.COMPLETED) {
        setTimeout(() => {
          setNewlyUnlocked(nu => {
            const s = new Set(nu);
            BADGE_CATALOG.forEach(badge => {
              const m = roadmapData.milestones.find(ms => ms.index === milestoneIndex);
              if (m) {
                const isMatch = badge.milestoneKeywords.some(kw => m.title.toLowerCase().includes(kw));
                if (isMatch) s.add(badge.id);
              }
            });
            return s;
          });
        }, 200);
      }
      return updated;
    });
  }, [career, roadmapData.milestones]);

  const toggleWeek = (wn) => setExpandedWeeks(prev => ({ ...prev, [wn]: !prev[wn] }));
  const toggleMilestone = (idx) => setExpandedMilestones(prev => ({ ...prev, [idx]: !prev[idx] }));

  const currentMonthPlan = roadmapData.monthly_roadmap.find(m => m.month_number === selectedMonth) || roadmapData.monthly_roadmap[0];

  // ── Share roadmap ───────────────────────────────────────────────────────────
  const handleShare = async () => {
    setShareLoading(true);
    setShareMsg('');
    try {
      const result = await shareRoadmap(roadmapData, candidateName || 'Candidate');
      const fullUrl = `${window.location.origin}${window.location.pathname}#shared/${result.share_id}`;
      await navigator.clipboard.writeText(fullUrl);
      setShareMsg('✓ Link copied to clipboard!');
    } catch (err) {
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
      await exportRoadmapPDF(roadmapData, candidateName || 'Candidate');
    } catch (err) {
      alert(`PDF export failed: ${err.message}`);
    } finally {
      setPdfLoading(false);
    }
  };

  // ─────────────────────────────────────────────────────────────────────────
  // RENDER
  // ─────────────────────────────────────────────────────────────────────────
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', animation: 'fadeIn 0.3s ease' }}>
      {/* CSS for badge animation */}
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
                ⏱️ {roadmapData.total_weeks}w / {roadmapData.total_months}mo
              </span>
              <span style={{ fontSize: '0.72rem', fontWeight: '700', backgroundColor: `${getDifficultyColor(roadmapData.difficulty)}15`, color: getDifficultyColor(roadmapData.difficulty), border: `1px solid ${getDifficultyColor(roadmapData.difficulty)}30`, padding: '0.22rem 0.6rem', borderRadius: '4px', textTransform: 'uppercase' }}>
                ⚡ {roadmapData.difficulty}
              </span>
              {jm?.demand_level && (
                <span style={{ fontSize: '0.72rem', fontWeight: '700', backgroundColor: `${getDemandColor(jm.demand_level)}15`, color: getDemandColor(jm.demand_level), border: `1px solid ${getDemandColor(jm.demand_level)}30`, padding: '0.22rem 0.6rem', borderRadius: '4px' }}>
                  🔥 {jm.demand_level} Demand
                </span>
              )}
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.75rem' }}>
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
              <button onClick={handleShare} disabled={shareLoading} style={{
                fontSize: '0.78rem', fontWeight: '600', padding: '0.4rem 0.85rem',
                backgroundColor: 'rgba(99,102,241,0.1)', border: '1px solid rgba(99,102,241,0.25)',
                color: '#a5b4fc', borderRadius: '6px', cursor: 'pointer', transition: 'all 0.2s ease'
              }}
                onMouseEnter={e => { e.target.style.backgroundColor = 'var(--primary)'; e.target.style.color = '#fff'; }}
                onMouseLeave={e => { e.target.style.backgroundColor = 'rgba(99,102,241,0.1)'; e.target.style.color = '#a5b4fc'; }}
              >
                {shareLoading ? '⏳ Sharing...' : '🔗 Share Roadmap'}
              </button>
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

      {/* ─── Live Progress Bar ─────────────────────────────────────────────── */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', padding: '1.25rem', borderRadius: '10px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.4rem', fontWeight: '700' }}>
          <span style={{ color: 'var(--text-light)' }}>Live Roadmap Completion</span>
          <span style={{ color: 'var(--primary)' }}>{completionPct}% complete • {completedCount}/{totalMilestones} milestones</span>
        </div>
        <div style={{ width: '100%', height: '8px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '4px', overflow: 'hidden' }}>
          <div style={{
            width: `${completionPct}%`, height: '100%',
            background: `linear-gradient(90deg, var(--primary), #10b981)`,
            borderRadius: '4px', transition: 'width 0.6s cubic-bezier(0.4,0,0.2,1)'
          }} />
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1.25rem', marginTop: '0.75rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          <div>✅ Completed: <strong style={{ color: 'var(--success)' }}>{completedCount}</strong></div>
          <div>🔄 In Progress: <strong style={{ color: '#fbbf24' }}>{inProgressCount}</strong></div>
          <div>⏳ Remaining: <strong style={{ color: '#94a3b8' }}>{totalMilestones - completedCount - inProgressCount}</strong></div>
          <div>📊 Skill Acquisition: <strong style={{ color: '#a5b4fc' }}>{skillAcqPct}%</strong></div>
          <div>🎯 Live Readiness: <strong style={{ color: 'var(--success)' }}>{liveReadiness}%</strong></div>
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
          { id: 'badges',       label: `🏅 Badges (${unlockedBadges.length}/${BADGE_CATALOG.length})` },
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
          {roadmapData.monthly_roadmap.map((month, idx) => {
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
            {roadmapData.monthly_roadmap.map(month => (
              <button key={month.month_number} onClick={() => setSelectedMonth(month.month_number)} style={{
                backgroundColor: selectedMonth === month.month_number ? 'var(--primary)' : 'rgba(255,255,255,0.03)',
                border: '1px solid var(--border-color)',
                color: selectedMonth === month.month_number ? '#fff' : 'var(--text-muted)',
                padding: '0.4rem 0.9rem', borderRadius: '20px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '600', transition: 'all 0.2s ease'
              }}>M{month.month_number}</button>
            ))}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '2rem', alignItems: 'flex-start' }}>
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
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', alignItems: 'flex-start' }}>
                        {/* Left Column */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                          <div>
                            <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: '#a5b4fc', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                              📝 Syllabus Topics
                            </h5>
                            <ul style={{ paddingLeft: '1.1rem', margin: 0, display: 'flex', flexDirection: 'column', gap: '0.3rem', fontSize: '0.8rem', color: '#cbd5e1' }}>
                              {week.topics?.map((t, i) => <li key={i}>{t}</li>)}
                            </ul>
                          </div>
                          
                          {week.practice_tasks?.length > 0 && (
                            <div>
                              <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: '#fbbf24', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                🛠️ Hands-on Practice
                              </h5>
                              <ul style={{ paddingLeft: '1.1rem', margin: 0, display: 'flex', flexDirection: 'column', gap: '0.3rem', fontSize: '0.8rem', color: '#cbd5e1' }}>
                                {week.practice_tasks.map((pt, i) => <li key={i}>{pt}</li>)}
                              </ul>
                            </div>
                          )}

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
                        </div>

                        {/* Right Column */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                          {week.mini_assignments?.length > 0 && (
                            <div>
                              <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: '#f472b6', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                ✏️ Mini Assignments
                              </h5>
                              <ul style={{ paddingLeft: '1.1rem', margin: 0, display: 'flex', flexDirection: 'column', gap: '0.3rem', fontSize: '0.8rem', color: '#cbd5e1' }}>
                                {week.mini_assignments.map((ma, i) => <li key={i}>{ma}</li>)}
                              </ul>
                            </div>
                          )}

                          {week.quiz && (
                            <div>
                              <h5 style={{ fontSize: '0.72rem', fontWeight: '700', color: '#60a5fa', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                ❓ Weekly Assessment
                              </h5>
                              <div style={{ 
                                fontSize: '0.78rem', 
                                color: '#e2e8f0', 
                                backgroundColor: 'rgba(96,165,250,0.05)', 
                                border: '1px solid rgba(96,165,250,0.15)', 
                                borderRadius: '6px', 
                                padding: '0.4rem 0.6rem',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.4rem'
                              }}>
                                <span>📝</span> <strong>Quiz:</strong> {week.quiz}
                              </div>
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
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', backgroundColor: 'rgba(99,102,241,0.05)', border: '1px solid rgba(99,102,241,0.15)', borderRadius: '8px', padding: '0.75rem 1rem' }}>
            💡 Click a milestone status badge to cycle through: <strong style={{ color: '#fbbf24' }}>Not Started</strong> → <strong style={{ color: '#fbbf24' }}>In Progress</strong> → <strong style={{ color: '#10b981' }}>Completed</strong>. Progress saves automatically.
          </div>

          {roadmapData.milestones.map(ms => {
            const status = milestoneProgress[ms.index] || STATUS.NOT_STARTED;
            const isExpanded = expandedMilestones[ms.index];
            const isFinal = ms.title.toLowerCase().includes('ready');

            return (
              <div key={ms.index} style={{
                backgroundColor: statusBg[status], border: `1px solid ${statusBorder[status]}`,
                borderRadius: '10px', overflow: 'hidden', transition: 'all 0.3s ease'
              }}>
                {/* Milestone header */}
                <div style={{ padding: '1rem 1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  {/* Status badge (clickable) */}
                  <button
                    onClick={() => !isFinal && toggleMilestoneStatus(ms.index)}
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
                    <button onClick={() => toggleMilestone(ms.index)} style={{
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
                <StatCard emoji="🚀" label="Projected Readiness" value={`${roadmapData.expected_readiness}%`} color="#10b981" sub="After completing roadmap" />
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
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
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
          {/* Progress rings row */}
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-light)', marginBottom: '1.25rem', fontFamily: "'Outfit',sans-serif" }}>
              📊 Career Readiness Analytics
            </h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '2rem', justifyContent: 'center', backgroundColor: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '12px', padding: '2rem' }}>
              <ProgressRing pct={liveReadiness} size={100} color="#6366f1" label="Career Readiness" sublabel="Live score" emoji="🎯" />
              <ProgressRing pct={roadmapData.expected_readiness} size={100} color="#10b981" label="Projected Readiness" sublabel="After completion" emoji="🚀" />
              <ProgressRing pct={completionPct} size={100} color="#f59e0b" label="Roadmap Completion" sublabel={`${completedCount}/${totalMilestones} milestones`} emoji="🏆" />
              <ProgressRing pct={skillAcqPct} size={100} color="#f472b6" label="Skill Acquisition" sublabel="In progress + done" emoji="📚" />
              <ProgressRing pct={liveSuccessProbability} size={100} color="#38bdf8" label="Success Probability" sublabel="Job landing estimate" emoji="📈" />
            </div>
          </div>

          {/* KPI cards grid */}
          <div>
            <h4 style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.85rem' }}>Key Performance Indicators</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(170px, 1fr))', gap: '0.75rem' }}>
              <StatCard emoji="🎯" label="Current Readiness" value={`${liveReadiness}%`} color="#6366f1" />
              <StatCard emoji="🚀" label="Projected Readiness" value={`${roadmapData.expected_readiness}%`} color="#10b981" />
              <StatCard emoji="✅" label="Skills Mastered" value={liveSkillsMastered} color="#34d399" />
              <StatCard emoji="📚" label="Skills Remaining" value={liveSkillsRemaining} color="#f472b6" />
              <StatCard emoji="⏱️" label="Est. Job Ready" value={remainingWeeks > 0 ? `${remainingWeeks} weeks` : 'Ready!'} color="#60a5fa" />
              <StatCard emoji="📈" label="Success Probability" value={`${liveSuccessProbability}%`} color="#f59e0b" />
              <StatCard emoji="🏆" label="Milestones Done" value={`${completedCount}/${totalMilestones}`} color="#a78bfa" />
              <StatCard emoji="🛠️" label="Projects Available" value={roadmapData.milestones.reduce((acc, m) => acc + (m.projects?.length || 0), 0)} color="#38bdf8" sub="Portfolio projects" />
              {jm && <StatCard emoji="💰" label="India Salary" value={jm.india_salary?.formatted || '—'} color="#f97316" />}
              {jm && <StatCard emoji="🌍" label="Global Salary" value={jm.global_salary?.formatted || '—'} color="#38bdf8" />}
              {jm && <StatCard emoji="💼" label="Job Openings" value={formatNumber(jm.estimated_job_openings)} color="#fbbf24" />}
              <StatCard emoji="🏅" label="Badges Earned" value={`${unlockedBadges.length}/${BADGE_CATALOG.length}`} color="#10b981" />
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
                { label: 'In Progress', count: inProgressCount, color: '#fbbf24', icon: '🔄' },
                { label: 'Not Started', count: totalMilestones - completedCount - inProgressCount, color: '#64748b', icon: '⏳' },
              ].map(row => (
                <div key={row.label} style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <span style={{ fontSize: '0.8rem', color: row.color, width: '110px', flexShrink: 0, fontWeight: '600' }}>{row.icon} {row.label}</span>
                  <div style={{ flex: 1, height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                    <div style={{ width: `${totalMilestones > 0 ? (row.count / totalMilestones) * 100 : 0}%`, height: '100%', backgroundColor: row.color, borderRadius: '3px', transition: 'width 0.6s ease' }} />
                  </div>
                  <span style={{ fontSize: '0.8rem', color: row.color, fontWeight: '700', width: '30px', textAlign: 'right' }}>{row.count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ═══════════════════════════════════════════════════════════════════ */}
      {/* TAB: BADGES & ACHIEVEMENTS                                          */}
      {/* ═══════════════════════════════════════════════════════════════════ */}
      {activeSubTab === 'badges' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div style={{ backgroundColor: 'rgba(16,185,129,0.04)', border: '1px solid rgba(16,185,129,0.15)', borderRadius: '10px', padding: '1rem 1.25rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <div style={{ fontSize: '1.1rem', fontWeight: '700', color: 'var(--text-light)' }}>🏅 Achievement Badges</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.15rem' }}>Complete milestones to unlock achievements. Progress saves automatically.</div>
            </div>
            <div style={{ fontSize: '1.5rem', fontWeight: '800', color: '#10b981', fontFamily: "'Outfit',sans-serif" }}>
              {unlockedBadges.length} / {BADGE_CATALOG.length} Unlocked
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '1rem' }}>
            {BADGE_CATALOG.map(badge => (
              <BadgeCard 
                key={badge.id} 
                badge={badge} 
                unlocked={unlockedBadges.some(b => b.id === badge.id)} 
                timestamp={badgeTimestamps[badge.id]}
                progress={getBadgeProgress(badge)}
              />
            ))}
          </div>

          {unlockedBadges.length > 0 && (
            <div style={{ backgroundColor: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '10px', padding: '1.1rem' }}>
              <h4 style={{ fontSize: '0.8rem', fontWeight: '700', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.65rem' }}>🎉 Your Achievements</h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {unlockedBadges.map(badge => (
                  <span key={badge.id} style={{ fontSize: '0.8rem', fontWeight: '600', backgroundColor: `${badge.color}15`, color: badge.color, border: `1px solid ${badge.color}30`, padding: '0.3rem 0.75rem', borderRadius: '20px' }}>
                    {badge.emoji} {badge.name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
